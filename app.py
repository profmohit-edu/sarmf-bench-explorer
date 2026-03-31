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

# ---------------- AI RISK SCORING ----------------
severity_map = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

df["Risk Score"] = df["Severity"].map(severity_map)

# ---------------- SIDEBAR ----------------
st.sidebar.title("SARMF Controls")

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
st.subheader("AI-Assisted Smart Contract Vulnerability Benchmarking System")

st.write("""
Developed by Mohit Tiwari  
Assistant Professor, Department of Computer Science  
Bharati Vidyapeeth's College of Engineering, New Delhi
""")

st.markdown("---")

# ---------------- RESEARCH POSITIONING ----------------
st.subheader("Research Context")

st.write("""
This system demonstrates a structured benchmarking approach for analyzing smart contract vulnerabilities 
across multiple automated analysis tools.

It incorporates a rule-based risk scoring mechanism that simulates AI-driven vulnerability prioritization, 
enabling comparative evaluation and decision support in secure blockchain development.

The framework can be extended into a full AI-based Cyber Maturity Index (CMI) model.
""")

st.markdown("---")

# ---------------- OVERVIEW ----------------
st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Contracts", filtered_df["Contract"].nunique())
col2.metric("Records", len(filtered_df))
col3.metric("Vulnerabilities", filtered_df["Vulnerability"].nunique())
col4.metric("Avg Risk Score", round(filtered_df["Risk Score"].mean(), 2) if not filtered_df.empty else 0)

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

# ---------------- TOOL COMPARISON ----------------
st.subheader("Tool Comparison")

if not filtered_df.empty:
    tool_compare = pd.crosstab(filtered_df["Tool"], filtered_df["Vulnerability"])
    st.dataframe(tool_compare)

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
    st.write("Risk Score:", row["Risk Score"])

    st.write("Recommendation: Prioritize based on risk score and validate manually.")

st.markdown("---")

# ---------------- FOOTER ----------------
st.write("SARMF Framework | AI-Driven Smart Contract Security Analysis System")
