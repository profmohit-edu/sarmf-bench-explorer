import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SARMF-Bench Dashboard", layout="wide")

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}

.main-title {
    font-size: 32px;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 16px;
    color: #6b7280;
    margin-bottom: 25px;
}

.card {
    background-color: white;
    padding: 18px;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.metric-box {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    text-align: center;
}

.metric-value {
    font-size: 22px;
    font-weight: 600;
    color: #111827;
}

.metric-label {
    font-size: 13px;
    color: #6b7280;
}

.dataframe th {
    background-color: #f9fafb !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">SARMF-Bench: Smart Contract Vulnerability Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interactive analysis of vulnerability patterns detected across smart contracts</div>', unsafe_allow_html=True)

# ---------------- LOAD CSV ----------------
try:
    df = pd.read_csv("sarmf_data.csv")
except:
    st.error("CSV file not found. Ensure 'sarmf_data.csv' is in the same folder.")
    st.stop()

# ---------------- METRICS ----------------
total_contracts = df['contract_name'].nunique()
total_issues = len(df)
unique_vulns = df['vulnerability'].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">{total_contracts}</div>
        <div class="metric-label">Total Contracts</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">{total_issues}</div>
        <div class="metric-label">Total Issues Detected</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-value">{unique_vulns}</div>
        <div class="metric-label">Unique Vulnerabilities</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- FILTER ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

selected_contract = st.selectbox(
    "Select Contract for Analysis",
    ["All"] + list(df['contract_name'].unique())
)

if selected_contract != "All":
    filtered_df = df[df['contract_name'] == selected_contract]
else:
    filtered_df = df

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TABLE ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Vulnerability Records")

st.dataframe(filtered_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CHART ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Vulnerability Distribution")

chart_data = filtered_df['vulnerability'].value_counts()
st.bar_chart(chart_data)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<hr style="margin-top:30px;">
<div style="text-align:center; font-size:13px; color:gray;">
SARMF Framework | Smart Contract Security Analysis Interface
</div>
""", unsafe_allow_html=True)
