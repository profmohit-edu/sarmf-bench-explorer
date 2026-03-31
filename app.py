import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# -------------------------------
# CREATE CSV (150 RECORDS)
# -------------------------------
csv_file = "sarmf_data.csv"

if not os.path.exists(csv_file):
    contracts = [f"Contract_{i}.sol" for i in range(1, 151)]

    vulnerabilities = [
        "Reentrancy", "Integer Overflow", "Access Control",
        "Front Running", "Timestamp Dependency",
        "Denial of Service", "Unchecked Call",
        "Weak Randomness", "Price Manipulation"
    ]

    severities = ["Low", "Medium", "High", "Critical"]
    tools = ["Slither", "Mythril", "Oyente"]

    gas_impact = ["Low", "Medium", "High"]
    exploitability = ["Low", "Medium", "High", "Critical"]
    categories = ["Security", "Financial", "Arithmetic", "Authorization", "Availability"]

    start_date = datetime(2026, 1, 1)

    rows = []

    for i in range(150):
        row = {
            "Contract": contracts[i],
            "Vulnerability": random.choice(vulnerabilities),
            "Severity": random.choice(severities),
            "Tool": random.choice(tools),
            "Date": (start_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "Risk_Score": random.randint(30, 100),
            "Gas_Impact": random.choice(gas_impact),
            "Exploitability": random.choice(exploitability),
            "Category": random.choice(categories)
        }
        rows.append(row)

    pd.DataFrame(rows).to_csv(csv_file, index=False)

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv(csv_file)
df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------
# UI
# -------------------------------
st.set_page_config(layout="wide")
st.title("🔐 SARMF-Bench Explorer")
st.subheader("AI-Assisted Smart Contract Vulnerability Benchmarking System")

# -------------------------------
# SIDEBAR
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
col2.metric("Avg Risk", int(filtered_df["Risk_Score"].mean()))
col3.metric("High Risk", len(filtered_df[filtered_df["Risk_Score"] > 80]))

st.divider()

# -------------------------------
# TOP RISK
# -------------------------------
st.subheader("🔥 Top Risk Contracts")
top = filtered_df.sort_values(by="Risk_Score", ascending=False).head(10)
st.dataframe(top)

# -------------------------------
# TOOL GRAPH
# -------------------------------
st.subheader("📊 Tool Effectiveness")

fig1, ax1 = plt.subplots()
filtered_df.groupby("Tool")["Risk_Score"].mean().plot(kind="bar", ax=ax1)
st.pyplot(fig1)

# -------------------------------
# TIME ANALYSIS
# -------------------------------
st.subheader("📅 Time Analysis")

time_data = filtered_df.groupby("Date")["Risk_Score"].mean()

fig2, ax2 = plt.subplots()
time_data.plot(ax=ax2)
st.pyplot(fig2)

# -------------------------------
# MULTI CONTRACT
# -------------------------------
st.subheader("📊 Multi-Contract Comparison")

selected = st.multiselect("Select Contracts", df["Contract"].unique())

if selected:
    comp = df[df["Contract"].isin(selected)]
    fig3, ax3 = plt.subplots()
    for c in selected:
        subset = comp[comp["Contract"] == c]
        ax3.plot(subset["Tool"], subset["Risk_Score"], label=c)
    ax3.legend()
    st.pyplot(fig3)

# -------------------------------
# AI MODEL
# -------------------------------
st.subheader("🤖 AI Prediction")

X = df[["Vulnerability", "Severity", "Tool"]]
y = df["Risk_Score"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(), ["Vulnerability", "Severity", "Tool"])
    ]
)

model = Pipeline(steps=[
    ("prep", preprocessor),
    ("model", RandomForestClassifier())
])

model.fit(X, y > 70)

test_v = st.selectbox("Vulnerability", df["Vulnerability"].unique())
test_s = st.selectbox("Severity", df["Severity"].unique())
test_t = st.selectbox("Tool", df["Tool"].unique())

test_input = pd.DataFrame([[test_v, test_s, test_t]],
                          columns=["Vulnerability", "Severity", "Tool"])

pred = model.predict(test_input)[0]

st.write("Prediction:", "High Risk" if pred else "Low Risk")

# -------------------------------
# PDF
# -------------------------------
st.subheader("📄 PDF Export")

def create_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(50, 800, "SARMF Report")
    c.drawString(50, 780, f"Total Records: {len(df)}")
    c.drawString(50, 760, f"Average Risk: {int(df['Risk_Score'].mean())}")
    c.save()
    buffer.seek(0)
    return buffer

pdf = create_pdf()

st.download_button("Download PDF", pdf, file_name="report.pdf")

# -------------------------------
# DATA
# -------------------------------
st.subheader("📄 Full Data")
st.dataframe(filtered_df)
