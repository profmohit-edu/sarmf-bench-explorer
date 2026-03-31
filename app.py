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
severity_map = {"Low": 1, "Medium": 2, "High": 3}
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

col1.metric("Contracts", filtered_df["Contract"].nunique())
col2.metric("Records", len(filtered_df))
col3.metric("Vulnerabilities", filtered_df["Vulnerability"].nunique())
col4.metric("Avg Risk Score", round(filtered_df["Risk Score"].mean(), 2) if not filtered_df.empty else 0)

# ---------------- TOP RISK HIGHLIGHT ----------------
st.subheader("Critical Risk Highlight")

if not filtered_df.empty:
    top_contract = filtered_df.sort_values("Risk Score", ascending=False).iloc[0]
    st.warning(
        f"Highest Risk Contract: {top_contract['Contract']} "
        f"({top_contract['Vulnerability']} | Severity: {top_contract['Severity']})"
    )

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

# ---------------- TOP RISK CONTRACTS ----------------
st.subheader("Top Risk Contracts")

if not filtered_df.empty:
    risk_table = (
        filtered_df.groupby("Contract", as_index=False)["Risk Score"]
        .max()
        .sort_values("Risk Score", ascending=False)
    )
    st.dataframe(risk_table, use_container_width=True)

st.markdown("---")

# ---------------- TOOL COMPARISON ----------------
st.subheader("Tool Comparison")

if not filtered_df.empty:
    tool_compare = pd.crosstab(filtered_df["Tool"], filtered_df["Vulnerability"])
    st.dataframe(tool_compare, use_container_width=True)

st.markdown("---")

# ---------------- TOOL EFFECTIVENESS ----------------
st.subheader("Tool Effectiveness")

if not filtered_df.empty:
    st.bar_chart(filtered_df["Tool"].value_counts())

st.markdown("---")

# ---------------- INTERPRETATION ----------------
st.subheader("Analytical Interpretation")

if not filtered_df.empty:
    most_common_vuln = filtered_df["Vulnerability"].value_counts().idxmax()
    most_used_tool = filtered_df["Tool"].value_counts().idxmax()

    st.write(f"Most frequent vulnerability: {most_common_vuln}")
    st.write(f"Most active tool: {most_used_tool}")

    st.write("""
The observed distribution suggests concentration of vulnerabilities in specific categories, 
indicating recurring design weaknesses.

Tool comparison highlights variability in detection coverage, supporting the need for 
multi-tool validation in smart contract security analysis.
""")

st.markdown("---")

# ---------------- CONTRACT INSPECTION ----------------
st.subheader("Contract Inspection")

selected_contract = None

if not filtered_df.empty:
    selected_contract = st.selectbox("Select Contract", filtered_df["Contract"].unique())

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

# ---------------- PDF FUNCTION ----------------
def create_pdf(contract, vuln, severity, tool, risk):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    y = 800
    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, y, "SARMF-Bench Report")
    y -= 30
    pdf.drawString(50, y, f"Contract: {contract}")
    y -= 20
    pdf.drawString(50, y, f"Vulnerability: {vuln}")
    y -= 20
    pdf.drawString(50, y, f"Severity: {severity}")
    y -= 20
    pdf.drawString(50, y, f"Tool: {tool}")
    y -= 20
    pdf.drawString(50, y, f"Risk Score: {risk}")

    pdf.save()
    buffer.seek(0)
    return buffer

# ---------------- PDF DOWNLOAD ----------------
st.subheader("Generate PDF Report")

if selected_contract:
    pdf_file = create_pdf(selected_contract, vuln_val, severity_val, tool_val, risk_val)

    st.download_button(
        "Download PDF",
        pdf_file,
        file_name=f"{selected_contract}_report.pdf"
    )

# ---------------- FINAL POSITIONING ----------------
st.info("Prototype system demonstrating AI-assisted benchmarking of smart contract vulnerabilities.")

# ---------------- FOOTER ----------------
st.write("SARMF Framework | Research Prototype System")
