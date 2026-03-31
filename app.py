import io
import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

st.set_page_config(page_title="SARMF Interactive Explorer", layout="wide")

# ---------------- LOAD CSV ----------------
try:
    df = pd.read_csv("sarmf_dataset.csv")
except Exception as e:
    st.error("CSV NOT FOUND - Keep 'sarmf_dataset.csv' in same folder as app.py")
    st.write(e)
    st.stop()

# ---------------- SAFE COLUMN CHECK ----------------
required_cols = ["Contract", "Vulnerability", "Severity", "Tool"]
missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing required columns in CSV: {missing_cols}")
    st.stop()

# ---------------- CREATE DATE COLUMN IF MISSING ----------------
if "Date" not in df.columns:
    df["Date"] = pd.date_range(start="2025-01-01", periods=len(df), freq="D")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# ---------------- AI RISK SCORING ----------------
st.sidebar.title("SARMF Controls")

st.sidebar.subheader("Risk Weighting")

low_w = st.sidebar.slider("Low Severity Weight", 0, 5, 1)
med_w = st.sidebar.slider("Medium Severity Weight", 0, 5, 2)
high_w = st.sidebar.slider("High Severity Weight", 0, 5, 3)

severity_map = {
    "Low": low_w,
    "Medium": med_w,
    "High": high_w
}

df["Risk Score"] = df["Severity"].map(severity_map).fillna(0)

df["Priority Class"] = df["Risk Score"].apply(
    lambda x: "High Priority" if x >= 3 else "Normal Priority"
)

# ---------------- SIDEBAR FILTERS ----------------
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

risk_threshold = st.sidebar.slider("Minimum Risk Score", 0, 5, 0)

filtered_df = df[
    df["Vulnerability"].isin(vuln_filter) &
    df["Severity"].isin(severity_filter) &
    df["Tool"].isin(tool_filter) &
    (df["Risk Score"] >= risk_threshold)
]

# ---------------- HEADER ----------------
st.title("SARMF Interactive Explorer")
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
This system demonstrates a structured benchmarking framework for evaluating smart contract vulnerabilities
across multiple automated analysis tools.

It combines severity-driven risk scoring, comparative tool analysis, time-based trend exploration,
and machine learning based priority prediction to support research and decision-making in blockchain security.
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

# ---------------- TOP RISK HIGHLIGHT ----------------
st.subheader("Critical Risk Highlight")

if not filtered_df.empty:
    top_contract = filtered_df.sort_values("Risk Score", ascending=False).iloc[0]
    st.warning(
        f"Highest Risk Contract: {top_contract['Contract']} "
        f"({top_contract['Vulnerability']} | Severity: {top_contract['Severity']} | Tool: {top_contract['Tool']})"
    )
else:
    st.info("No data available for current filter settings.")

st.markdown("---")

# ---------------- DATA TABLE ----------------
st.subheader("Contract Data")

if filtered_df.empty:
    st.warning("No matching data")
else:
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# ---------------- ANALYSIS ----------------
st.subheader("Distribution Analysis")

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
    st.info("No ranking available.")

st.markdown("---")

# ---------------- TOOL COMPARISON ----------------
st.subheader("Tool Comparison")

if not filtered_df.empty:
    tool_compare = pd.crosstab(filtered_df["Tool"], filtered_df["Vulnerability"])
    st.dataframe(tool_compare, use_container_width=True)
else:
    st.info("No tool comparison available.")

st.markdown("---")

# ---------------- TOOL EFFECTIVENESS GRAPH ----------------
st.subheader("Tool Effectiveness")

if not filtered_df.empty:
    st.bar_chart(filtered_df["Tool"].value_counts())
else:
    st.info("No tool effectiveness data available.")

st.markdown("---")

# ---------------- MULTI-CONTRACT COMPARISON ----------------
st.subheader("Multi-Contract Comparison")

if not filtered_df.empty:
    compare_contracts = st.multiselect(
        "Select Multiple Contracts",
        options=filtered_df["Contract"].unique(),
        default=list(filtered_df["Contract"].unique())[:2]
    )

    compare_df = filtered_df[filtered_df["Contract"].isin(compare_contracts)]

    if not compare_df.empty:
        comparison_table = compare_df[["Contract", "Vulnerability", "Severity", "Tool", "Risk Score"]]
        st.dataframe(comparison_table, use_container_width=True)

        contract_risk = (
            compare_df.groupby("Contract")["Risk Score"]
            .max()
            .sort_values(ascending=False)
        )
        st.write("Risk Comparison Across Selected Contracts")
        st.bar_chart(contract_risk)
    else:
        st.info("Select at least one contract.")
else:
    st.info("No data available for contract comparison.")

st.markdown("---")

# ---------------- TIME-BASED ANALYSIS ----------------
st.subheader("Time-Based Analysis")

