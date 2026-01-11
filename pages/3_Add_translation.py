import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
WORKSHEET = "Translations"
df = conn.read(worksheet=WORKSHEET, ttl=0)

st.title("➕ Add New Languages Name")

with st.form("add_translation_form"):
    new_nepali = st.text_input("Nepali Word/Phrase*", help="This is the base entry")

    st.markdown("**Translations** (at least one recommended)")

    # Dynamic input fields for each language (excluding Nepali)
    translations = {}
    cols = st.columns(3)  # better layout for many languages
    for i, lang in enumerate([l for l in df.columns if l != "Nepali"]):
        with cols[i % 3]:
            translations[lang] = st.text_input(lang, key=f"trans_{lang}")

    submitted = st.form_submit_button("Add to Database", type="primary")

if submitted:
    if not new_nepali.strip():
        st.error("Nepali word/phrase is required!")
    else:
        new_row = {"Nepali": new_nepali.strip()}
        for lang, value in translations.items():
            if value.strip():
                new_row[lang] = value.strip()

        new_df = pd.DataFrame([new_row])
        updated_df = pd.concat([df, new_df], ignore_index=True)
        conn.update(worksheet=WORKSHEET, data=updated_df)
        st.success("New translation added successfully! 🎉")
        st.rerun()
