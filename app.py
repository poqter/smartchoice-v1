import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="적금 vs 단기납 비교", layout="wide")

# 강조 박스 함수
def emphasize_box(text, bg="#e6f2ff", color="#003366"):
    return f"""<div style='background-color:{bg}; color:{color}; padding:12px; border-radius:10px;
                font-size:14px; font-weight:bold; margin-bottom:6px;'>{text}</div>"""

# 금액 포맷 함수 (만원 이하 삭제용)
def format_currency_trim(value):
    won = int(value * 10000)
    return f"{won:,}원"

# 인쇄용 CSS 스타일 적용
st.markdown("""
<style>
@media print {
    html, body {
        font-size: 11pt;
        line-height: 1.3;
        margin: 10mm 12mm;
    }
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
    }
    .element-container {
        margin-bottom: 6px !important;
    }
    .sidebar, .no-print, header, footer {
        display: none !important;
    }
    h1, h2, h3 {
        margin: 4px 0;
    }
}
h1 a, h2 a, h3 a {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown("## 💰 적금 vs 단기납 비교")

# 입력 칼럼
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📌 적금 조건 입력**")
    deposit_monthly = st.number_input("월 납입액 (만원)", min_value=0, step=1, value=None, format="%d", placeholder="예: 100")
    deposit_rate = st.number_input("연 이자율 (%)", min_value=0.0, step=0.1, value=None, placeholder="예: 2.5")

with col2:
    st.markdown("**📌 단기납 조건 입력**")
    insurance_monthly = st.number_input("월 납입액 (만원)", min_value=0, step=1, value=None, format="%d", placeholder="예: 100", key="ins_monthly")
    return_rate = st.number_input("10년 시점 해지회급률 (%)", min_value=0.0, step=0.1, value=None, placeholder="예: 150.0")

# 결과 보기 버튼
if st.button("결과 보기"):
    if deposit_monthly in (None, 0) or deposit_rate in (None, 0.0) or insurance_monthly in (None, 0) or return_rate in (None, 0.0):
        st.warning("⚠️ 모든 항목에 값을 입력해주세요.")
    else:
        with st.spinner("결과를 계산 중입니다..."):
            time.sleep(1.0)

        st.markdown("---")
        st.markdown("### 🔍 결과 요약")

        # 적금 계산
        monthly_rate = (deposit_rate / 100) / 12
        total_deposit = deposit_monthly * 12
        interest_sum = sum([deposit_monthly * monthly_rate * (12 - m) for m in range(12)])
        tax = interest_sum * 0.154
        after_tax_interest = interest_sum - tax
        total_after_tax_interest_10y = after_tax_interest * 10
        monthly_avg_interest = after_tax_interest / 12

        # 단기납 계산
        total_insurance = insurance_monthly * 12 * 5
        refund = total_insurance * (return_rate / 100)
        bonus = refund - total_insurance
        monthly_bonus = bonus / 120

        # 요약 출력
        st.markdown(f"**✔️ 적금 세후 이자 총합 (10년)**: <span style='color:red'>{int(total_after_tax_interest_10y)}만원</span>", unsafe_allow_html=True)
        st.markdown(emphasize_box(f"세후 이자 월 평균: {monthly_avg_interest * 10000:,.0f}원", bg="#e6f2ff", color="#003366"), unsafe_allow_html=True)

        st.markdown(f"**✔️ 단기납 보너스 총합 (10년)**: <span style='color:red'>{int(bonus)}만원</span>", unsafe_allow_html=True)
        st.markdown(emphasize_box(f"단기납 보너스 월 평균: {monthly_bonus * 10000:,.0f}원", bg="#fff3e6", color="#663300"), unsafe_allow_html=True)

        # 단기납 설명 추가
        st.caption("💡 10년 이후 해지 시, **비과세 혜택** 적용 가능")

        # 역산 계산
        st.markdown("---")
        st.markdown("### 📌 비교 계산")

        if deposit_rate > 0:
            factor = sum([(12 - m) * monthly_rate for m in range(12)])
            monthly_required = (bonus / 10) / (factor * (1 - 0.154))
            st.markdown(f"👉 단기납 보너스 총합을 적금 세후 이자로 만들려면, 매달 약 **{monthly_required:,.0f}만원**을 10년간 납입해야 해요.")
        else:
            st.markdown("❗ 연 이자율이 0%여서 비교 계산이 불가능합니다.")
