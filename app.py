import streamlit as st
import pandas as pd
import time
from fpdf import FPDF
from io import BytesIO
import os

# 페이지 설정
st.set_page_config(page_title="적금 vs 단기납 비교", layout="wide")

# 강조 박스 함수
def emphasize_box(text, bg="#e6f2ff", color="#003366"):
    return f"""<div style='background-color:{bg}; color:{color}; padding:12px; border-radius:10px;
                font-size:20px; font-weight:bold; margin-bottom:10px;'>
                {text}
             </div>"""

# PDF 저장 함수
def generate_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()

    # ✅ 한글 폰트 등록
    font_path = os.path.join("fonts", "NanumGothic.ttf")
    pdf.add_font("Nanum", "", font_path, uni=True)
    pdf.set_font("Nanum", size=12)

    for line in summary_text.strip().split("\n"):
        pdf.cell(0, 10, line, ln=True)
    pdf_bytes = pdf.output(dest='S').encode('utf-8')
    return BytesIO(pdf_bytes)

# 타이틀
st.title("\ud83d\udcb0 \uc801\uae08 vs \ub2e8\uae30\ub0a9 \ube44\uad50 \ubc30\uacbd \ub3c4\uad6c")

# \uc785\ub825 \ucee8\ub7fc
col1, col2 = st.columns(2)

with col1:
    st.header("\ud83d\udccc \uc801\uae08")
    deposit_monthly = st.number_input("\uc6d4 \ub0a9\uc785\uc561 (\ub9cc\uc6d0)", min_value=0.0, step=1.0, value=None, placeholder="\uc608: 100")
    deposit_rate = st.number_input("\uc5f0 \uc774\uc790\uc728 (%)", min_value=0.0, step=0.1, value=None, placeholder="\uc608: 2.5")

with col2:
    st.header("\ud83d\udccc \ub2e8\uae30\ub0a9")
    insurance_monthly = st.number_input("\uc6d4 \ub0a9\uc785\uc561 (\ub9cc\uc6d0)", min_value=0.0, step=1.0, value=None, placeholder="\uc608: 100", key="ins_monthly")
    return_rate = st.number_input("10\ub144 \uc2dc\uc810 \ud574\uc9c0\ud655\uae08\ub960 (%)", min_value=0.0, step=0.1, value=None, placeholder="\uc608: 150.0")

