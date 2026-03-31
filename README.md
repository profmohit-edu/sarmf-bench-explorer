# SARMF-Bench Explorer

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sarmfbenchexplorerbvcoend.streamlit.app/)

SARMF-Bench Explorer is an interactive web application for exploring **SARMF-Bench**, a reproducible smart contract vulnerability benchmark and cross-tool evaluation framework.  
The app provides a visual, filterable interface over a curated benchmark dataset, enabling researchers, students, and practitioners to understand vulnerability patterns and tool behaviour on Ethereum smart contracts.

Live app: **https://sarmfbenchexplorerbvcoend.streamlit.app/**

---

## 1. Purpose

Smart contract security tools often report inconsistent results across tools, versions, and environments, making it hard to compare their effectiveness fairly.  
**SARMF-Bench Explorer**:

- Turns the SARMF-Bench benchmark into a **clickable, web-based portal**.
- Allows **rapid exploration** of contracts, vulnerabilities, severities, tools, and risk scores.
- Demonstrates an **AI-assisted classifier** on top of the benchmark data.
- Serves as a **teaching and demonstration tool** for smart contract security, SWC patterns, and reproducible benchmarking.

The system is powered by SARMF-Bench, a smart contract vulnerability benchmark **independently designed, implemented, and maintained from an independent home research lab aligned with the Department of Computer Science and Engineering at BVCOE, Delhi.**

---

## 2. Features

- **Interactive dashboard**
  - Filter by vulnerability type, severity level, and analysis tool.
  - View top high-risk contracts based on user-defined severity weights.
  - Inspect vulnerability and tool usage distributions.
  - Analyze time-based risk trends.

- **Customizable risk scoring**
  - Adjustable weights for `Low`, `Medium`, `High`, and `Critical` severities.
  - Dynamic recomputation of risk scores and all visualizations.

- **AI-based high-risk classifier**
  - Random Forest model with one-hot encoding over vulnerability, severity, and tool.
  - Predicts whether a configuration is likely to be “High risk”.
  - Displays an estimated probability (where meaningful).

- **PDF reporting**
  - One-click export of a simple PDF “Risk Report” for the current filtered view.

- **DOI-backed benchmark data**
  - Backed by the **SARMF-Bench** dataset and framework, archived across multiple international repositories (see below).

---

## 3. SARMF-Bench DOIs and Resources

Core dataset and framework:

- **Harvard Dataverse (Dataset DOI):**  
  https://doi.org/10.7910/DVN/0SP3OO

- **Zenodo (Software / Framework DOI):**  
  https://doi.org/10.5281/zenodo.18754015

- **IEEE DataPort (Primary Dataset DOI):**  
  https://doi.org/10.21227/zj4q-p934

- **Mendeley Data (Dataset DOI):**  
  https://doi.org/10.17632/kd3vcpnn9v.1

- **Open Science Framework – OSF Project (Archive DOI):**  
  https://doi.org/10.17605/OSF.IO/EJWDC

- **protocols.io (Method / Workflow DOI):**  
  https://doi.org/10.17504/protocols.io.bp216eyxdgqe/v1

When using this app or the underlying benchmark in academic work, please **cite the dataset DOIs above** and (when available) the SARMF-Bench and SARMF-Bench Explorer papers.

---

## 4. Live Demo

The app is deployed on **Streamlit Community Cloud**:

> https://sarmfbenchexplorerbvcoend.streamlit.app/

You can use the live deployment to:

- Explore vulnerability distributions.
- Demonstrate SARMF-Bench in lectures and seminars.
- Share a zero-install reproduction of results.

---

## 5. Running Locally

### 5.1. Prerequisites

- Python 3.9+  
- Recommended tools: `git`, `virtualenv` or `conda`

### 5.2. Clone the repository

```bash
git clone https://github.com/profmohit-edu/sarmf-bench-explorer.git
cd sarmf-bench-explorer
```

### 5.3. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 5.4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5.5. Ensure benchmark CSV is present

The app expects a CSV file named **`sarmf_bench_real.csv`** in the repository root with columns:

```text
Contract,Vulnerability,Severity,Tool,Date
```

This repository already includes a pre-generated mini benchmark (~180 rows) aligned with SARMF-Bench naming and SWC categories.  
You can replace or expand this file with your own SARMF-Bench exports as long as the column structure is preserved.

### 5.6. Run the app

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (typically `http://localhost:8501`) in your browser.

---

## 6. Project Structure

```text
sarmf-bench-explorer/
│
├── app.py                  # Streamlit application
├── sarmf_bench_real.csv    # Benchmark CSV backing the explorer
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── LICENSE                 # Open source license (e.g., MIT/BSD/GPL)
```

---

## 7. Citation

If you use SARMF-Bench Explorer in your research, please cite:

[1] M. Tiwari, “SARMF-Bench Explorer v1.0 – AI-Assisted Smart Contract Vulnerability Benchmarking System”. Zenodo, Mar. 31, 2026. doi: 10.5281/zenodo.19354672.

---

## 8. Contact

For questions, suggestions, or collaboration:

- **Email:** mohit.tiwari@bharatividyapeeth.edu  
- **LinkedIn:** https://www.linkedin.com/in/mtiw  
- **Research profiles:** ORCID / Google Scholar / Scopus / Web of Science / Vidwan / ResearchGate (see links above).
