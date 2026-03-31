import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="SARMF Explorer", layout="wide")

# -------------------------------
# HEADER
# -------------------------------
st.title("SARMF-Bench Explorer")
st.subheader("AI-Assisted Smart Contract Vulnerability Benchmarking System")

st.markdown("""
**Mohit Tiwari**  
Assistant Professor, Department of Computer Science  
Bharati Vidyapeeth's College of Engineering, New Delhi  

**Academic Profiles:**  
- [ORCID](https://orcid.org/0000-0003-1836-3451)  
- [Google Scholar](https://scholar.google.com/citations?user=ZFRPBBcAAAAJ&hl=en)  
- [Scopus](https://www.scopus.com/authid/detail.uri?authorId=24483852000)  
- [Web of Science](https://www.webofscience.com/wos/author/record/33087873)  
- [Vidwan](https://vidwan.inflibnet.ac.in/profile/293249)  
- [ResearchGate](https://www.researchgate.net/profile/Mohit-Tiwari-6)  
- [LinkedIn](https://www.linkedin.com/in/mtiw)
""")

st.divider()

# -------------------------------
# DATA GENERATION (150 RECORDS)
# -------------------------------
csv_file = "sarmf_data.csv"

if not os.path.exists(csv_file):
    contracts = [f"Contract_{i}.sol" for i in range(1, 151)]
    vulnerabilities = ["Reentrancy", "Overflow", "Access Control", "Front Running", "DoS"]
    severities = ["Low", "Medium", "High", "Critical"]
    tools = ["Slither", "Mythril", "Oyente"]

    rows = []
    start_date = datetime(2026, 1, 1)

    for i in range(150):
        rows.append({
            "Contract": contracts[i],
            "Vulnerability": random.choice(vulnerabilities),
            "Severity": random.choice(severities),
            "Tool": random.choice(tools),
            "Date": (start_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "Risk_Score": random.randint(30, 100)
        })

    pd.DataFrame(rows).to_csv(csv_file, index=False)

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv(csv_file)
df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

tool_filter = st.sidebar.multiselect("Tool", df["Tool"].unique(), default=df["Tool"].unique())
severity_filter = st.sidebar.multiselect("Severity", df["Severity"].unique(), default=df["Severity"].unique())

filtered_df = df[(df["Tool"].isin(tool_filter)) & (df["Severity"].isin(severity_filter))]

# -------------------------------
# METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Contracts", len(filtered_df))
col2.metric("Average Risk Score", int(filtered_df["Risk_Score"].mean()))
col3.metric("High Risk Cases", len(filtered_df[filtered_df["Risk_Score"] > 80]))

st.divider()

# -------------------------------
# TOP RISK CONTRACTS
# -------------------------------
st.subheader("Top Risk Contracts")

top = filtered_df.sort_values(by="Risk_Score", ascending=False).head(10)
st.dataframe(top, use_container_width=True)

# -------------------------------
# VISUAL ANALYTICS
# -------------------------------
st.subheader("Vulnerability Distribution")
st.bar_chart(filtered_df["Vulnerability"].value_counts())

st.subheader("Tool Usage")
st.bar_chart(filtered_df["Tool"].value_counts())

# -------------------------------
# TIME ANALYSIS
# -------------------------------
st.subheader("Time-Based Risk Trend")

time_data = filtered_df.groupby("Date")["Risk_Score"].mean()
st.line_chart(time_data)

st.divider()

# -------------------------------
# AI MODEL
# -------------------------------
st.subheader("AI-Based Risk Prediction")

X = df[["Vulnerability", "Severity", "Tool"]]
y = df["Risk_Score"]

preprocessor = ColumnTransformer(
    [("cat", OneHotEncoder(), ["Vulnerability", "Severity", "Tool"])]
)

model = Pipeline([
    ("prep", preprocessor),
    ("model", RandomForestClassifier())
])

model.fit(X, y > 70)

v = st.selectbox("Vulnerability", df["Vulnerability"].unique())
s = st.selectbox("Severity", df["Severity"].unique())
t = st.selectbox("Tool", df["Tool"].unique())

pred = model.predict(pd.DataFrame([[v, s, t]],
                                 columns=["Vulnerability", "Severity", "Tool"]))[0]

st.write("Prediction:", "High Risk" if pred else "Normal")

st.divider()

# -------------------------------
# PDF EXPORT
# -------------------------------
st.subheader("Export Report")

def create_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.drawString(50, 800, "SARMF Report")
    c.drawString(50, 780, f"Total Records: {len(df)}")
    c.drawString(50, 760, f"Average Risk: {int(df['Risk_Score'].mean())}")

    c.drawString(50, 720, "Developed by Mohit Tiwari")
    c.save()

    buffer.seek(0)
    return buffer

st.download_button("Download PDF", create_pdf(), "sarmf_report.pdf")

# -------------------------------
# FULL DATA
# -------------------------------
st.subheader("Dataset")
st.dataframe(filtered_df, use_container_width=True)
