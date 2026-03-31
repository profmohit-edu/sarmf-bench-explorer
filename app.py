import streamlit as st
import pandas as pd

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="SARMF-Bench Explorer",
    layout="wide",
)

# -------------------- DATASET (CSV FIRST, THEN FALLBACK) --------------------
try:
    df = pd.read_csv("sarmf_dataset.csv")
except:
    data = [
        {"Contract": "C1", "Vulnerability": "Reentrancy", "Severity": "High", "Tool": "Mythril"},
        {"Contract": "C2", "Vulnerability": "Overflow", "Severity": "Medium", "Tool": "Slither"},
        {"Contract": "C3", "Vulnerability": "Access Control", "Severity": "High", "Tool": "Oyente"},
        {"Contract": "C4", "Vulnerability": "DoS", "Severity": "Low", "Tool": "Mythril"},
        {"Contract": "C5", "Vulnerability": "Timestamp", "Severity": "Medium", "Tool": "Slither"},
    ]
    df = pd.DataFrame(data)

# -------------------- HEADER --------------------
st.title("SARMF-Bench Explorer")
st.subheader("Interactive Smart Contract Vulnerability Benchmarking Portal")

st.write(
    "Explore smart contracts, vulnerability types, severities, and tool findings "
    "using an interactive dashboard."
)

st.markdown(
    """
**Developed by:** Mohit Tiwari  
Assistant Professor, Department of Computer Science  
Bharati Vidyapeeth's College of Engineering, New Delhi
"""
)

st.markdown("---")

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.title("Filters")

vuln_filter = st.sidebar.multiselect(
    "Vulnerability type",
    options=sorted(df["Vulnerability"].unique()),
    default=sorted(df["Vulnerability"].unique()),
)

severity_filter = st.sidebar.multiselect(
    "Severity level",
    options=sorted(df["Severity"].unique()),
    default=sorted(df["Severity"].unique()),
)

tool_filter = st.sidebar.multiselect(
    "Analysis tool",
    options=sorted(df["Tool"].unique()),
    default=sorted(df["Tool"].unique()),
)

filtered_df = df[
    df["Vulnerability"].isin(vuln_filter)
    & df["Severity"].isin(severity_filter)
    & df["Tool"].isin(tool_filter)
]

st.sidebar.caption("Filtering controls for vulnerability, severity, and tool.")

# -------------------- OVERVIEW METRICS --------------------
st.subheader("Dataset Overview")

m1, m2, m3 = st.columns(3)
m1.metric("Total contracts", len(filtered_df))
m2.metric("Unique vulnerabilities", filtered_df["Vulnerability"].nunique())
m3.metric("Tools represented", filtered_df["Tool"].nunique())

st.markdown("---")

# -------------------- DISTRIBUTION --------------------
st.subheader("Distributions")

c1, c2 = st.columns(2)

with c1:
    st.write("Vulnerability distribution")
    if not filtered_df.empty:
        st.bar_chart(filtered_df["Vulnerability"].value_counts())
    else:
        st.info("No data available.")

with c2:
    st.write("Severity distribution")
    if not filtered_df.empty:
        severity_order = ["Low", "Medium", "High"]
        st.bar_chart(
            filtered_df["Severity"]
            .value_counts()
            .reindex(severity_order)
            .fillna(0)
        )
    else:
        st.info("No data available.")

st.markdown("---")

# -------------------- TABLE + INSPECTION --------------------
st.subheader("Contracts and Detailed Inspection")

tcol, dcol = st.columns([2, 1])

with tcol:
    if filtered_df.empty:
        st.warning("No matching contracts.")
        selected_contract = None
        contract_data = pd.DataFrame()
    else:
        st.dataframe(filtered_df, use_container_width=True)

        selected_contract = st.selectbox(
            "Select contract",
            filtered_df["Contract"].unique(),
        )

        contract_data = filtered_df[
            filtered_df["Contract"] == selected_contract
        ]

with dcol:
    if selected_contract is None or contract_data.empty:
        st.info("Select a contract to view details.")
        vuln_val = None
        severity_val = None
        tool_val = None
    else:
        row = contract_data.iloc[0]
        vuln_val = row["Vulnerability"]
        severity_val = row["Severity"]
        tool_val = row["Tool"]

        st.write(f"Contract: {row['Contract']}")
        st.write(f"Vulnerability: {vuln_val}")
        st.write(f"Severity: {severity_val}")
        st.write(f"Tool: {tool_val}")

        st.write("Interpretation:")
        st.write(
            f"The contract shows {vuln_val} vulnerability with {severity_val} severity."
        )

st.markdown("---")

# -------------------- REPORT --------------------
st.subheader("Generate Report")

if selected_contract is not None and vuln_val is not None:
    report_text = f"""
SARMF-Bench Analysis Report

Contract: {selected_contract}
Vulnerability: {vuln_val}
Severity: {severity_val}
Tool: {tool_val}

Summary:
The contract shows a {vuln_val} vulnerability with {severity_val} severity.

Recommendation:
Further manual audit required.

Developed by:
Mohit Tiwari
Assistant Professor, CSE
BVCOE, New Delhi
"""

    st.download_button(
        "Download report",
        report_text,
        file_name=f"{selected_contract}_report.txt",
    )
else:
    st.info("Select a contract to enable report.")

st.markdown("---")

# -------------------- ABOUT --------------------
st.write("This system supports dataset-driven smart contract vulnerability analysis.")
