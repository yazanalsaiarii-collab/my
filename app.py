import streamlit as st
import pandas as pd
import random
import time

# 1. إعدادات الصفحة والـ Theme الاحترافي
st.set_page_config(
    page_title="برنامج الأبطال الخارقين للتحفيز",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة المستخدم بألوان مبهجة ومناسبة للأطفال
st.markdown("""
    <style>
    .main { background-color: #f7f9fc; }
    h1 { color: #2E4057; font-family: 'Cairo', sans-serif; text-align: center; }
    h2 { color: #048A81; }
    .stButton>button { background-color: #048A81; color: white; border-radius: 12px; font-size: 18px; width: 100%; }
    .stButton>button:hover { background-color: #06B4A6; color: white; }
    .wheel-box { background-color: #F4D35E; padding: 20px; border-radius: 15px; text-align: center; border: 3px dashed #EE964B; }
    </style>
""", unsafe_allow_html=True)

st.title("🏆 برنامج تحدي الأسبوعين للأبطال الخمسة 🏆")
st.write("---")

# 2. إدارة البيانات في الذاكرة (Session State) للحفاظ على النقاط والبنود
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    # نظام الـ 5 أشخاص الثابت
    st.session_state.players = {
        "البطل 1": 0,
        "البطل 2": 0,
        "البطل 3": 0,
        "البطل 4": 0,
        "البطل 5": 0
    }
    # البنود الافتراضية السهلة التعديل
    st.session_state.tasks = {
        "🕋 الصلوات الخمس في وقتها": 50,
        "📖 قراءة ورد من القرآن الكريم": 100,
        "🛏️ ترتيب الغرفة والسرير صباحاً": 30,
        "🤝 مساعدة الأهل والبر بهم": 40,
        "📚 حل الواجبات المدرسية أو القراءة": 50
    }
    # مكافآت عجلة الحظ
    st.session_state.wheel_rewards = [
        "🎁 هدية مفاجأة مميزة!", 
        "🍦 مشوار لأقرب محل آيسكريم", 
        "🎮 1 ساعة إضافية ألعاب إلكترونية", 
        "💵 مكافأة مالية تشجيعية", 
        "🍿 سهرة فيلم مع الفشار ونوم متأخر",
        "🎈 بطاقة إعفاء من مهمة منزلية ليوم واحد"
    ]

# 3. لوحة التحكم الجانبية (تعديل البنود والأسماء بكل سهولة)
st.sidebar.header("⚙️ لوحة التحكم السريعة")

# تعديل أسماء الأبطال الخمسة بسهولة
st.sidebar.subheader("👤 تعديل أسماء الأبطال")
updated_players = {}
for i, (current_name, current_points) in enumerate(st.session_state.players.items(), 1):
    new_name = st.sidebar.text_input(f"اسم البطل {i}: ", value=current_name, key=f"p_{i}")
    updated_players[new_name] = current_points
st.session_state.players = updated_players

st.sidebar.write("---")

# إدارة وتعديل البنود من داخل البرنامج
st.sidebar.subheader("📝 إدارة بند جديد")
with st.sidebar.form("add_task_form", clear_on_submit=True):
    new_task_name = st.text_input("اسم المهمة/البند الجديد:")
    new_task_points = st.number_input("نقاط البند:", min_value=10, max_value=500, value=50, step=10)
    submitted = st.form_submit_button("➕ حفظ البند الجديد")
    if submitted and new_task_name:
        st.session_state.tasks[new_task_name] = new_task_points
        st.sidebar.success(f"تمت إضافة: {new_task_name}")

# عرض وحذف البنود الحالية لتسهيل التحكم
st.sidebar.subheader("🗑️ البنود الحالية (يمكنك حذف ما تريد)")
tasks_to_delete = []
for task in list(st.session_state.tasks.keys()):
    if st.sidebar.button(f"❌ {task} ({st.session_state.tasks[task]} ن)", key=f"del_{task}"):
        del st.session_state.tasks[task]
        st.rerun()

# 4. واجهة تسجيل الإنجازات اليومية
st.header("🎯 رصد الإنجازات اليومية")
col1, col2 = st.columns(2)

with col1:
    child_selected = st.selectbox("من البطل الذي أنجز؟", list(st.session_state.players.keys()))

with col2:
    task_selected = st.selectbox("ما هي المهمة التي قام بها؟", list(st.session_state.tasks.keys()))

task_points = st.session_state.tasks[task_selected]

if st.button(f"✨ إضافة {task_points} نقطة لـ {child_selected}"):
    st.session_state.players[child_selected] += task_points
    st.balloons()
    st.success(f"كفو يا بطل! تم إضافة {task_points} نقطة لـ {child_selected}")

st.write("---")

# 5. لوحة الصدارة ومتابعة تحدي الأسبوعين
st.header("📊 لوحة الصدارة (تحدي الـ 14 يوماً)")

df = pd.DataFrame(list(st.session_state.players.items()), columns=["البطل", "مجموع النقاط"])
df = df.sort_values(by="مجموع النقاط", ascending=False).reset_index(drop=True)

# عرض شريط تقدم رقمي وتفاعلي لكل طفل
for index, row in df.iterrows():
    progress_percentage = min(row['مجموع النقاط'] / 1000, 1.0)
    
    # تحديد مرتبة البطل التعبيرية
    rank_emoji = "🥇" if index == 0 else "🥈" if index == 1 else "🥉" if index == 2 else "🏃‍♂️"
    
    st.subheader(f"{rank_emoji} {row['البطل']} — {row['مجموع النقاط']} / 1000 نقطة")
    st.progress(progress_percentage)

st.write("---")

# 6. نظام "عجلة الحظ التفاعلية" عند الوصول لـ 1000 نقطة
st.header("🎡 عجلة الحظ والمكافآت الخارقة")
st.write("🔓 تفتح هذه العجلة تلقائياً وبشكل حصري للأبطال الذين كسروا حاجز الـ **1000 نقطة**!")

# فحص الأبطال المؤهلين للعجلة
qualified_players = [player for player, score in st.session_state.players.items() if score >= 1000]

if qualified_players:
    player_for_wheel = st.selectbox("اختر البطل المؤهل ليدير العجلة:", qualified_players)
    
    st.markdown("<div class='wheel-box'>", unsafe_allow_html=True)
    st.write(f"🎉 البطل **{player_for_wheel}** يمتلك الرصيد الكافي الآن للَف العجلة!")
    
    if st.button("🚀 لَف عجلة الحظ الآن! 🎡"):
        # محاكاة تأثير حركة دوران العجلة الحماسية للأطفال
        with st.spinner("⏳ العجلة تدور وتدور وتدور..."):
            time.sleep(2)  # توقف درامي خفيف للحماس
            reward = random.choice(st.session_state.wheel_rewards)
            
        st.markdown(f"### 🤩 مبروووك! النتيجة هي:")
        st.success(f"🏆 {reward} 🏆")
        st.snow() # تأثير ثلجي احتفالي بالجائزة
        
        # خصم الـ 1000 نقطة مقابل السحبة ليتمكن من تجميعها مجدداً
        st.session_state.players[player_for_wheel] -= 1000
        st.info("ℹ️ تم استهلاك 1000 نقطة مقابل هذه اللفة، ويمكنه التجميع مرة أخرى!")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("🔒 لا يوجد أي بطل وصل إلى 1000 نقطة حتى الآن. استمروا في جمع النقاط لفتح العجلة!")
