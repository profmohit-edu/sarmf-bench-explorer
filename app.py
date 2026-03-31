import io
import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="SARMF Interactive Explorer", layout="wide")

# ---------------- LOAD CSV ----------------
try:
    df = pd.read_csv("sarmf_dataset.csv")
except Exception as e:
    st.error("CSV NOT FOUND")
    st.write(e)
    st.stop()

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.title("Interactive Controls")

# 🎯 AI Risk Weight Control
st.sidebar.subheader("Risk Weighting")

low_w = st.sidebar.slider("Low Severity Weight", 0, 5, 1)
med_w = st.sidebar.slider("Medium Severity Weight", 0, 5, 2)
high_w = st.sidebar.slider("High Severity Weight", 0, 5, 3)

severity_map = {
    "Low": low_w,
    "Medium": med_w,
    "High": high_w
}

df["Risk Score"] = df["Severity"].map(severity_map)

# 🎯 Tool Toggle
tool_filter = st.sidebar.multiselect(
    "Select Tools",
    df["Tool"].unique(),
    default=df["Tool"].unique()
)

# 🎯 Risk Threshold Filter
risk_threshold = st.sidebar.slider("Minimum Risk Score", 0, 5, 0)

filtered_df = df[
    (df["Tool"].isin(tool_filter)) &
    (df["Risk Score"] >= risk_threshold)
]

# ---------------- HEADER ----------------
st.title("SARMF Interactive Explorer")
st.subheader("AI-Driven Smart Contract Benchmarking System")

st.markdown("---")

# ---------------- LIVE FEEDBACK ----------------
st.subheader("Live System Behavior")

st.write(f"""
Current Configuration:
- Low Weight: {low_w}
- Medium Weight: {med_w}
- High Weight: {high_w}
- Risk Threshold: {risk_threshold}
""")

# ---------------- OVERVIEW ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Contracts", filtered_df["Contract"].nunique())
col2.metric("Records", len(filtered_df))
col3.metric("Avg Risk", round(filtered_df["Risk Score"].mean(), 2) if not filtered_df.empty else 0)

# ---------------- TOP RISK ----------------
st.subheader("Top Risk Contract")

if not filtered_df.empty:
    top = filtered_df.sort_values("Risk Score", ascending=False).iloc[0]
    st.warning(f"{top['Contract']} → {top['Vulnerability']} (Risk: {top['Risk Score']})")

# ---------------- WHAT-IF SIMULATION ----------------
st.subheader("What-if Simulation")

if not filtered_df.empty:
    contract = st.selectbox("Select Contract to Modify", filtered_df["Contract"].unique())

    row = filtered_df[filtered_df["Contract"] == contract].iloc[0]

    new_severity = st.selectbox("Change Severity", ["Low", "Medium", "High"])

    simulated_score = severity_map[new_severity]

    st.write("Original Severity:", row["Severity"])
    st.write("New Severity:", new_severity)
    st.write("New Risk Score:", simulated_score)

# ---------------- CHARTS ----------------
st.subheader("Dynamic Analysis")

col1, col2 = st.columns(2)

with col1:
    st.write("Vulnerability Distribution")
    if not filtered_df.empty:
        st.bar_chart(filtered_df["Vulnerability"].value_counts())

with col2:
    st.write("Tool Effectiveness")
    if not filtered_df.empty:
        st.bar_chart(filtered_df["Tool"].value_counts())

# ---------------- RANKING ----------------
st.subheader("Top Risk Ranking")

if not filtered_df.empty:
    ranking = (
        filtered_df.groupby("Contract", as_index=False)["Risk Score"]
        .max()
        .sort_values("Risk Score", ascending=False)
    )
    st.dataframe(ranking)

# ---------------- TABLE ----------------
st.subheader("Dataset View")

st.dataframe(filtered_df, use_container_width=True)

# ---------------- PDF ----------------
def create_pdf(contract, vuln, severity, tool, risk):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    y = 800
    pdf.drawString(50, y, "SARMF Interactive Report")
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

st.subheader("Export Report")

if not filtered_df.empty:
    c = st.selectbox("Select Contract for Report", filtered_df["Contract"].unique())
    r = filtered_df[filtered_df["Contract"] == c].iloc[0]

    pdf = create_pdf(c, r["Vulnerability"], r["Severity"], r["Tool"], r["Risk Score"])

    st.download_button("Download PDF", pdf, file_name=f"{c}_report.pdf")

# ---------------- FINAL ----------------
st.info("Interactive benchmarking system with AI-assisted risk modeling.")
