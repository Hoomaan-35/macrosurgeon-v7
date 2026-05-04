import streamlit as st
import urllib.parse

# --- تنظیمات صفحه ---
st.set_page_config(page_title="MacroSurgeon V12 Ultimate", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    .stNumberInput input { color: #10b981 !important; font-size: 18px !important; font-weight: bold; }
    .stNumberInput label { font-size: 14px !important; color: #e2e8f0; }
    .metric-box { background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #38bdf8; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 مرکز فرماندهی V12: نسخه نهایی (Ultimate)")
st.write("بدون اسلایدر - فقط ورودی‌های دقیق عددی برای معامله‌گران حرفه‌ای")

# --- گام ۱: دریافت داده‌ها از جمینای ---
with st.expander("🔍 استخراج داده‌های زنده از Gemini", expanded=False):
    fetch_prompt = """
    لطفاً جدیدترین آمارهای اقتصادی آمریکا (منتشر شده در ماه جاری) را جستجو کن و فقط اعداد را لیست کن:
    1. Fed Rate
    2. 2-Year Treasury Yield
    3. 10-Year Treasury Yield
    4. Inflation Rate (CPI)
    5. PPI (Producer Price Index)
    6. JOLTS Job Openings
    7. Initial Jobless Claims (مدعیان بیکاری به هزار نفر)
    8. Trade Balance (تراز تجاری به میلیارد دلار)
    9. PMI (Manufacturing Index)
    """
    st.code(fetch_prompt, language="text")
    st.link_button("🚀 کپی و باز کردن Gemini برای دریافت داده‌ها", "https://gemini.google.com/app")

st.markdown("---")
st.header("🩺 گام ۲: ورود داده‌های اقتصادی")

# ستون‌بندی برای ورودی‌ها (۳ ستون)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("سیاست پولی و اوراق")
    ir = st.number_input("نرخ بهره فدرال (Fed Rate %)", value=3.75, step=0.25)
    y2 = st.number_input("بازدهی ۲ ساله (2Y Yield %)", value=4.80, step=0.05)
    y10 = st.number_input("بازدهی ۱۰ ساله (10Y Yield %)", value=4.20, step=0.05)

with col2:
    st.subheader("تورم و صنعت")
    cpi = st.number_input("نرخ تورم (Inflation Rate / CPI %)", value=3.0, step=0.1)
    ppi = st.number_input("تورم تولیدکننده (PPI %)", value=3.5, step=0.1)
    pmi = st.number_input("شاخص تولید (PMI)", value=48.0, step=0.5, help="بالای 50 یعنی رونق، زیر 50 یعنی رکود صنعتی")

with col3:
    st.subheader("بازار کار و تجارت")
    jolts = st.number_input("فرصت‌های شغلی (JOLTS میلیون)", value=6.87, step=0.05)
    unemp_claims = st.number_input("مدعیان بیکاری (هزار نفر)", value=215.0, step=1.0, help="معمولا بین 200 تا 300 هزار است")
    trade_bal = st.number_input("تراز تجاری (B$ میلیارد دلار)", value=-57.3, step=0.5)

# --- گام ۳: محاسبات و خروجی استراتژیک ---
st.markdown("---")
st.header("📊 گام ۳: داشبورد جراحی کلان")

# محاسبات کلیدی
yield_spread = y10 - y2  # منحنی بازدهی
real_yield = y10 - cpi   # بهره واقعی

c_res1, c_res2, c_res3, c_res4 = st.columns(4)

with c_res1:
    status_curve = "🔴 وارونگی (رکود)" if yield_spread < 0 else "🟢 عادی"
    st.metric("منحنی بازدهی (10Y-2Y)", f"{yield_spread:.2f}%", status_curve, delta_color="off")

with c_res2:
    status_real = "🟢 قاتل طلا" if real_yield > 0 else "🔴 جذاب برای طلا"
    st.metric("بهره واقعی (Real Yield)", f"{real_yield:.2f}%", status_real, delta_color="off")

with c_res3:
    status_margin = "🔴 فشار روی بورس" if ppi > cpi else "🟢 سودآوری امن"
    st.metric("حاشیه سود شرکت‌ها", f"PPI vs CPI", status_margin, delta_color="off")

with c_res4:
    labor_health = "🔴 شکننده" if (jolts < 6.0 or unemp_claims > 250) else "🟢 قدرتمند (شاهین)"
    st.metric("وضعیت بازار کار", f"{unemp_claims}k مدعی", labor_health, delta_color="off")

# --- گام ۴: پرامپت نهایی تحلیل‌گر هوش مصنوعی ---
st.markdown("---")
st.header("🤖 گام ۴: دریافت استراتژی نهایی از جمینای")

final_prompt = f"""
من یک تریدر هستم. لطفاً با توجه به این داده‌های قطعی (V12) بازار را تحلیل کن:
- سیاست پولی: نرخ بهره {ir}% | اوراق ۲ ساله: {y2}% | اوراق ۱۰ ساله: {y10}%
- تورم: تورم مصرف‌کننده (CPI) {cpi}% | تورم تولید (PPI) {ppi}%
- صنعت و تجارت: شاخص تولید (PMI) {pmi} | تراز تجاری {trade_bal} میلیارد دلار
- بازار کار: فرصت‌های شغلی (JOLTS) {jolts} میلیون | مدعیان بیکاری {unemp_claims} هزار نفر

با توجه به فاصله بازدهی (Yield Curve) که {yield_spread:.2f}% است و بهره واقعی {real_yield:.2f}%:
۱. وضعیت رکود یا رشد اقتصاد آمریکا چگونه است؟
۲. بهترین استراتژی برای معامله روی شاخص دلار (DXY) و طلای جهانی چیست؟
۳. آیا فدرال رزرو با این داده‌های بازار کار و تورم، توانایی کاهش نرخ بهره را دارد؟
"""
st.text_area("این متن بر اساس اعداد شما ساخته شده. کپی کنید و به جمینای بدهید:", final_prompt, height=250)
