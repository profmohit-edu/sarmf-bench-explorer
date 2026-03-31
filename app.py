import streamlit as st
import pandas as pd
from datetime import datetime
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
st.set_page_config(page_title="SARMF-Bench Explorer", layout="wide")

# -------------------------------
# HEADER
# -------------------------------
st.title("SARMF-Bench Explorer")
st.subheader("AI-Assisted Smart Contract Vulnerability Benchmarking System")

st.markdown("""
**Mohit Tiwari**  
Assistant Professor, Department of Computer Science and Engineering  
Bharati Vidyapeeth's College of Engineering (BVCOE, Delhi)  

This system is powered by SARMF-Bench, a smart contract vulnerability benchmark that I independently designed, implemented, and maintain from my home research lab aligned with the Department of Computer Science and Engineering at BVCOE, Delhi.  

The dataset and framework are archived across multiple international repositories with DOI-backed accessibility:

- **Harvard Dataverse (Dataset DOI):** [https://doi.org/10.7910/DVN/0SP3OO](https://doi.org/10.7910/DVN/0SP3OO)  
- **Zenodo (Software / Framework DOI):** [https://doi.org/10.5281/zenodo.18754015](https://doi.org/10.5281/zenodo.18754015)  
- **IEEE DataPort (Primary Dataset DOI):** [https://doi.org/10.21227/zj4q-p934](https://doi.org/10.21227/zj4q-p934)  
- **Mendeley Data (Dataset DOI):** [https://doi.org/10.17632/kd3vcpnn9v.1](https://doi.org/10.17632/kd3vcpnn9v.1)  
- **Open Science Framework – OSF Project (Archive DOI):** [https://doi.org/10.17605/OSF.IO/EJWDC](https://doi.org/10.17605/OSF.IO/EJWDC)  
- **protocols.io (Method / Workflow DOI):** [https://doi.org/10.17504/protocols.io.bp216eyxdgqe/v1](https://doi.org/10.17504/protocols.io.bp216eyxdgqe/v1)  

**Academic Profiles:**  
- ORCID: [https://orcid.org/0000-0003-1836-3451](https://orcid.org/0000-0003-1836-3451)  
- Google Scholar: [https://scholar.google.com/citations?user=ZFRPBBcAAAAJ&hl=en](https://scholar.google.com/citations?user=ZFRPBBcAAAAJ&hl=en)  
- Scopus: [https://www.scopus.com/authid/detail.uri?authorId=24483852000](https://www.scopus.com/authid/detail.uri?authorId=24483852000)  
- Web of Science: [https://www.webofscience.com/wos/author/record/33087873](https://www.webofscience.com/wos/author/record/33087873)  
- Vidwan: [https://vidwan.inflibnet.ac.in/profile/293249](https://vidwan.inflibnet.ac.in/profile/293249)  
- ResearchGate: [https://www.researchgate.net/profile/Mohit-Tiwari-6](https://www.researchgate.net/profile/Mohit-Tiwari-6)  
- LinkedIn: [https://www.linkedin.com/in/mtiw](https://www.linkedin.com/in/mtiw)
""")

st.info(
    "Use the controls in the left sidebar to adjust severity weights and filter by tool/"
    "severity. The tabs below provide an overview dashboard, a demo AI classifier, and "
    "access to the full dataset."
)

st.divider()

