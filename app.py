import streamlit as st
import pandas as pd

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="SARMF-Bench Explorer",
    layout="wide",
)

# -------------------- CLEAN STYLING --------------------
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

h1 {
    color: #1f4e79;
    font-weight: 700;
}

h2, h3 {
    color: #2c3e50;
}

.block-container {
    padding-top: 2rem;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e6e6e6;
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOAD DATA --------------------
try:
    df = pd.read_csv("sarmf_dataset.csv")
except:
    df = pd.DataFrame([
        {"Contract": "C1", "Vulnerability": "Reentrancy", "Severity": "High", "Tool": "Mythril"},
        {"Contract": "C2", "Vulnerability": "Overflow", "Severity": "Medium", "Tool": "Slither"},
        {"Contract": "C3", "Vulnerability": "Access Control", "Severity": "High", "Tool": "Oyente"},
    ])

# -------------------- HEADER --------------------
st.title("SARMF-Bench Explorer")
st.subheader("Smart Contract Vulnerability Benchmarking System")

st.write("""
Developed by Mohit Tiwari  
Assistant Professor, Department of Computer Science  
Bharati Vidyapeeth's College of Engineering, New Delhi
""")

st.markdown("---")

# -------------------- SYSTEM PURPOSE --------------------
st.subheader("System Purpose")

st.write("""
SARMF-Bench Explorer is a prototype system designed to support benchmarking of 
smart contract vulnerabilities across multiple analysis tools.

The system enables structured comparison of vulnerability types, severity levels, 
and tool outputs, providing a foundation for reproducible evaluation of 
smart contract security mechanisms.
""")

st.markdown("---")

# -------------------- FILTERS --------------------
st.sidebar.header("Filters")

vuln_filter = st.sidebar.multiselect(
    "Vulnerability",
    sorted(df["Vulnerability"].unique()),
    default=sorted(df["Vulnerability"].unique()),
)

severity_filter = st.sidebar.multiselect(
    "Severity",
    sorted(df["Severity"].unique()),
    default=sorted(df["Severity"].unique()),
)

tool_filter = st.sidebar.multiselect(
    "Tool",
    sorted(df["Tool"].unique()),
    default=sorted(df["Tool"].unique()),
)

filtered_df = df[
    df["Vulnerability"].isin(vuln_filter)
    & df["Severity"].isin(severity_filter)
    & df["Tool"].isin(tool_filter)
]

# -------------------- OVERVIEW --------------------
st.subheader("Dataset Overview")

c1, c2, c3 = st.columns(3)
c1.metric("Total Contracts", len(filtered_df))
c2.metric("Unique Vulnerabilities", filtered_df["Vulnerability"].nunique())
c3.metric("Tools", filtered_df["Tool"].nunique())

st.markdown("---")

# -------------------- TABLE --------------------
st.subheader("Contract Data")

if filtered_df.empty:
    st.warning("No matching data")
else:
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# -------------------- ANALYSIS --------------------
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

# -------------------- CONTRACT INSPECTION --------------------
st.subheader("Contract Inspection")

if filtered_df.empty:
    st.info("No contracts available")
    selected_contract = None
else:
    selected_contract = st.selectbox(
        "Select Contract",
        filtered_df["Contract"].unique()
    )

if selected_contract:
    row = filtered_df[filtered_df["Contract"] == selected_contract].iloc[0]

    vuln_val = row["Vulnerability"]
    severity_val = row["Severity"]
    tool_val = row["Tool"]

    st.markdown("### Details")
    st.write(f"Contract: {row['Contract']}")
    st.write(f"Vulnerability: {vuln_val}")
    st.write(f"Severity: {severity_val}")
    st.write(f"Tool: {tool_val}")

    st.markdown("### Interpretation")
    st.write(
        f"The contract shows {vuln_val} vulnerability with {severity_val} severity."
    )

st.markdown("---")

# -------------------- REPORT --------------------
st.subheader("Generate Report")

if selected_contract:
    report = f"""
SARMF-Bench Analysis Report

Contract: {selected_contract}
Vulnerability: {vuln_val}
Severity: {severity_val}
Tool: {tool_val}

Summary:
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
        report,
        file_name=f"{selected_contract}_report.txt"
    )
else:
    st.info("Select a contract first")
