import streamlit as st
import pandas as pd

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="SARMF-Bench Explorer",
    layout="wide",
)

# -------------------- DATASET (DEMO) --------------------
data = [
    {"Contract": "C1", "Vulnerability": "Reentrancy",      "Severity": "High",   "Tool": "Mythril"},
    {"Contract": "C2", "Vulnerability": "Overflow",        "Severity": "Medium", "Tool": "Slither"},
    {"Contract": "C3", "Vulnerability": "Access Control",  "Severity": "High",   "Tool": "Oyente"},
    {"Contract": "C4", "Vulnerability": "DoS",             "Severity": "Low",    "Tool": "Mythril"},
    {"Contract": "C5", "Vulnerability": "Timestamp",       "Severity": "Medium", "Tool": "Slither"},
    {"Contract": "C6", "Vulnerability": "Overflow",        "Severity": "High",   "Tool": "Mythril"},
    {"Contract": "C7", "Vulnerability": "Access Control",  "Severity": "Low",    "Tool": "Slither"},
    {"Contract": "C8", "Vulnerability": "Reentrancy",      "Severity": "Medium", "Tool": "Oyente"},
    {"Contract": "C9", "Vulnerability": "DoS",             "Severity": "Medium", "Tool": "Slither"},
    {"Contract": "C10","Vulnerability": "Timestamp",       "Severity": "Low",    "Tool": "Oyente"},
]

df = pd.DataFrame(data)

# -------------------- HEADER --------------------
st.title("SARMF-Bench Explorer")
st.subheader("Interactive Smart Contract Vulnerability Benchmarking Portal")

st.write(
    "Explore demo smart contracts, vulnerability types, severities, and tool findings "
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

st.sidebar.caption("Use these filters to focus on particular vulnerability types, severities, or tools.")

# -------------------- OVERVIEW METRICS --------------------
st.subheader("Dataset Overview")

m1, m2, m3 = st.columns(3)
m1.metric("Total contracts", len(filtered_df))
m2.metric("Unique vulnerabilities", filtered_df["Vulnerability"].nunique())
m3.metric("Tools represented", filtered_df["Tool"].nunique())

st.markdown("---")

# -------------------- DISTRIBUTION CHARTS --------------------
st.subheader("Distributions")

c1, c2 = st.columns(2)

with c1:
    st.markdown("**Vulnerability distribution**")
    if not filtered_df.empty:
        vuln_counts = filtered_df["Vulnerability"].value_counts().sort_values(ascending=False)
        st.bar_chart(vuln_counts)
    else:
        st.info("No data for current filter selection.")

with c2:
    st.markdown("**Severity distribution**")
    if not filtered_df.empty:
        severity_order = ["Low", "Medium", "High"]
        severity_counts = (
            filtered_df["Severity"]
            .value_counts()
            .reindex(severity_order)
            .fillna(0)
            .astype(int)
        )
        st.bar_chart(severity_counts)
    else:
        st.info("No data for current filter selection.")

st.markdown("---")

# -------------------- TABLE + CONTRACT INSPECTION --------------------
st.subheader("Contracts and Detailed Inspection")

tcol, dcol = st.columns([2, 1])

with tcol:
    st.markdown("**Contracts table**")
    if filtered_df.empty:
        st.warning("No contracts match the current filters.")
        selected_contract = None
        contract_data = pd.DataFrame()
    else:
        st.dataframe(
            filtered_df.reset_index(drop=True),
            use_container_width=True,
        )

        selected_contract = st.selectbox(
            "Select a contract for detailed view",
            options=filtered_df["Contract"].unique(),
            key="contract_selector",
        )
        contract_data = filtered_df[filtered_df["Contract"] == selected_contract]

with dcol:
    st.markdown("**Contract details**")
    if selected_contract is None or contract_data.empty:
        st.info("Select a contract from the list to see details.")
        vuln_val = None
        severity_val = None
    else:
        row = contract_data.iloc[0]
        vuln_val = row["Vulnerability"]
        severity_val = row["Severity"]
        tool_val = row["Tool"]

        st.write(f"**Contract ID:** {row['Contract']}")
        st.write(f"**Vulnerability:** {vuln_val}")
        st.write(f"**Severity:** {severity_val}")
        st.write(f"**Tool:** {tool_val}")

        st.markdown("**Quick interpretation**")
        st.write(
            f"The selected contract is flagged for **{vuln_val}** with "
            f"**{severity_val}** severity by **{tool_val}**."
        )

st.markdown("---")

# -------------------- REPORT DOWNLOAD --------------------
st.subheader("Generate Simple Text Report")

if selected_contract is not None and vuln_val is not None:
    report_text = f"""
SARMF-Bench Analysis Report (DEMO)

Contract: {selected_contract}
Detected vulnerability: {vuln_val}
Severity: {severity_val}
Tool: {tool_val}

Summary:
The contract shows a {vuln_val} vulnerability with {severity_val} severity, as reported by {tool_val}.

Recommendation:
This is a demo report. In a real SARMF-Bench deployment, this section would
be based on cross-tool validation and manual review outcomes.

Developed by:
Mohit Tiwari
Assistant Professor, CSE
BVCOE, New Delhi
"""

    st.download_button(
        label="Download text report",
        data=report_text,
        file_name=f"{selected_contract}_report.txt",
    )
else:
    st.info("Select a contract above to enable report generation.")

st.markdown("---")

# -------------------- ABOUT SECTION --------------------
st.markdown("#### About this demo")
st.write(
    "This Streamlit app demonstrates the concept of **SARMF-Bench Explorer** on a small "
    "synthetic dataset. In a full deployment, it would be backed by real smart contracts, "
    "SWC labels, and cross-tool findings from your SARMF-Bench benchmark."
)
st.caption("Built with Streamlit Community Cloud.")
