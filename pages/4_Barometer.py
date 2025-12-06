import streamlit as st
from openai import OpenAI

# ================================
#  TITULEK
# ================================
st.title("📊 Child Weight Risk Barometer")

# ================================
#  STYL
# ================================
st.markdown("""
<style>
    .main > div {
        max-width: 900px;
        margin: 0 auto;
        padding-top: 2rem;
    }

    /* rozumné mezery mezi otázkami */
    div[data-testid="stSelectbox"] {
        margin-top: 0 !important;
        margin-bottom: 12px !important;
    }

    div[data-baseweb="select"] {
        border-radius: 8px !important;
        background-color: #f8f9fb !important;
        border: 1px solid #e2e6ec !important;
        width: 100% !important;
        margin: 0;
    }

    div[data-baseweb="select"] div {
        font-size: 15px !important;
        color: #222 !important;
    }
</style>
""", unsafe_allow_html=True)


# ================================
# 2) USER OPTIONS – ŠKÁLY
# ================================

sex_options = {"Boy": 1, "Girl": 2}

soft_sweets_labels = [
    "1 – never",
    "2 – less than once per week",
    "3 – once per week",
    "4 – 2–4 times per week",
    "5 – 5–6 times per week",
    "6 – daily",
    "7 – more than once per day"
]

soft_drinks_labels = soft_sweets_labels
sweets_labels = soft_sweets_labels

vegetables_labels = [
    "1 – daily",
    "2 – 5–6 times per week",
    "3 – 2–4 times per week",
    "4 – once per week",
    "5 – less than once per week",
    "6 – rarely",
    "7 – never"
]

phys_labels = [
    "1 – 6–7 days",
    "2 – 5 days",
    "3 – 4 days",
    "4 – 3 days",
    "5 – 2 days",
    "6 – 1 day",
    "7 – 0 days"
]

breakfast_labels = [
    "1 – every day",
    "2 – 4 days",
    "3 – 3 days",
    "4 – 2 days",
    "5 – 1 day",
    "6 – less often",
    "7 – never"
]

tooth_labels = [
    "1 – twice per day or more",
    "2 – once per day",
    "3 – once per week",
    "4 – less often",
    "5 – never"
]

feellow_labels = [
    "1 – never",
    "2 – rarely",
    "3 – monthly",
    "4 – weekly",
    "5 – several times per week",
    "6 – almost daily",
    "7 – daily"
]

talkfather_labels = [
    "1 – very easy",
    "2 – easy",
    "3 – rather easy",
    "4 – rather difficult",
    "5 – difficult",
    "6 – very difficult",
    "7 – not in contact"
]


# ================================
# 3) BUILD VECTOR – pomocná funkce
# ================================
def extract_number(label: str) -> int:
    """Convert label like '1 – daily' → 1"""
    return int(label.split("–")[0].split("-")[0].strip())


# ================================
# 3b) BAROMETER SCORE – VÝPOČET
# ================================
def compute_risk_score(user_data: dict) -> int:
    """
    Returns lifestyle risk score 0–100.
    0 = very healthy habits, 100 = very unhealthy habits.
    """

    # All 1–7 scales: 1 = best, 7 = worst
    soft_drinks_risk = (user_data["SOFT_DRINKS"] - 1) / 6
    sweets_risk      = (user_data["SWEETS"] - 1) / 6
    vegetables_risk  = (user_data["VEGETABLES"] - 1) / 6
    phys_risk        = (user_data["PHYS_ACT_60"] - 1) / 6
    breakfast_risk   = (user_data["BREAKFAST_WEEKDAYS"] - 1) / 6
    feel_low_risk    = (user_data["FEEL_LOW"] - 1) / 6
    talk_father_risk = (user_data["TALK_FATHER"] - 1) / 6

    # Tooth brushing has 1–5 scale
    teeth_risk       = (user_data["TOOTH_BRUSHING"] - 1) / 4

    components = [
        soft_drinks_risk,
        sweets_risk,
        vegetables_risk,
        phys_risk,
        breakfast_risk,
        teeth_risk,
        feel_low_risk,
        talk_father_risk,
    ]

    base_score = sum(components) / len(components)   # 0–1
    score_0_100 = int(round(base_score * 100))

    return score_0_100


# ================================
# 4) UI – OTÁZKY VE DVOU SLOUPCÍCH
# ================================

# řádek 0 – gender / age
row0_col1, row0_col2 = st.columns(2)
with row0_col1:
    sex_label = st.selectbox("👦👧 Gender of your child", list(sex_options.keys()))
    sex = sex_options[sex_label]
with row0_col2:
    age = st.selectbox("🎂 Age of your child", list(range(10, 17)))

st.markdown("---")

# řádek 1 – soft drinks / sweets
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    soft_drinks = st.selectbox(
        "🥤 How many times a week does your child drink soft drinks?",
        soft_drinks_labels
    )
with row1_col2:
    sweets = st.selectbox(
        "🍬 How many times a week does your child eat sweets?",
        sweets_labels
    )

# řádek 2 – vegetables / physical activity
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    vegetables = st.selectbox(
        "🥦 How many times a week does your child eat vegetables?",
        vegetables_labels
    )
with row2_col2:
    phys = st.selectbox(
        "🏃‍♂️ On how many days per week is your child physically active for at least 60 minutes?",
        phys_labels
    )

# řádek 3 – feeling low / teeth
row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    feel_low = st.selectbox(
        "😔 How often does your child feel low or sad?",
        feellow_labels
    )
with row3_col2:
    teeth = st.selectbox(
        "🦷 How often does your child brush their teeth?",
        tooth_labels
    )

# řádek 4 – breakfast / talk to father
row4_col1, row4_col2 = st.columns(2)
with row4_col1:
    breakfast = st.selectbox(
        "🍽️ On how many schooldays does your child usually eat breakfast?",
        breakfast_labels
    )
with row4_col2:
    talk_father = st.selectbox(
        "👨‍👧 How easy is it for your child to talk to their father about their problems?",
        talkfather_labels
    )


# ================================
# 5) COMPUTE – BAROMETER + AI TIP
# ================================
if st.button("🔍 Evaluate"):
    user_data = {
        "SEX": sex,
        "AGE": age,
        "SOFT_DRINKS": extract_number(soft_drinks),
        "SWEETS": extract_number(sweets),
        "VEGETABLES": extract_number(vegetables),
        "PHYS_ACT_60": extract_number(phys),
        "BREAKFAST_WEEKDAYS": extract_number(breakfast),
        "TOOTH_BRUSHING": extract_number(teeth),
        "FEEL_LOW":_
    }