# \uacb0\uacfc \ubcf4\uae30 \ubc84\ud2bc
if st.button("\uacb0\uacfc \ubcf4\uae30"):
    if deposit_monthly in (None, 0.0) or deposit_rate in (None, 0.0) or insurance_monthly in (None, 0.0) or return_rate in (None, 0.0):
        st.warning("\u26a0\ufe0f \ubaa8\ub4e0 \ud56d\ubaa9\uc5d0 \uac12\uc744 \uc785\ub825\ud574\uc8fc\uc138\uc694.")
    else:
        with st.spinner("\uacb0\uacfc\ub97c \ubd84\uc11d\ud558\ub294 \uc911\uc785\ub2c8\ub2e4..."):
            time.sleep(1.2)

        st.markdown("---")
        st.subheader("\ud83d\udd0d \uacb0\uacfc \ubd84\uc11d")

        # \uacc4\uc0b0
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

        # \uc694\uc57d \ucd9c\ub825
        sum1, sum2 = st.columns(2)

        with sum1:
            st.markdown("### \ud83e\uddfe \uc801\uae08 \uacc4\uc0b0 \uc694\uc57d")
            st.write(f"- \uc6d0\uae08 \ud569\uacc4 (1\ub144): {total_deposit:,.0f}\ub9cc\uc6d0")
            st.write(f"- \uc138\uc804 \uc774\uc790: {pre_tax_interest:,.0f}\ub9cc\uc6d0")
            st.write(f"- \uc774\uc790 \uacfc\uc138 (15.4%): {tax:,.0f}\ub9cc\uc6d0")
            st.write(f"- \uc138\ud6c4 \uc774\uc790: {after_tax_interest:,.0f}\ub9cc\uc6d0")
            st.markdown(emphasize_box(f"\uc138\ud6c4 \uc774\uc790 \uc6d4 \ud3c9\uaddc: {monthly_avg_interest:,.2f}\ub9cc\uc6d0", bg="#e6f2ff", color="#003366"), unsafe_allow_html=True)

        with sum2:
            st.markdown("### \ud83e\uddfe \ub2e8\uae30\ub0a9 \uacc4\uc0b0 \uc694\uc57d")
            st.write(f"- \uc6d0\uae08 \ud569\uacc4 (5\ub144): {total_insurance:,.0f}\ub9cc\uc6d0")
            st.write(f"- 10\ub144 \uc2dc\uc810 \ud574\uc9c0\ud655\uae08\uae08: {refund:,.0f}\ub9cc\uc6d0")
            st.write(f"- \ubcf4\ub108\uc2a4 \uae08\uc561: {bonus:,.0f}\ub9cc\uc6d0")
            st.markdown(emphasize_box(f"\ubcf4\ub108\uc2a4 \uc6d4 \ud3c9\uaddc: {monthly_bonus:,.2f}\ub9cc\uc6d0", bg="#fff3e6", color="#663300"), unsafe_allow_html=True)

        # \ud574\uc57c\ud560 \uac83: \ud574\uc678 PDF\ub85c \uc800\uc7a5
        st.markdown("### \u2705 \ud574\uc57c \ud560 \uac83")
        colm1, colm2 = st.columns(2)
        with colm1:
            st.metric("\uc138\ud6c4 \uc774\uc790 \ucd1d\ud569 (10\ub144 \uae30\uc900)", f"{total_after_tax_interest_10y:,.0f}\ub9cc\uc6d0")
        with colm2:
            st.metric("\ubcf4\ub108\uc2a4 \ucd1d\ud569 (\ub2e8\uae30\ub0a9 \uae30\uc900)", f"{bonus:,.0f}\ub9cc\uc6d0", delta=f"{bonus - total_after_tax_interest_10y:,.0f}\ub9cc\uc6d0")

        # PDF \uc0dd\uc131 \ubc84\ud2bc
        st.markdown("---")
        summary_text = f"""
\ud83d\udccc \uc801\uae08
- \uc6d0\uae08 \ud569\uacc4 (1\ub144): {total_deposit:,.0f}\ub9cc\uc6d0
- \uc138\uc804 \uc774\uc790: {pre_tax_interest:,.0f}\ub9cc\uc6d0
- \uc774\uc790 \uacfc\uc138 (15.4%): {tax:,.0f}\ub9cc\uc6d0
- \uc138\ud6c4 \uc774\uc790: {after_tax_interest:,.0f}\ub9cc\uc6d0
- \uc138\ud6c4 \uc774\uc790 \uc6d4 \ud3c9\uaddc: {monthly_avg_interest:,.2f}\ub9cc\uc6d0

\ud83d\udccc \ub2e8\uae30\ub0a9
- \uc6d0\uae08 \ud569\uacc4 (5\ub144): {total_insurance:,.0f}\ub9cc\uc6d0
- 10\ub144 \uc2dc\uc810 \ud574\uc9c0\ud655\uae08\uae08: {refund:,.0f}\ub9cc\uc6d0
- \ubcf4\ub108\uc2a4 \uae08\uc561: {bonus:,.0f}\ub9cc\uc6d0
- \ubcf4\ub108\uc2a4 \uc6d4 \ud3c9\uaddc: {monthly_bonus:,.2f}\ub9cc\uc6d0

\u2705 \ud574\uc57c \ud560 \uac83
- \uc138\ud6c4 \uc774\uc790 \ucd1d\ud569 (10\ub144 \uae30\uc900): {total_after_tax_interest_10y:,.0f}\ub9cc\uc6d0
- \ubcf4\ub108\uc2a4 \ucd1d\ud569 (\ub2e8\uae30\ub0a9 \uae30\uc900): {bonus:,.0f}\ub9cc\uc6d0
"""
        pdf_file = generate_pdf(summary_text)
        st.download_button("\ud83d\udcc5 PDF \ub2e4\uc6b4\ub85c\ub4dc", data=pdf_file, file_name="\uacb0\uacfc_\uc694\uc57d.pdf", mime="application/pdf")