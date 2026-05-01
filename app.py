import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sky-Graph Dashboard", page_icon="☁️", layout="wide")
st.title("☁️ Project Sky-Graph: Cloud Resilience Map")

@st.cache_data
def load_data():
    # Make sure your CSV is uploaded to Colab or generated in a previous cell!
    return pd.read_csv("skygraph_dataset.csv")

try:
    df = load_data()

    st.write("### Network Overview")
    col1, col2 = st.columns(2)
    col1.metric("Domains Scanned", len(df))
    col2.metric("Unique Providers Found", df['provider'].nunique())

    st.divider()

    st.write("### Infrastructure Market Share")
    provider_counts = df['provider'].value_counts()
    st.bar_chart(provider_counts)

except FileNotFoundError:
    st.error("⚠️ Dataset not found. Ensure 'skygraph_dataset.csv' is in the Colab file explorer.")
