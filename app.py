import streamlit as st

# 페이지 설정
st.set_page_config(page_title="적금 vs 단기납 비교", layout="wide")

# 타이틀
st.title("💰 적금 vs 단기납 비교 분석 도구")

# 컬럼 나누기
col1, col2 = st.columns(2)

with col1:
    st.header("📌 적금")
    deposit_monthly = st.number_input("월 납입액 (만원)", min_value=0.0, step=1.0)
    deposit_rate = st.number_input("연 이자율 (%)", min_value=0.0, step=0.1)

with col2:
    st.header("📌 단기납")
    insurance_monthly = st.number_input("월 납입액 (만원)", min_value=0.0, step=1.0, key="ins_monthly")
    return_rate = st.number_input("10년 시점 환급률 (%)", min_value=0.0, step=0.1)

# 결과 보기 버튼
if st.button("결과 보기"):
    st.markdown("---")
    st.subheader("🔍 결과 분석")

    with col1:
        total_deposit = deposit_monthly * 12 * 10
        pre_tax_interest = total_deposit * (deposit_rate / 100)
        tax = pre_tax_interest * 0.154
        after_tax_interest = pre_tax_interest - tax
        total_received = total_deposit + after_tax_interest
        monthly_avg_interest = after_tax_interest / 120  # 10년, 120개월

        st.write("**원금 합계:**", f"{total_deposit:,.0f}만원")
        st.write("**세전 이자:**", f"{pre_tax_interest:,.0f}만원")
        st.write("**이자 과세 (15.4%):**", f"{tax:,.0f}만원")
        st.write("**세후 이자:**", f"{after_tax_interest:,.0f}만원")
        st.write("**세후 수령액:**", f"{total_received:,.0f}만원")
        st.write("**세후 이자 월 평균:**", f"{monthly_avg_interest:,.2f}만원")

    with col2:
        total_insurance = insurance_monthly * 12 * 10
        refund = total_insurance * (return_rate / 100)
        bonus = refund - total_insurance
        monthly_bonus = bonus / 120

        st.write("**원금 합계:**", f"{total_insurance:,.0f}만원")
        st.write("**해지환급금 (10년 시점):**", f"{refund:,.0f}만원")
        st.write("**보너스 금액:**", f"{bonus:,.0f}만원")
        st.write("**보너스 월 평균:**", f"{monthly_bonus:,.2f}만원")
