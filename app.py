import streamlit as st
import pandas as pd

st.set_page_config(page_title="SARMF-Bench Dashboard", layout="wide")

# ---------------- LOAD CSV ----------------
try:
    df = pd.read_csv("sarmf_dataset.csv")
except:
    st.error("CSV file not found. Keep 'sarmf_dataset.csv' in same folder as app.py")
    st.stop()

# ---------------- HEADER ----------------
st.title("SARMF-Bench Dashboard")
st.write("Smart Contract Vulnerability Analysis System")

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Contracts", df['Contract'].nunique())
col2.metric("Total Issues", len(df))
col3.metric("Vulnerabilities", df['Vulnerability'].nunique())

# ---------------- FILTER ----------------
selected_contract = st.selectbox(
    "Select Contract",
    ["All"] + list(df['Contract'].unique())
)

if selected_contract != "All":
    filtered_df = df[df['Contract'] == selected_contract]
else:
    filtered_df = df

# ---------------- TABLE ----------------
st.subheader("Data")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- CHART ----------------
st.subheader("Vulnerability Distribution")
st.bar_chart(filtered_df['Vulnerability'].value_counts())
