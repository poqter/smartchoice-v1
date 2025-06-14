import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="적금 vs 단기납 비교", layout="wide")

# 타이틀
st.title("💰 적금 vs 단기납 비교 분석 도구")

# 컬럼 나누기
col1, col2 = st.columns(2)

with col1:
    st.header("📌 적금")
    deposit_monthly = int(st.number_input("월 납입액 (만원)", min_value=0.0, step=1.0))
    deposit_rate = st.number_input("연 이자율 (%)", min_value=0.0, step=0.1)

with col2:
    st.header("📌 단기납")
    insurance_monthly = int(st.number_input("월 납입액 (만원)", min_value=0.0, step=1.0, key="ins_monthly"))
    return_rate = st.number_input("10년 시점 환급률 (%)", min_value=0.0, step=0.1)

# 결과 보기 버튼
if st.button("결과 보기"):
    st.markdown("---")
    st.subheader("🔍 결과 분석")

    # 계산 파트
    total_deposit = deposit_monthly * 12  # 1년 기준
    pre_tax_interest = total_deposit * (deposit_rate / 100)
    tax = pre_tax_interest * 0.154
    after_tax_interest = pre_tax_interest - tax
    total_after_tax_interest_10y = after_tax_interest * 10
    monthly_avg_interest = after_tax_interest / 12

    total_insurance = insurance_monthly * 12 * 10  # 10년 기준
    refund = total_insurance * (return_rate / 100)
    bonus = refund - total_insurance
    monthly_bonus = bonus / 120

    # 비교 테이블 생성
    compare_df = pd.DataFrame({
        "항목": [
            "원금 합계",
            "수익 총합",
            "월평균 수익"
        ],
        "적금": [
            f"{total_deposit:,.0f}만원",
            f"{total_after_tax_interest_10y:,.0f}만원",
            f"{monthly_avg_interest:,.2f}만원"
        ],
        "단기납": [
            f"{total_insurance:,.0f}만원",
            f"{bonus:,.0f}만원",
            f"{monthly_bonus:,.2f}만원"
        ],
        "차이": [
            f"{total_deposit - total_insurance:,.0f}만원",
            f"{bonus - total_after_tax_interest_10y:,.0f}만원",
            f"{monthly_bonus - monthly_avg_interest:,.2f}만원"
        ]
    })

    st.markdown("### 📊 비교 테이블")
    st.table(compare_df)

    # metric 강조
    st.markdown("### ✅ 핵심 요약")
    colm1, colm2 = st.columns(2)
    with colm1:
        st.metric("세후 이자 총합 (적금 기준)", f"{total_after_tax_interest_10y:,.0f}만원")
    with colm2:
        st.metric("보너스 총합 (단기납 기준)", f"{bonus:,.0f}만원", delta=f"{bonus - total_after_tax_interest_10y:,.0f}만원")

    # 그래프 시각화
    fig = go.Figure(data=[
        go.Bar(name='적금', x=['원금', '수익'], y=[total_deposit, total_after_tax_interest_10y]),
        go.Bar(name='단기납', x=['원금', '수익'], y=[total_insurance, bonus])
    ])
    fig.update_layout(barmode='group', title='💹 적금 vs 단기납 수익 비교')
    st.plotly_chart(fig)
