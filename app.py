import streamlit as st
import pandas as pd
import random

# Page config
st.set_page_config(
    page_title="SARMF-Bench Explorer",
    layout="wide"
)

# Custom styling (IMPORTANT)
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    color: #1f4e79;
}
h2, h3 {
    color: #2c3e50;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<h1>SARMF-Bench Explorer</h1>
<h3>Smart Contract Vulnerability Benchmarking System</h3>
""", unsafe_allow_html=True)

# Author
st.markdown("""
<b>Developed by Mohit Tiwari</b><br>
Assistant Professor, Department of Computer Science<br>
Bharati Vidyapeeth's College of Engineering, New Delhi
""", unsafe_allow_html=True)

st.markdown("---")

# DATA GENERATION
contracts = []
vulnerabilities = ["Reentrancy", "Overflow", "Access Control", "Timestamp", "DoS"]
severities = ["Low", "Medium", "High"]
tools = ["Slither", "Mythril", "Oyente"]

for i in range(100):
    contracts.append({
        "Contract": f"C{i}",
        "Vulnerability": random.choice(vulnerabilities),
        "Severity": random.choice(severities),
        "Tool": random.choice(tools)
    })

df = pd.DataFrame(contracts)

# SIDEBAR
st.sidebar.title("Filters")

vuln = st.sidebar.multiselect(
    "Select Vulnerability",
    df["Vulnerability"].unique(),
    default=df["Vulnerability"].unique()
)

severity = st.sidebar.multiselect(
    "Select Severity",
    df["Severity"].unique(),
    default=df["Severity"].unique()
)

filtered_df = df[
    (df["Vulnerability"].isin(vuln)) &
    (df["Severity"].isin(severity))
]

# METRICS
st.markdown("## Overview")

col1, col2 = st.columns(2)

col1.metric("Total Contracts", len(filtered_df))
col2.metric("Unique Vulnerabilities", filtered_df["Vulnerability"].nunique())

st.markdown("---")

# TABLE
st.markdown("## Contract Data")

st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# CHARTS
col3, col4 = st.columns(2)

with col3:
    st.markdown("### Vulnerability Distribution")
    st.bar_chart(filtered_df["Vulnerability"].value_counts())

with col4:
    st.markdown("### Severity Distribution")
    st.bar_chart(filtered_df["Severity"].value_counts())

st.markdown("---")

# INSPECTION SECTION
st.markdown("## 🔍 Contract Inspection")

selected_contract = st.selectbox(
    "Select Contract",
    filtered_df["Contract"]
)

contract_data = filtered_df[filtered_df["Contract"] == selected_contract]

st.markdown("### Details")
st.dataframe(contract_data)

st.markdown("### Analysis")

vuln_val = contract_data["Vulnerability"].values[0]
severity_val = contract_data["Severity"].values[0]

st.success(f"Detected: {vuln_val} vulnerability")
st.warning(f"Severity Level: {severity_val}")
st.info("Recommendation: Further manual audit required.")
