import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SARMF-Bench Explorer", layout="wide")

# ---------------- LOAD CSV ----------------
try:
    df = pd.read_csv("sarmf_dataset.csv")
except Exception as e:
    st.error("CSV NOT FOUND - Keep 'sarmf_dataset.csv' in same folder")
    st.write(e)
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("SARMF Controls")

st.sidebar.markdown("### Filter Data")

vuln_filter = st.sidebar.multiselect(
    "Vulnerability",
    sorted(df["Vulnerability"].unique()),
    default=sorted(df["Vulnerability"].unique())
)

severity_filter = st.sidebar.multiselect(
    "Severity",
    sorted(df["Severity"].unique()),
    default=sorted(df["Severity"].unique())
)

tool_filter = st.sidebar.multiselect(
    "Tool",
    sorted(df["Tool"].unique()),
    default=sorted(df["Tool"].unique())
)

filtered_df = df[
    df["Vulnerability"].isin(vuln_filter) &
    df["Severity"].isin(severity_filter) &
    df["Tool"].isin(tool_filter)
]

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
forming a base for reproducible security evaluation and research.
""")

st.markdown("---")

# ---------------- OVERVIEW ----------------
st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Contracts", filtered_df["Contract"].nunique())
col2.metric("Total Records", len(filtered_df))
col3.metric("Unique Vulnerabilities", filtered_df["Vulnerability"].nunique())

st.markdown("---")

# ---------------- DATA TABLE ----------------
st.subheader("Contract Data")

if filtered_df.empty:
    st.warning("No matching data")
else:
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# ---------------- ANALYSIS ----------------
st.subheader("Analysis")

col1, col2 = st.columns(2)

with col1:
    st.write("Vulnerability Distribution")
    if not filtered_df.empty:
        st.bar_chart(filtered_df["Vulnerability"].value_counts())

with col2:
    st.write("Severity Distribution")
    if not filtered_df.empty:
        order = ["Low", "Medium", "High"]
        st.bar_chart(
            filtered_df["Severity"]
            .value_counts()
            .reindex(order)
            .fillna(0)
        )

st.markdown("---")

# ---------------- CONTRACT INSPECTION ----------------
st.subheader("Contract Inspection")

if filtered_df.empty:
    st.info("No data available")
else:
    selected_contract = st.selectbox(
        "Select Contract",
        filtered_df["Contract"].unique()
    )

    row = filtered_df[filtered_df["Contract"] == selected_contract].iloc[0]

    st.write("Contract:", row["Contract"])
    st.write("Vulnerability:", row["Vulnerability"])
    st.write("Severity:", row["Severity"])
    st.write("Tool:", row["Tool"])

    st.write("Recommendation: Further manual audit required.")

st.markdown("---")

# ---------------- FOOTER ----------------
st.write("SARMF Framework | Smart Contract Security Analysis System")
