import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="SARMF-Bench Explorer", layout="wide")

st.title("SARMF-Bench Explorer")
st.subheader("Smart Contract Vulnerability Benchmarking System")
st.write("Developed by Mohit Tiwari")

# Generate large dataset
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

vuln = st.sidebar.multiselect("Vulnerability", df["Vulnerability"].unique(), default=df["Vulnerability"].unique())
severity = st.sidebar.multiselect("Severity", df["Severity"].unique(), default=df["Severity"].unique())

filtered_df = df[
    (df["Vulnerability"].isin(vuln)) &
    (df["Severity"].isin(severity))
]

# Metrics
col1, col2 = st.columns(2)
col1.metric("Total Contracts", len(filtered_df))
col2.metric("Unique Vulnerabilities", filtered_df["Vulnerability"].nunique())

# Table
st.dataframe(filtered_df, use_container_width=True)

# Charts
st.subheader("Vulnerability Distribution")
st.bar_chart(filtered_df["Vulnerability"].value_counts())

st.subheader("Severity Distribution")
st.bar_chart(filtered_df["Severity"].value_counts())
import streamlit as st
import pandas as pd

st.title("SARMF-Bench Explorer")
st.write("Developed by Mohit Tiwari")

data = {
    "Contract": ["C1", "C2", "C3"],
    "Vulnerability": ["Reentrancy", "Overflow", "Access Control"],
    "Severity": ["High", "Medium", "High"]
}

df = pd.DataFrame(data)

st.dataframe(df)
