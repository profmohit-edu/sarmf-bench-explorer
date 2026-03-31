import streamlit as st
import pandas as pd
import random

# Page configuration
st.set_page_config(page_title="SARMF-Bench Explorer", layout="wide")

# Title
st.title("SARMF-Bench Explorer")
st.subheader("Smart Contract Vulnerability Benchmarking System")

# Author + affiliation (PROFESSIONAL FORMAT)
st.write("""
**Developed by Mohit Tiwari**  
Assistant Professor, Department of Computer Science  
Bharati Vidyapeeth's College of Engineering, New Delhi
""")

st.caption("An independent academic research system for smart contract vulnerability benchmarking by Mohit Tiwari,Dept of CSE,BVCOE Delhi.")

# Generate dataset
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

# Sidebar filters
st.sidebar.header("Filters")

vuln = st.sidebar.multiselect(
    "Vulnerability",
    df["Vulnerability"].unique(),
    default=df["Vulnerability"].unique()
)

severity = st.sidebar.multiselect(
    "Severity",
    df["Severity"].unique(),
    default=df["Severity"].unique()
)

filtered_df = df[
    (df["Vulnerability"].isin(vuln)) &
    (df["Severity"].isin(severity))
]

# Metrics
col1, col2 = st.columns(2)
col1.metric("Total Contracts", len(filtered_df))
col2.metric("Unique Vulnerabilities", filtered_df["Vulnerability"].nunique())

# Data table
st.dataframe(filtered_df, use_container_width=True)

# Charts
st.subheader("Vulnerability Distribution")
st.bar_chart(filtered_df["Vulnerability"].value_counts())

st.subheader("Severity Distribution")
st.bar_chart(filtered_df["Severity"].value_counts())

# Contract inspection (KEY FEATURE)
st.subheader("🔍 Contract Inspection")

selected_contract = st.selectbox(
    "Select Contract",
    filtered_df["Contract"]
)

contract_data = filtered_df[filtered_df["Contract"] == selected_contract]

st.write("### Details")
st.write(contract_data)

st.write("### Interpretation")

vuln_val = contract_data["Vulnerability"].values[0]
severity_val = contract_data["Severity"].values[0]

st.success(f"This contract shows {vuln_val} vulnerability with {severity_val} severity.")
st.warning("Recommendation: Further manual audit required.")
