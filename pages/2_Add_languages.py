import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
WORKSHEET = "Translations"
df = conn.read(worksheet=WORKSHEET, ttl=0)

st.title("➕ Add New Language")

new_lang = st.text_input("New Language Name", placeholder="e.g., Thakuri, Tamang, etc.")

if st.button("Add Language", type="primary"):
    if not new_lang:
        st.error("Please enter a language name.")
    elif new_lang in df.columns:
        st.warning("This language already exists!")
    else:
        df[new_lang] = pd.NA
        conn.update(worksheet=WORKSHEET, data=df)
        st.success(f"Added new language: **{new_lang}** 🎉")
        st.rerun()