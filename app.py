import streamlit as st
from datetime import datetime

# تنظیمات تم و صفحه برای موبایل
st.set_page_config(page_title="MacroSurgeon V7", page_icon="✂️", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700&display=swap');
    
    * {
        font-family: 'Vazirmatn', sans-serif !important;
    }
    
    .main { background-color: #0e1117; }
    .stSlider [data-baseweb="slider"] { margin-bottom: 25px; }
    .metric-card { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

st.title("✂️ جراحی بزرگ: داشبورد وارش")
st.write("تحلیل زنده بر اساس دکترین جدید اقتصادی ۲۰۲۶")

# --- بخش اول: تایمر استراتژیک ---
st.sidebar.header("⏳ شمارش معکوس جراحی")
next_meeting = datetime(2026, 5, 20)
days_left = (next_meeting - datetime.now()).days
st.sidebar.metric("روز تا جلسه فدرال رزرو", f"{days_left} روز")
st.sidebar.info("کوین وارش در ۱۵ می صندلی را تحویل می‌گیرد.")

# --- بخش دوم: ورودی‌های کلیدی ---
st.header("🩺 ورودی‌های زنده بازار")
col1, col2 = st.columns(2)

with col1:
    ir = st.slider("نرخ بهره فعلی (%)", 0.0, 10.0, 3.75)
    inf = st.slider("تورم مصرف‌کننده CPI (%)", 0.0, 15.0, 3.0)
    ppi = st.slider("تورم تولیدکننده PPI (%)", 0.0, 15.0, 3.5)
    fed_tone = st.radio("لحن فدرال رزرو:", ["شاهین (تند) 🦅", "کبوتر (نرم) 🕊️"])

with col2:
    pmi = st.slider("شاخص مدیران خرید PMI", 30, 70, 48)
    unemp = st.slider("نرخ بیکاری (%)", 2.0, 10.0, 4.2)
    m2 = st.slider("رشد نقدینگی M2 (%)", -5.0, 15.0, 2.0)
    war_risk = st.select_slider("ریسک ژئوپلیتیک", options=["صلح", "تنش", "بحران"])

st.markdown("---")
st.subheader("📉 وضعیت بازار اوراق")
yield_2y = st.number_input("بازده اوراق ۲ ساله (%)", value=4.10, step=0.05)
yield_10y = st.number_input("بازده اوراق ۱۰ ساله (%)", value=3.90, step=0.05)
yield_spread = yield_10y - yield_2y

if yield_spread < 0:
    st.warning(f"⚠️ وارونگی منحنی بازدهی ({yield_spread:.2f}%): سیگنال کلاسیک رکود و فشار برای کاهش نرخ بهره!")

# --- بخش سوم: تحلیل هوشمند ---
st.markdown("---")
st.header("🧪 خروجی تحلیل و احتمال")

# منطق محاسبه با در نظر گرفتن اسپرد اوراق
prob_score = (unemp * 10) + (50 - pmi) + (5 if fed_tone == "کبوتر (نرم) 🕊️" else -10)
if yield_spread < 0: prob_score += 15 # وارونگی احتمال کات را بالا می‌برد

prob_final = min(max(prob_score, 0), 100)

st.subheader(f"احتمال کاهش نرخ در جلسه آینده: {prob_final:.1f}%")
st.progress(int(prob_final)) # استفاده از int برای جلوگیری از خطا

# تحلیل دارایی‌ها
dxy_score = (ir * 2) + (5 if fed_tone == "شاهین (تند) 🦅" else -5) - (prob_final * 0.2)
gold_score = (inf * 2) + (5 if war_risk == "بحران" else -10) - (ir * 3) + (prob_final * 0.1)
crypto_score = (m2 * 3) + (prob_final * 0.2) - (ir * 2) # تاثیر مستقیم M2 و کاهش نرخ روی کریپتو

col_a, col_b, col_c = st.columns(3)
with col_a:
    if dxy_score > 5: st.success("💵 دلار: صعودی")
    else: st.error("💵 دلار: تحت فشار")

with col_b:
    if gold_score > 5: st.success("🟡 طلا: صعودی / امن")
    else: st.error("🟡 طلا: اصلاحی")

with col_c:
    if crypto_score > 5: st.success("₿ بیت‌کوین/کریپتو: صعودی (تزریق نقدینگی)")
    else: st.error("₿ کریپتو: نزولی (کمبود نقدینگی)")

# تاثیر ریسک جنگ بر تورم
if war_risk == "بحران":
    st.info("🛢️ توجه: ریسک ژئوپلیتیک بالا می‌تواند باعث شوک انرژی شده و CPI را مجدداً بالا ببرد. این موضوع دست فدرال رزرو را برای کاهش نرخ بهره می‌بندد.")

# --- بخش چهارم: گزارش تشریحی ---
st.markdown("---")
with st.expander("📝 مشاهده گزارش کالبدشکافی"):
    report = f"""
    * **تحلیل PPI vs CPI:** شکاف {ppi - inf:.1f} درصدی نشان می‌دهد که هزینه‌های تولید هنوز کاملاً به مصرف‌کننده منتقل نشده است.
    * **تحلیل PMI و اشتغال:** عدد {pmi} در کنار بیکاری {unemp}% نشان‌دهنده {'رکود صنعتی' if pmi < 50 else 'رونق صنعتی'} است.
    * **جریان نقدینگی (M2):** رشد {m2}% نقدینگی {'محرک بازارهای ریسکی مانند سهام و کریپتو' if m2 > 0 else 'موجب خشکی نقدینگی در بازارها'} است.
    * **استراتژی وارش:** با توجه به احتمال {prob_final:.1f}% کاهش نرخ، بازار در حال قیمت‌گذاری مجدد دارایی‌هاست.
    """
    st.write(report)
