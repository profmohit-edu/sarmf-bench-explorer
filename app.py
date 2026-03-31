import streamlit as st
import pandas as pd

st.set_page_config(page_title="SARMF-Bench Explorer", layout="wide")

# ---------------- LOAD CSV ----------------
try:
    df = pd.read_csv("sarmf_dataset.csv")
except Exception as e:
    st.error("CSV NOT FOUND - Keep 'sarmf_dataset.csv' in same folder")
    st.write(e)
    st.stop()

# ---------------- HEADER ----------------
st.title("SARMF-Bench Explorer")
st.subheader("Smart Contract Vulnerability Benchmarking System")

st.write("""
Developed by Mohit Tiwari  
Assistant Professor, Department of Computer Science  
Bharati Vidyapeeth's College of Engineering, New Delhi
""")

st.markdown("---")

# ---------------- SYSTEM PURPOSE ----------------
st.subheader("System Purpose")

st.write("""
This system supports benchmarking of smart contract vulnerabilities across multiple analysis tools.

It enables structured comparison of vulnerability types, severity levels, and tool outputs,
forming a base for reproducible security evaluation and research in blockchain systems.
""")

st.markdown("---")

# ---------------- RAW DATA (CONFIRMATION) ----------------
st.subheader("Dataset Preview")

st.dataframe(df, use_container_width=True)

st.markdown("---")

# ---------------- METRICS ----------------
st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Contracts", df['Contract'].nunique())
col2.metric("Total Records", len(df))
col3.metric("Unique Vulnerabilities", df['Vulnerability'].nunique())

st.markdown("---")

# ---------------- FILTER ----------------
st.subheader("Filter by Contract")

selected_contract = st.selectbox(
    "Select Contract",
    ["All"] + list(df["Contract"].unique())
)

if selected_contract != "All":
    filtered_df = df[df["Contract"] == selected_contract]
else:
    filtered_df = df

# ---------------- FILTERED DATA ----------------
st.subheader("Filtered Data")

st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# ---------------- CHART ----------------
st.subheader("Vulnerability Distribution")

st.bar_chart(filtered_df["Vulnerability"].value_counts())

st.markdown("---")

# ---------------- CONTRACT INSPECTION ----------------
st.subheader("Contract Inspection")

if not filtered_df.empty:
    contract_choice = st.selectbox(
        "Inspect Contract",
        filtered_df["Contract"].unique()
    )

    row = filtered_df[filtered_df["Contract"] == contract_choice].iloc[0]

    st.write("Contract:", row["Contract"])
    st.write("Vulnerability:", row["Vulnerability"])
    st.write("Severity:", row["Severity"])
    st.write("Tool:", row["Tool"])

    st.write("Recommendation: Further manual audit required.")
else:
    st.info("No data available")
