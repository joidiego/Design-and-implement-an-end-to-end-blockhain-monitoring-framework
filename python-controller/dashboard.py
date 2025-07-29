import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Blockchain Anomaly Monitor", layout="wide")
st.title("🚨 Blockchain Anomaly Monitor")

# Ambil data dari FastAPI
@st.cache_data(ttl=5)
def load_data():
    try:
        anomalies = requests.get("http://localhost:8000/anomalies").json()
        return pd.DataFrame(anomalies)
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Belum ada data anomali.")
else:
    st.subheader("Daftar Anomali Terkini")
    st.dataframe(df[["txid", "r", "s", "block", "time", "entropy_r", "entropy_s"]].head(10))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Entropi r dan s")
        fig = px.line(df.tail(50), x="time", y=["entropy_r", "entropy_s"], title="Entropi Tanda Tangan")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribusi r vs s")
        fig2 = px.scatter(df.tail(100), x="r", y="s", color="block", title="Distribusi (r, s)")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Jumlah Anomali")
    count = len(df)
    st.metric("Total Anomali Terdeteksi", count)