import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Statistics")


st.title('Statistics')

# --- Connect to Google Sheets ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Read data (optional) ---
df = conn.read(worksheet="Orders", usecols=[0, 1, 2,3,4], ttl=5)
prices_df = conn.read(worksheet="Prices")

# Let user choose a column to calculate total
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

if numeric_columns:
    selected_column = st.selectbox("Select a numeric column to calculate total:", numeric_columns)
    total = df[selected_column].sum()
    st.success(f"✅ {selected_column}**: {total:,}")
else:
    st.warning("No numeric columns found in the uploaded data.")
