import io
import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="SARMF-Bench Explorer", layout="wide")

# ---------------- LOAD CSV ----------------
try:
    df = pd.read_csv("sarmf_dataset.csv")
except Exception as e:
    st.error("CSV NOT FOUND - Keep 'sarmf_dataset.csv' in same folder as app.py")
    st.write(e)
    st.stop()

# ---------------- AI RISK SCORING ----------------
severity_map = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

df["Risk Score"] = df["Severity"].map(severity_map).fillna(0)

# ---------------- SIDEBAR ----------------
st.sidebar.title("SARMF Controls")

vuln_filter = st.sidebar.multiselect(
    "Vulnerability",
    sorted(df["Vulnerability"].dropna().unique()),
    default=sorted(df["Vulnerability"].dropna().unique())
)

severity_filter = st.sidebar.multiselect(
    "Severity",
    sorted(df["Severity"].dropna().unique()),
    default=sorted(df["Severity"].dropna().unique())
)

tool_filter = st.sidebar.multiselect(
    "Tool",
    sorted(df["Tool"].dropna().unique()),
    default=sorted(df["Tool"].dropna().unique())
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

The framework can be extended into a full AI-based Cyber Maturity Index model.
""")

st.markdown("---")

# ---------------- OVERVIEW ----------------
st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

contracts_count = filtered_df["Contract"].nunique() if not filtered_df.empty else 0
records_count = len(filtered_df)
vuln_count = filtered_df["Vulnerability"].nunique() if not filtered_df.empty else 0
avg_risk = round(filtered_df["Risk Score"].mean(), 2) if not filtered_df.empty else 0

col1.metric("Contracts", contracts_count)
col2.metric("Records", records_count)
col3.metric("Vulnerabilities", vuln_count)
col4.metric("Avg Risk Score", avg_risk)

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
        severity_counts = (
            filtered_df["Severity"]
            .value_counts()
            .reindex(order)
            .fillna(0)
        )
        st.bar_chart(severity_counts)

st.markdown("---")

# ---------------- TOP RISK CONTRACTS ----------------
st.subheader("Top Risk Contracts")

if not filtered_df.empty:
    risk_table = (
        filtered_df.groupby("Contract", as_index=False)["Risk Score"]
        .max()
        .sort_values("Risk Score", ascending=False)
    )
    st.dataframe(risk_table, use_container_width=True)
else:
    st.info("No data available for ranking.")

st.markdown("---")

# ---------------- TOOL COMPARISON ----------------
st.subheader("Tool Comparison")

if not filtered_df.empty:
    tool_compare = pd.crosstab(filtered_df["Tool"], filtered_df["Vulnerability"])
    st.dataframe(tool_compare, use_container_width=True)
else:
    st.info("No data available for tool comparison.")

st.markdown("---")

# ---------------- TOOL EFFECTIVENESS GRAPH ----------------
st.subheader("Tool Effectiveness")

if not filtered_df.empty:
    tool_effectiveness = filtered_df["Tool"].value_counts()
    st.bar_chart(tool_effectiveness)
else:
    st.info("No data available for tool effectiveness graph.")

st.markdown("---")

# ---------------- CONTRACT INSPECTION ----------------
st.subheader("Contract Inspection")

selected_contract = None
vuln_val = None
severity_val = None
tool_val = None
risk_val = None

if filtered_df.empty:
    st.info("No data available")
else:
    selected_contract = st.selectbox(
        "Select Contract",
        filtered_df["Contract"].unique()
    )

    row = filtered_df[filtered_df["Contract"] == selected_contract].iloc[0]

    vuln_val = row["Vulnerability"]
    severity_val = row["Severity"]
    tool_val = row["Tool"]
    risk_val = row["Risk Score"]

    st.write("Contract:", row["Contract"])
    st.write("Vulnerability:", vuln_val)
    st.write("Severity:", severity_val)
    st.write("Tool:", tool_val)
    st.write("Risk Score:", risk_val)
    st.write("Recommendation: Prioritize based on risk score and validate manually.")

st.markdown("---")

# ---------------- PDF REPORT FUNCTION ----------------
def create_pdf_report(contract, vulnerability, severity, tool, risk_score):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 60
    line_gap = 22

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "SARMF-Bench Analysis Report")

    y -= 2 * line_gap
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Contract: {contract}")
    y -= line_gap
    pdf.drawString(50, y, f"Vulnerability: {vulnerability}")
    y -= line_gap
    pdf.drawString(50, y, f"Severity: {severity}")
    y -= line_gap
    pdf.drawString(50, y, f"Tool: {tool}")
    y -= line_gap
    pdf.drawString(50, y, f"Risk Score: {risk_score}")

    y -= 2 * line_gap
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Summary")
    y -= line_gap
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"The contract shows {vulnerability} vulnerability with {severity} severity.")
    y -= line_gap
    pdf.drawString(50, y, "Recommendation: Further manual audit required.")

    y -= 2 * line_gap
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Developed by")
    y -= line_gap
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, "Mohit Tiwari")
    y -= line_gap
    pdf.drawString(50, y, "Assistant Professor, Department of Computer Science")
    y -= line_gap
    pdf.drawString(50, y, "Bharati Vidyapeeth's College of Engineering, New Delhi")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer

# ---------------- PDF REPORT DOWNLOAD ----------------
st.subheader("Generate PDF Report")

if selected_contract is not None:
    pdf_buffer = create_pdf_report(
        selected_contract,
        vuln_val,
        severity_val,
        tool_val,
        risk_val
    )

    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name=f"{selected_contract}_report.pdf",
        mime="application/pdf"
    )
else:
    st.info("Select a contract first")

st.markdown("---")

# ---------------- FOOTER ----------------
st.write("SARMF Framework | AI-Driven Smart Contract Security Analysis System")