# -------------------------------
# REAL DATA LOAD (SARMF-Bench CSV)
# -------------------------------
csv_file = "sarmf_bench_real.csv"  # expanded benchmark CSV

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Ensure required columns exist
    required = {"Contract", "Vulnerability", "Severity", "Tool"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    # Handle Date column (optional but preferred)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
    else:
        df["Date"] = pd.to_datetime("2026-01-01")

    return df

df = load_data(csv_file)

# -------------------------------
# SIDEBAR (INTERACTIVE SLIDERS)
# -------------------------------
st.sidebar.header("Severity Weights")

low_w = st.sidebar.slider("Weight: Low severity", 0, 5, 1)
med_w = st.sidebar.slider("Weight: Medium severity", 0, 5, 2)
high_w = st.sidebar.slider("Weight: High severity", 0, 5, 3)
crit_w = st.sidebar.slider("Weight: Critical severity", 0, 5, 4)

severity_map = {
    "Low": low_w,
    "Medium": med_w,
    "High": high_w,
    "Critical": crit_w,
}

df["Risk_Score"] = df["Severity"].map(severity_map)

st.sidebar.header("Filters")

tool_filter = st.sidebar.multiselect(
    "Tool",
    options=sorted(df["Tool"].unique()),
    default=sorted(df["Tool"].unique()),
)

severity_filter = st.sidebar.multiselect(
    "Severity",
    options=sorted(df["Severity"].unique()),
    default=sorted(df["Severity"].unique()),
)

filtered_df = df[(df["Tool"].isin(tool_filter)) & (df["Severity"].isin(severity_filter))]

st.sidebar.caption(
    "Adjust severity weights to change the risk scoring and use filters to focus on "
    "specific tools or severity levels."
)

# -------------------------------
# TABS
# -------------------------------
overview_tab, ai_tab, data_tab = st.tabs(["Overview dashboard", "AI & reports", "Full dataset"])

# -------------------------------
# OVERVIEW TAB
# -------------------------------
with overview_tab:
    st.subheader("Risk Overview")

    if filtered_df.empty:
        contracts_count = 0
        avg_risk = 0
        high_risk_cases = 0
    else:
        contracts_count = len(filtered_df)
        avg_risk = int(filtered_df["Risk_Score"].mean())
        high_risk_cases = (filtered_df["Risk_Score"] >= high_w).sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Contracts (filtered)", contracts_count)
    col2.metric("Unique vulnerabilities", filtered_df["Vulnerability"].nunique())
    col3.metric("Tools represented", filtered_df["Tool"].nunique())
    col4.metric("High-risk contracts", high_risk_cases)

    st.divider()

    st.subheader("Top risk contracts")
    if filtered_df.empty:
        st.warning("No records match the current filter selection.")
    else:
        top = filtered_df.sort_values(by="Risk_Score", ascending=False).head(10)
        st.dataframe(top, use_container_width=True)

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Vulnerability distribution**")
        if filtered_df.empty:
            st.info("No data for current filters.")
        else:
            st.bar_chart(filtered_df["Vulnerability"].value_counts().sort_values(ascending=False))

    with c2:
        st.markdown("**Tool usage**")
        if filtered_df.empty:
            st.info("No data for current filters.")
        else:
            st.bar_chart(filtered_df["Tool"].value_counts().sort_values(ascending=False))

    st.subheader("Time-based risk trend")
    if filtered_df.empty:
        st.info("No data for current filters.")
    else:
        time_data = filtered_df.groupby("Date")["Risk_Score"].mean()
        st.line_chart(time_data)

# -------------------------------
# AI & REPORTS TAB
# -------------------------------
@st.cache_resource
def train_model(df: pd.DataFrame, high_threshold: int):
    X = df[["Vulnerability", "Severity", "Tool"]]
    y = df["Risk_Score"] >= high_threshold

    preprocessor = ColumnTransformer(
        [("cat", OneHotEncoder(), ["Vulnerability", "Severity", "Tool"])]
    )

    model = Pipeline([
        ("prep", preprocessor),
        ("model", RandomForestClassifier(random_state=42)),
    ])

    model.fit(X, y)
    return model

with ai_tab:
    st.subheader("Demo: AI-based high-risk classifier")

    st.caption(
        "This classifier is trained on the current SARMF-Bench CSV using a "
        "Random Forest model and one-hot encoding. It predicts whether a given "
        "Vulnerability / Severity / Tool combination is likely to be high risk."
    )

    model = train_model(df, high_w)

    v = st.selectbox("Vulnerability", sorted(df["Vulnerability"].unique()))
    s = st.selectbox("Severity", sorted(df["Severity"].unique()))
    t = st.selectbox("Tool", sorted(df["Tool"].unique()))

    input_df = pd.DataFrame([[v, s, t]], columns=["Vulnerability", "Severity", "Tool"])
    pred = model.predict(input_df)[0]

    # Safe probability handling (works even if model saw only one class)
    proba = None
    if hasattr(model, "predict_proba"):
        all_proba = model.predict_proba(input_df)[0]
        classes = list(model.classes_)
        if True in classes and len(all_proba) == len(classes):
            pos_idx = classes.index(True)
            proba = all_proba[pos_idx]

    st.write("Prediction:", "High risk" if pred else "Normal")
    if proba is not None:
        st.write(f"Estimated probability of high risk: {proba:.2f}")
    else:
        st.caption(
            "Probability not shown because the model saw only one class with the current "
            "severity weights or does not expose calibrated probabilities."
        )

    st.divider()

    st.subheader("Export current view as PDF")

    def create_pdf():
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        c.drawString(50, 800, "SARMF-Bench Risk Report")

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.drawString(50, 780, f"Generated on: {now_str}")

        # Use filtered view for summary
        total_records = len(filtered_df)
        avg_risk_pdf = int(filtered_df["Risk_Score"].mean()) if total_records > 0 else 0

        c.drawString(50, 760, f"Total records (filtered): {total_records}")
        c.drawString(50, 740, f"Average risk (filtered): {avg_risk_pdf}")

        c.drawString(50, 720, f"Tools: {', '.join(tool_filter) if tool_filter else 'None selected'}")
        c.drawString(50, 700, f"Severities: {', '.join(severity_filter) if severity_filter else 'None selected'}")

        c.drawString(50, 660, "Developed by Mohit Tiwari, BVCOE, Delhi")
        c.save()

        buffer.seek(0)
        return buffer

    st.download_button(
        "Download PDF report",
        data=create_pdf(),
        file_name="sarmf_report.pdf",
    )

# -------------------------------
# FULL DATASET TAB
# -------------------------------
with data_tab:
    st.subheader("Dataset (filtered view)")
    if filtered_df.empty:
        st.info("No records match the current filter selection.")
    else:
        st.dataframe(filtered_df, use_container_width=True)

    st.caption(
        "SARMF-Bench Explorer is a personal research tool from my independent home lab, "
        "built to showcase a DOI-backed smart contract vulnerability benchmark curated "
        "at the Department of Computer Science and Engineering, BVCOE, Delhi."
    )
