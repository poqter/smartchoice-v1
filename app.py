import streamlit as st
import pandas as pd
import time
import streamlit.components.v1 as components
from urllib.parse import quote

# 페이지 설정
st.set_page_config(page_title="적금 vs 단기납 비교", layout="wide")

# 강조 박스 함수
def emphasize_box(text, bg="#e6f2ff", color="#003366"):
    return f"""<div style='background-color:{bg}; color:{color}; padding:12px; border-radius:10px;
                font-size:20px; font-weight:bold; margin-bottom:10px;'>
                {text}
             </div>"""

# 타이틀
st.title("💰 적금 vs 단기납 비교")

# 입력 칼럼
col1, col2 = st.columns(2)

with col1:
    st.header("📌 적금")
    deposit_monthly = st.number_input("월 납입액 (만원)", min_value=0, step=1, value=None, format="%d", placeholder="예: 100")
    deposit_rate = st.number_input("연 이자율 (%)", min_value=0.0, step=0.1, value=None, placeholder="예: 2.5")

with col2:
    st.header("📌 단기납")
    insurance_monthly = st.number_input("월 납입액 (만원)", min_value=0, step=1, value=None, format="%d", placeholder="예: 100", key="ins_monthly")
    return_rate = st.number_input("10년 시점 해지환급률 (%)", min_value=0.0, step=0.1, value=None, placeholder="예: 150.0")

# 결과 보기 버튼
if st.button("결과 보기"):
    if deposit_monthly in (None, 0) or deposit_rate in (None, 0.0) or insurance_monthly in (None, 0) or return_rate in (None, 0.0):
        st.warning("⚠️ 모든 항목에 값을 입력해주세요.")
    else:
        with st.spinner("결과를 분석하는 중입니다..."):
            time.sleep(1.2)

        st.markdown("---")
        st.subheader("🔍 결과 분석")

        # 계산
        total_deposit = deposit_monthly * 12
        pre_tax_interest = total_deposit * (deposit_rate / 100)
        tax = pre_tax_interest * 0.154
        after_tax_interest = pre_tax_interest - tax
        monthly_avg_interest = after_tax_interest / 12
        total_after_tax_interest_10y = after_tax_interest * 10

        total_insurance = insurance_monthly * 12 * 5
        refund = total_insurance * (return_rate / 100)
        bonus = refund - total_insurance
        monthly_bonus = bonus / 120

        # 요약 출력
        sum1, sum2 = st.columns(2)

        with sum1:
            st.markdown("### 🧾 적금 계산 요약")
            st.write(f"- 원금 합계 (1년): {total_deposit:,.0f}만원")
            st.write(f"- 세전 이자: {pre_tax_interest:,.0f}만원")
            st.write(f"- 이자 과세 (15.4%): {tax:,.0f}만원")
            st.write(f"- 세후 이자: {after_tax_interest:,.0f}만원")

        with sum2:
            st.markdown("### 🧾 단기납 계산 요약")
            st.write(f"- 원금 합계 (5년): {total_insurance:,.0f}만원")
            st.write(f"- 10년 시점 해지환급금: {refund:,.0f}만원")
            st.write(f"- 보너스 금액: {bonus:,.0f}만원")

        # 핵심 요약
        st.markdown("### ✅ 핵심 요약")
        colm1, colm2 = st.columns(2)
        with colm1:
            st.metric("세후 이자 총합 (10년 기준)", f"{total_after_tax_interest_10y:,.0f}만원")
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown(emphasize_box(f"세후 이자 월 평균: {monthly_avg_interest:,.2f}만원", bg="#e6f2ff", color="#003366"), unsafe_allow_html=True)
        with colm2:
            st.metric("보너스 총합 (단기납 기준)", f"{bonus:,.0f}만원", delta=f"{bonus - total_after_tax_interest_10y:,.0f}만원")
            st.markdown(emphasize_box(f"보너스 월 평균: {monthly_bonus:,.2f}만원", bg="#fff3e6", color="#663300"), unsafe_allow_html=True)

        # 외부 저장용 HTML 페이지 연결 (요약 텍스트 포함 전달)
        summary_text = f"""
적금 결과 요약:\n
- 세후 이자 총합: {total_after_tax_interest_10y:,.0f}만원
- 세후 이자 월 평균: {monthly_avg_interest:,.2f}만원

단기납 결과 요약:
- 보너스 총합: {bonus:,.0f}만원
- 보너스 월 평균: {monthly_bonus:,.2f}만원"""

        encoded_summary = quote(summary_text)
        external_url = f"https://poqter.github.io/pdf-export/save.html?data={encoded_summary}"

        st.markdown("---")
        st.markdown(f"""
        <div class="no-print" style="font-size:16px;">
        📥 <strong>Tip:</strong> 결과를 PDF로 저장하려면 아래 버튼을 클릭하세요.<br><br>
        <a href="{external_url}" target="_blank" style="text-decoration:none;">
            <button style="padding:10px 20px; font-size:16px; font-weight:bold;
            background-color:#4CAF50; color:white; border:none; border-radius:8px; cursor:pointer;">
            📄 결과 저장 페이지 열기</button>
        </a>
        </div>
        <style>
        @media print {{
            .no-print {{display: none;}}
        }}
        </style>
        """, unsafe_allow_html=True)
