import streamlit as st
import urllib.parse

# تنظیمات حرفه‌ای V11
st.set_page_config(page_title="MacroSurgeon V11 Emperor", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    .stNumberInput input { color: #facc15 !important; font-size: 20px !important; }
    .yield-card { background: #111827; padding: 15px; border-radius: 10px; border-top: 4px solid #facc15; }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 مرکز فرماندهی V11: نسخه امپراتور")
st.write("تحلیل جامع ۲۰۲۶: منحنی بازدهی، بهره واقعی و تراز تجاری")

# --- گام ۱: استخراج داده‌های زنده ---
with st.expander("🔍 استخراج داده از Gemini (نسخه ارتقا یافته)", expanded=False):
    fetch_prompt = """
    لطفاً آمار دقیق می ۲۰۲۶ را استخراج کن:
    - Fed Rate | 2-Year Yield | 10-Year Yield
    - CPI & PPI Inflation | JOLTS Job Openings
    - Trade Balance | PMI Index
    فقط اعداد را لیست کن.
    """
    st.code(fetch_prompt)
    st.link_button("🚀 باز کردن Gemini", "https://gemini.google.com/app")

st.markdown("---")

# --- گام ۲: ورودی‌های جراحی ---
col1, col2, col3 = st.columns(3)

def dual_input(col, label, min_val, max_val, default_val, step, key):
    with col:
        v_num = st.number_input(label, value=default_val, step=step, key=f"n_{key}")
        v_slip = st.slider(f"تنظیم {label}", min_val, max_val, v_num, step, key=f"s_{key}")
        return v_slip

with col1:
    y2 = dual_input(col1, "بازدهی ۲ ساله (%)", 0.0, 7.0, 4.8, 0.05, "y2")
    y10 = dual_input(col1, "بازدهی ۱۰ ساله (%)", 0.0, 7.0, 4.2, 0.05, "y10")

with col2:
    cpi = dual_input(col2, "تورم CPI (%)", 0.0, 10.0, 3.0, 0.1, "cpi")
    ppi = dual_input(col2, "تورم PPI (%)", 0.0, 10.0, 3.5, 0.1, "ppi")

with col3:
    trade_bal = dual_input(col3, "تراز تجاری (B$)", -150.0, 50.0, -57.3, 0.5, "tb")
    jolts = dual_input(col3, "JOLTS (M)", 0.0, 15.0, 6.87, 0.1, "jolts")

# --- محاسبات استراتژیک V11 ---
yield_spread = y10 - y2
real_yield = y10 - cpi

st.markdown("---")
c_res1, c_res2, c_res3 = st.columns(3)

with c_res1:
    status = "🔴 وارونگی (خطر رکود)" if yield_spread < 0 else "🟢 عادی"
    st.metric("منحنی بازدهی (10Y-2Y)", f"{yield_spread:.2f}%", status)

with c_res2:
    st.metric("نرخ بهره واقعی", f"{real_yield:.2f}%", "جذاب برای طلا" if real_yield < 0 else "فشار بر طلا")

with c_res3:
    dxy_score = (y2 * 1.2) + (trade_bal / 20) + (jolts - 6)
    st.metric("شاخص قدرت دلار (DXY)", f"{dxy_score:.1f}")

# --- گام ۴: پرامپت نهایی ---
final_prompt = f"""
تحلیل امپراتور (V11):
- بازدهی ۲ ساله: {y2}% | ۱۰ ساله: {y10}% (تفاوت: {yield_spread:.2f}%)
- بهره واقعی: {real_yield:.2f}% | تورم تولید (PPI): {ppi}%
- تجارت: {trade_bal}B$ | اشتغال: {jolts}M
با توجه به وارونگی منحنی بازدهی و سطح بهره واقعی، استراتژی دقیق برای دلار و طلا در بازه ماه می ۲۰۲۶ چیست؟
"""
st.subheader("🤖 استراتژی نهایی Gemini")
st.text_area("کپی برای تحلیل نهایی:", final_prompt, height=150)
