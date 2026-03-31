import streamlit as st
import pandas as pd

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="SARMF-Bench Explorer", layout="wide")

# -------------------- HEADER --------------------
st.title("SARMF-Bench Explorer")
st.subheader("Smart Contract Vulnerability Benchmarking System")

st.write("""
Developed by Mohit Tiwari  
Assistant Professor, Department of Computer Science  
Bharati Vidyapeeth's College of Engineering, New Delhi
""")

st.markdown("---")

# -------------------- DATASET --------------------
data = [
    {"Contract": "C1", "Vulnerability": "Reentrancy", "Severity": "High", "Tool": "Mythril"},
    {"Contract": "C2", "Vulnerability": "Overflow", "Severity": "Medium", "Tool": "Slither"},
    {"Contract": "C3", "Vulnerability": "Access Control", "Severity": "High", "Tool": "Oyente"},
    {"Contract": "C4", "Vulnerability": "DoS", "Severity": "Low", "Tool": "Mythril"},
    {"Contract": "C5", "Vulnerability": "Timestamp", "Severity": "Medium", "Tool": "Slither"},
    {"Contract": "C6", "Vulnerability": "Overflow", "Severity": "High", "Tool": "Mythril"},
    {"Contract": "C7", "Vulnerability": "Access Control", "Severity": "Low", "Tool": "Slither"},
    {"Contract": "C8", "Vulnerability": "Reentrancy", "Severity": "Medium", "Tool": "Oyente"},
    {"Contract": "C9", "Vulnerability": "DoS", "Severity": "Medium", "Tool": "Slither"},
    {"Contract": "C10", "Vulnerability": "Timestamp", "Severity": "Low", "Tool": "Oyente"},
]

df = pd.DataFrame(data)

# -------------------- SIDEBAR FILTER --------------------
st.sidebar.title("Filters")

vuln_filter = st.sidebar.multiselect(
    "Select Vulnerability",
    df["Vulnerability"].unique(),
    default=df["Vulnerability"].unique()
)

severity_filter = st.sidebar.multiselect(
    "Select Severity",
    df["Severity"].unique(),
    default=df["Severity"].unique()
)

filtered_df = df[
    (df["Vulnerability"].isin(vuln_filter)) &
    (df["Severity"].isin(severity_filter))
]

# -------------------- OVERVIEW --------------------
st.subheader("Dataset Overview")

col1, col2 = st.columns(2)
col1.metric("Total Contracts", len(filtered_df))
col2.metric("Unique Vulnerabilities", filtered_df["Vulnerability"].nunique())

st.markdown("---")

# -------------------- TABLE --------------------
st.subheader("Contract Data")
st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# -------------------- ANALYSIS --------------------
st.subheader("Analytical Summary")

st.write("Vulnerability Distribution")
st.bar_chart(filtered_df["Vulnerability"].value_counts())

st.write("Severity Distribution")
st.bar_chart(filtered_df["Severity"].value_counts())

st.markdown("---")

# -------------------- CONTRACT INSPECTION --------------------
st.subheader("Contract Inspection")

selected_contract = st.selectbox(
    "Select Contract",
    filtered_df["Contract"].unique(),
    key="contract_selector"
)

contract_data = filtered_df[filtered_df["Contract"] == selected_contract]

st.write("Details")
st.dataframe(contract_data, use_container_width=True)

vuln_val = contract_data["Vulnerability"].values[0]
severity_val = contract_data["Severity"].values[0]

st.write("Analysis Result")
st.write(f"Detected Vulnerability: {vuln_val}")
st.write(f"Severity Level: {severity_val}")
st.write("Recommendation: Further manual audit required.")

st.markdown("---")

# -------------------- REPORT DOWNLOAD --------------------
st.subheader("Generate Report")

report_text = f"""
SARMF-Bench Analysis Report

Contract: {selected_contract}
Vulnerability: {vuln_val}
Severity: {severity_val}

Analysis Summary:
The contract shows {vuln_val} vulnerability with {severity_val} severity.

Recommendation:
Further manual audit required.

Developed by:
Mohit Tiwari
Assistant Professor, CSE
BVCOE, New Delhi
"""

st.download_button(
    "Download Report",
    report_text,
    file_name=f"{selected_contract}_report.txt"
)
