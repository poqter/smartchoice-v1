import streamlit as st
import time

#############################
# 유틸리티 함수
#############################

def emphasize_box(text: str, bg: str = "#e6f2ff", color: str = "#003366") -> str:
    """HTML 강조 박스."""
    return (
        f"<div style='background-color:{bg}; color:{color}; padding:12px; border-radius:10px;"
        f" font-size:20px; font-weight:bold; margin-bottom:10px;'>{text}</div>"
    )


def format_currency_trim(value: float) -> str:
    """금액(만원)을 보기 좋게 표시. 만원 단위 이하는 원 단위로 표시."""
    won = int(value * 10000)
    return f"{won // 10000:,}만원" if won % 10000 == 0 else f"{won:,}원"


def future_value_annuity(monthly: float, monthly_rate: float, periods: int) -> float:
    """월 적립 + 복리 계산 (단위: 만원)."""
    if monthly_rate == 0:
        return monthly * periods
    return monthly * (((1 + monthly_rate) ** periods - 1) / monthly_rate)


#############################
# 메인 앱
#############################

def run():
    # ---------- 기본 페이지 설정 ---------- #
    st.set_page_config(page_title="💰 적금 vs 단기납 시뮬레이터", layout="wide")

    # ---------- 사이드바: 인쇄 안내 & 정보 ---------- #
    with st.sidebar:
        st.markdown(
            """
            ### 📄 인쇄 안내
            - 우측 상단 **⋯ → Print** 로 인쇄 / PDF 저장
            - **More Settings**
              - Header & Footer: ❌
              - Background Graphics: ✅
            """
        )
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='margin-bottom:20px;'>👨‍💻 <strong>제작자:</strong> 비전본부 드림지점 박병선 팀장</div>
            <div style='margin-bottom:20px;'>🗓️ <strong>버전:</strong> v1.1.0</div>
            <div style='margin-bottom:20px;'>📅 <strong>최종 업데이트:</strong> 2025-07-12</div>
            """,
            unsafe_allow_html=True,
        )

    # ---------- 헤더 ---------- #
    st.title("💰 적금 vs 단기납 시뮬레이터")

    # ---------- 탭 구조 ---------- #
    tab_input, tab_result, tab_help = st.tabs(["입력", "결과", "가정·도움말"])

    #############################
    # 1) 입력 탭
    #############################
    with tab_input:
        col_dep, col_ins = st.columns(2)

        # --- 적금 입력 ---
        with col_dep:
            st.header("📌 적금")
            deposit_monthly = st.slider("월 납입액 (만원)", min_value=10, max_value=500, step=10, value=100)
            deposit_rate = st.number_input(
                "연 이자율 (%)", min_value=0.0, max_value=10.0, step=0.1, value=2.5
            )

        # --- 단기납 입력 ---
        with col_ins:
            st.header("📌 단기납")
            insurance_monthly = st.slider(
                "월 납입액 (만원)", min_value=10, max_value=500, step=10, value=100, key="ins_monthly"
            )
            pay_years = st.radio("납입 기간 (년)", [5, 7], index=0, horizontal=True)
            return_rate = st.number_input(
                "10년 시점 해지환급률 (%)", min_value=0.0, max_value=200.0, step=0.1, value=123.0
            )

        calc_btn = st.button("🚀 계산하기", type="primary")

    #############################
    # 2) 결과 탭
    #############################
    if calc_btn:
        with st.spinner("계산 중입니다..."):
            time.sleep(0.3)

        # --- 적금 계산 ---
        monthly_rate = (deposit_rate / 100) / 12
        fv_deposit = future_value_annuity(deposit_monthly, monthly_rate, 120)  # 10년 = 120개월
        principal_deposit = deposit_monthly * 120
        interest_pre_tax = fv_deposit - principal_deposit
        tax = interest_pre_tax * 0.154
        interest_after_tax = interest_pre_tax - tax

        # --- 단기납 계산 ---
        total_insurance_paid = insurance_monthly * 12 * pay_years
        refund = total_insurance_paid * (return_rate / 100)
        bonus = refund - total_insurance_paid

        # --- KPI 비교 ---
        with tab_result:
            st.subheader("🔍 결과 분석")
            kpi_dep, kpi_ins = st.columns(2)
            with kpi_dep:
                st.metric("세후 이자 총합 (10년)", f"{interest_after_tax:,.0f}만원")
            with kpi_ins:
                delta_val = bonus - interest_after_tax
                delta_prefix = "+" if delta_val >= 0 else ""
                st.metric(
                    "단기납 보너스 총합 (10년)",
                    f"{bonus:,.0f}만원",
                    delta=f"{delta_prefix}{delta_val:,.0f}만원",
                    delta_color="normal" if delta_val >= 0 else "inverse",
                )

            #############################
            # 상세 요약
            #############################
            col_sum1, col_sum2 = st.columns(2)
            with col_sum1:
                st.markdown("### 📜 적금 요약")
                st.write(f"- 원금 합계: {format_currency_trim(principal_deposit)}")
                st.write(f"- 세전 이자: {format_currency_trim(interest_pre_tax)}")
                st.write(f"- 이자 과세 (15.4%): {format_currency_trim(tax)}")
                st.write(f"- 세후 이자: {format_currency_trim(interest_after_tax)}")
            with col_sum2:
                st.markdown("### 📜 단기납 요약")
                st.write(f"- 원금 합계 ({pay_years}년): {format_currency_trim(total_insurance_paid)}")
                st.write(f"- 10년 시점 해지환급금: {format_currency_trim(refund)}")
                st.write(f"- 보너스 금액: {format_currency_trim(bonus)}")
                st.write("- *10년 이후 해지 시 **비과세** 혜택 가능*")

            #############################
            # 맞춤 설득 멘트
            #############################
            st.markdown("---")
            st.markdown("### 💬 맞춤 설득 멘트")
            if bonus > interest_after_tax:
                st.success(
                    emphasize_box(
                        "적금으로는 10년 동안 세후 **{0:,.0f}만원**을 벌지만, 단기납을 선택하면 같은 기간 **{1:,.0f}만원**을 손에 쥘 수 있어요! (차이 {2:,.0f}만원)".format(
                            interest_after_tax, bonus, bonus - interest_after_tax
                        ),
                        bg="#fff9e6",
                        color="#663300",
                    ),
                    icon="📈",
                )
            else:
                st.info(
                    emphasize_box(
                        "이번 시나리오에서는 단기납보다 적금이 유리합니다. 이자율이나 환급률을 조정해 다른 가정을 테스트해보세요!",
                        bg="#e6f7ff",
                        color="#004d66",
                    ),
                    icon="🔍",
                )

            #############################
            # 참고 계산
            #############################
            st.markdown("---")
            st.markdown("### 📌 참고 계산")
            factor = ((1 + monthly_rate) ** 120 - 1) / monthly_rate if monthly_rate else 120
            monthly_required = (bonus) / (factor * (1 - 0.154))
            st.markdown(
                f"👉 보너스와 동일한 결과를 내려면, 적금 월 납입액을 **{monthly_required:,.0f}만원**으로 설정해야 합니다."
            )

    #############################
    # 3) 도움말 탭
    #############################
    with tab_help:
        st.markdown(
            """
            #### ℹ️ 계산 가정
            - **적금**: 매월 말 납입, 복리 이자, 이자 과세 15.4%.
            - **단기납**: 매월 말 납입, **비과세** 환급금.
            - 계산 결과는 가정에 따라 달라질 수 있으며, 실제 상품 약관을 반드시 확인하세요.
            ---
            #### 🔧 사용 팁
            1. *입력* 탭에서 슬라이더와 숫자 입력으로 시나리오를 빠르게 조정해보세요.
            2. *결과* 탭에서 KPI와 맞춤 멘트를 즉시 확인할 수 있습니다.
            3. 사이드바 인쇄 안내를 참고해 PDF 보고서로 내보낼 수 있어요.
            """
        )


if __name__ == "__main__":
    run()
