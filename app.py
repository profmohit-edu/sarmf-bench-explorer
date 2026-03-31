import streamlit as st
import pandas as pd

st.title("SARMF-Bench Explorer")
st.write("Developed by Mohit Tiwari")

data = {
    "Contract": ["C1", "C2", "C3"],
    "Vulnerability": ["Reentrancy", "Overflow", "Access Control"],
    "Severity": ["High", "Medium", "High"]
}

df = pd.DataFrame(data)

st.dataframe(df)
