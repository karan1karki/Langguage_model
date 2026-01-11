import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

NEPAL_LANGUAGES = [
    "English","Nepali", "Maithili", "Bhojpuri", "Tharu", "Tamang", "Bajjika", "Awadhi", "Nepal Bhasha (Newar)",
    "Magar Dhut", "Doteli", "Urdu", "Yakthung/Limbu", "Gurung", "Magahi", "Baitadeli", "Rai", "Achhami",
    "Bantawa", "Rajbanshi", "Sherpa", "Khash", "Bajhangi", "Hindi", "Magar Kham", "Chamling", "Ranatharu",
    "Chepang", "Bajureli", "Santali", "Danuwar", "Darchuleli", "Uranw/Urau", "Kulung", "Angika", "Majhi",
    "Sunuwar", "Thami", "Ganagai", "Thulung", "Bangla", "Ghale", "Sampang", "Marwadi", "Dadeldhuri",
    "Dhimal", "Tajpuriya", "Kumal", "Khaling", "Musalman", "Wambule", "Bahing/Bayung", "Yakkha",
    "Sanskrit", "Bhujel", "Bhote", "Darai", "Yamphu/Yamphe", "Nachhiring", "Hyolmo/Yholmo", "Dumi",
    "Jumli", "Bote", "Mewahang", "Puma", "Pahari", "Athpahariya", "Dungmali", "Jirel", "Tibetan",
    "Dailekhi", "Chum/Nubri", "Chhantyal", "Raji", "Thakali", "Meche", "Koyee", "Lohorung", "Kewarat",
    "Dolpali", "Done", "Mugali", "Jero/Jerung", "Karmarong", "Chhintang", "Lhopa", "Lapcha",
    "Munda/Mudiyari", "Manange", "Chhiling", "Dura", "Tilung", "Sign Language", "Byansi", "Balkura/Baram",
    "Baragunwa", "Sadri", "English", "Magar Kaike", "Sonaha", "Hayu/Vayu", "Kisan", "Punjabi", "Dhuleli",
    "Khamchi(Raute)", "Lungkhim", "Lowa", "Kagate", "Waling/Walung", "Nar-Phu", "Lhomi", "Tichhurong Poike",
    "Kurmali", "Koche", "Sindhi", "Phangduwali", "Belhare", "Surel"
]

# --- Connection & Data Loading (same as before) ---
conn = st.connection("gsheets", type=GSheetsConnection)
WORKSHEET = "Translations"

@st.cache_data(ttl=60)
def load_data():
    df = conn.read(worksheet=WORKSHEET, ttl=0)
    if df.empty and len(df.columns) == 0:
        initial_columns = ["Nepali"] + [lang for lang in NEPAL_LANGUAGES if lang != "Nepali"]
        df = pd.DataFrame(columns=initial_columns)
        dummy_row = pd.DataFrame([[""] * len(initial_columns)], columns=initial_columns)
        df_with_dummy = pd.concat([df, dummy_row], ignore_index=True)
        conn.update(worksheet=WORKSHEET, data=df_with_dummy)
        df = conn.read(worksheet=WORKSHEET, ttl=0)
    
    return df

df = load_data()
languages = list(df.columns)

# --- Dashboard Page ---
st.title("📊 Dashboard")
st.write("Quick translation tool for Nepal's languages")

# Translation widget
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From Language", languages, key="dash_source")
with col2:
    target_lang = st.selectbox("To Language", languages, key="dash_target")

input_text = st.text_input("Enter word or phrase", key="dash_input")

if st.button("Translate", type="primary"):
    if source_lang == target_lang:
        st.success(f"Same language → {input_text}")
    else:
        words = input_text.lower().split()  # simple normalization
        translated = []
        for word in words:
            match = df[df[source_lang].str.lower() == word]
            if not match.empty:
                trans = match[target_lang].values[0]
                translated.append(trans if pd.notna(trans) else f"[{word} - missing]")
            else:
                translated.append(f"[{word} - not found]")
        st.markdown("**Translation:** " + " ".join(translated))

# Quick stats
st.subheader("Data Overview")
st.info(f"Currently supporting **{len(languages)}** languages")
st.info(f"**{len(df)}** words/phrases in database")

st.dataframe(df.head(10), use_container_width=True)