if not filtered_df.empty and filtered_df["Date"].notna().any():
    time_df = (
        filtered_df.groupby(filtered_df["Date"].dt.to_period("M").astype(str))
        .size()
        .reset_index(name="Count")
    )
    time_df = time_df.rename(columns={"Date": "Month"})
    time_df = time_df.set_index("Date") if "Date" in time_df.columns else time_df.set_index(time_df.columns[0])
    st.write("Monthly Distribution of Records")
    st.line_chart(time_df)
else:
    st.info("No valid date information available for time-based analysis.")

st.markdown("---")

# ---------------- ML MODEL ----------------
st.subheader("AI Model: Priority Prediction")

if not filtered_df.empty:
    X = filtered_df[["Vulnerability", "Severity", "Tool"]]
    y = filtered_df["Priority Class"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["Vulnerability", "Severity", "Tool"])
        ]
    )

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    model.fit(X, y)

    st.write("Test the AI model with custom inputs")

    pred_vuln = st.selectbox(
        "Test Vulnerability",
        sorted(df["Vulnerability"].dropna().unique()),
        key="pred_vuln"
    )
    pred_severity = st.selectbox(
        "Test Severity",
        ["Low", "Medium", "High"],
        key="pred_severity"
    )
    pred_tool = st.selectbox(
        "Test Tool",
        sorted(df["Tool"].dropna().unique()),
        key="pred_tool"
    )

    pred_input = pd.DataFrame([{
        "Vulnerability": pred_vuln,
        "Severity": pred_severity,
        "Tool": pred_tool
    }])

    prediction = model.predict(pred_input)[0]
    st.write(f"Predicted Priority Class: {prediction}")
else:
    st.info("Not enough data for AI prediction.")

st.markdown("---")

# ---------------- ANALYTICAL INTERPRETATION ----------------
st.subheader("Analytical Interpretation")

if not filtered_df.empty:
    most_common_vuln = filtered_df["Vulnerability"].value_counts().idxmax()
    most_used_tool = filtered_df["Tool"].value_counts().idxmax()

    st.write(f"Most frequent vulnerability: {most_common_vuln}")
    st.write(f"Most active tool: {most_used_tool}")

    st.write("""
The observed distribution suggests concentration of vulnerabilities in specific categories,
indicating recurring design weaknesses in smart contracts.

Comparative tool outputs show variability in coverage, reinforcing the need for multi-tool validation.
The machine learning model provides an additional decision-support layer by classifying contract cases
into higher or normal priority groups based on known patterns.
""")
else:
    st.info("No data available for interpretation.")

st.markdown("---")

# ---------------- CONTRACT INSPECTION ----------------
st.subheader("Contract Inspection")

selected_contract = None
vuln_val = None
severity_val = None
tool_val = None
risk_val = None

if not filtered_df.empty:
    selected_contract = st.selectbox(
        "Select Contract for Detailed Inspection",
        filtered_df["Contract"].unique(),
        key="inspection_contract"
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
else:
    st.info("No contracts available for inspection.")

st.markdown("---")

# ---------------- PDF FUNCTION ----------------
def create_pdf_report(contract, vuln, severity, tool, risk):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 60
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "SARMF-Bench Analysis Report")

    y -= 35
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Contract: {contract}")
    y -= 22
    pdf.drawString(50, y, f"Vulnerability: {vuln}")
    y -= 22
    pdf.drawString(50, y, f"Severity: {severity}")
    y -= 22
    pdf.drawString(50, y, f"Tool: {tool}")
    y -= 22
    pdf.drawString(50, y, f"Risk Score: {risk}")

    y -= 35
    pdf.drawString(50, y, "Summary:")
    y -= 22
    pdf.drawString(50, y, f"The contract shows {vuln} vulnerability with {severity} severity.")
    y -= 22
    pdf.drawString(50, y, "Recommendation: Further manual audit required.")

    y -= 35
    pdf.drawString(50, y, "Developed by:")
    y -= 22
    pdf.drawString(50, y, "Mohit Tiwari")
    y -= 22
    pdf.drawString(50, y, "Assistant Professor, Department of Computer Science")
    y -= 22
    pdf.drawString(50, y, "Bharati Vidyapeeth's College of Engineering, New Delhi")

    pdf.save()
    buffer.seek(0)
    return buffer

# ---------------- PDF DOWNLOAD ----------------
st.subheader("Generate PDF Report")

if selected_contract:
    pdf_file = create_pdf_report(
        selected_contract,
        vuln_val,
        severity_val,
        tool_val,
        risk_val
    )

    st.download_button(
        "Download PDF Report",
        pdf_file,
        file_name=f"{selected_contract}_report.pdf",
        mime="application/pdf"
    )
else:
    st.info("Select a contract first to generate report.")

st.markdown("---")

# ---------------- FINAL POSITIONING ----------------
st.info("Prototype system demonstrating AI-assisted benchmarking of smart contract vulnerabilities for research and decision support.")

# ---------------- FOOTER ----------------
st.write("SARMF Framework | Research Prototype System")
