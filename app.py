import streamlit as st
from datetime import datetime
import urllib.parse

# تنظیمات صفحه برای موبایل
st.set_page_config(page_title="MacroSurgeon V9", page_icon="🏦", layout="centered")

st.markdown("""
    <style>
    .stNumberInput div div input { font-weight: bold; color: #38bdf8; }
    .metric-container { background-color: #1e2130; padding: 15px; border-radius: 12px; border-left: 5px solid #38bdf8; }
    .stSlider [data-baseweb="slider"] { margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✂️ جراحی کلان V9: نسخه فول استراتژیک")
st.write("تحلیل جامع ۲۰۲۶: از JOLTS تا تراز تجاری و بازسازی")

# --- بخش ورودی‌ها ---
st.header("🩺 علائم حیاتی (داده‌های دقیق)")

def sync_input(label, min_val, max_val, default_val, step, help_text=""):
    col_s, col_t = st.columns([2, 1])
    with col_t:
        val_text = st.number_input(f"عدد {label}", value=default_val, step=step, key=f"t_{label}", help=help_text)
    with col_s:
        val_slider = st.slider(f"تغییر {label}", min_val, max_val, val_text, step, key=f"s_{label}")
    return val_slider

# ورودی‌های اصلی
ir = sync_input("نرخ بهره (%)", 0.0, 10.0, 3.75, 0.25)
cpi = sync_input("تورم CPI (%)", 0.0, 15.0, 3.0, 0.1)
ppi = sync_input("تورم PPI (%)", 0.0, 15.0, 3.5, 0.1)

# اضافه شدن تراز تجاری (Trade Balance)
# عدد منفی نشان دهنده کسری تجاری (Deficit) است که برای آمریکا معمول است.
trade_bal = sync_input("تراز تجاری (میلیارد دلار)", -150.0, 50.0, -57.3, 0.1, "مثبت یعنی مازاد، منفی یعنی کسری تجاری")

jolts = sync_input("JOLTS (میلیون شغل)", 0.0, 15.0, 6.87, 0.01)
pmi = sync_input("شاخص PMI", 30.0, 70.0, 48.0, 0.5)

st.markdown("---")
fed_tone = st.radio("لحن فدرال رزرو (وارش/پاول):", ["شاهین (Hawkish) 🦅", "کبوتر (Doveish) 🕊️"])
geo_risk = st.select_slider("ریسک ژئوپلیتیک و ناتو", options=["ثبات/صلح", "تنش محدود", "بحران/جنگ"])

# --- محاسبات منطقی ارتقا یافته ---
st.markdown("---")
st.header("📊 خروجی جراحی (پتانسیل بازار)")

# منطق دلار: بهره بالا + تراز تجاری رو به بهبود + JOLTS بالا = دلار پادشاه
dxy_logic = (ir * 2) + (5 if fed_tone == "شاهین (Hawkish) 🦅" else -5) + (jolts - 6) + (trade_bal / 20)
# منطق طلا: تورم بالا + ریسک جنگ - بهره بالا - تراز تجاری قوی (دلار قوی)
gold_logic = (cpi * 2) + (10 if geo_risk == "بحران/جنگ" else -10) - (ir * 2.5) - (trade_bal / 20)

c1, c2 = st.columns(2)
with c1:
    st.metric("پتانسیل دلار (DXY)", f"{dxy_logic:.1f}", delta="تقویت صادرات" if trade_bal > -55 else "ضعف تجاری", delta_color="normal")
with c2:
    st.metric("پتانسیل طلا (XAU)", f"{gold_logic:.1f}", delta="ریزش به ۳۱۰۰" if gold_logic < 0 else "حمایت موقت")

# --- بخش هوش مصنوعی (Gemini Center) ---
st.markdown("---")
st.header("🤖 مرکز تحلیل هوشمند Gemini")

gemini_prompt = f"""
تحلیل کلان برای ترید در می ۲۰۲۶:
داده‌ها:
- نرخ بهره: {ir}% | تورم (CPI): {cpi}% | تورم تولید (PPI): {ppi}%
- تراز تجاری آمریکا: {trade_bal} میلیارد دلار (Trade Balance)
- بازار کار (JOLTS): {jolts} میلیون شغل
- شاخص تولید (PMI): {pmi} | لحن فدرال رزرو: {fed_tone}
- ریسک ژئوپلیتیک: {geo_risk}

سوالات تخصصی برای تحلیل:
۱. با توجه به تراز تجاری {trade_bal} میلیارد دلاری، آیا تقاضای فیزیکی برای دلار جهت بازسازی و صادرات تسلیحات ناتو تأمین می‌شود؟
۲. آیا عدد {jolts} میلیونی JOLTS به کوین وارش اجازه جراحی و کاهش نرخ را می‌دهد یا او را در موضع شاهین نگه می‌دارد؟
۳. روند انس طلا با توجه به فشار دلار و کاهش هزینه‌های ناتو به سمت ۳۱۰۰ دلار است یا خیر؟
"""

st.text_area("پرومپت آماده (کپی کن):", gemini_prompt, height=250)

if st.button("🚀 انتقال به Gemini"):
    encoded_prompt = urllib.parse.quote(gemini_prompt)
    # لینک مستقیم به اپلیکیشن جمینای
    st.markdown(f'<a href="https://gemini.google.com/app" target="_blank">۱. اینجا کلیک کن و در جمینای Paste کن</a>', unsafe_allow_html=True)

st.info(f"💡 تحلیل جراح: تراز تجاری فعلی تو ({trade_bal}) نشان می‌دهد که آمریکا {'هنوز در حال خروج نقدینگی است' if trade_bal < -60 else 'در حال بهبود وضعیت صادرات است'}. بهبود این عدد مستقیماً قیمت طلا را سرکوب می‌کند.")
