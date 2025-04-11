import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 📌 GitHub raw CSV URL
csv_url = "https://raw.githubusercontent.com/Himanshu-hub21/Task_Tracker/main/data/tasks.csv"

# 📥 Load data with cache (15 min TTL)
@st.cache_data(ttl=900)
def load_data():
    response = requests.get(csv_url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        return None

# 🚀 Streamlit App
st.set_page_config(page_title="Task Tracker", layout="wide")
st.title("✅ Task Tracker Dashboard")

# 🔄 Load data with spinner
with st.spinner("Loading task data..."):
    df = load_data()

if df is not None:
    # 🧾 Show entire dataset
    st.subheader("📋 All Tasks")
    st.dataframe(df, use_container_width=True)

    # 🎯 Filter by task status
    status_options = ["All"] + df["Status"].dropna().unique().tolist()
    status_filter = st.selectbox("🔎 Filter by Status", status_options)

    if status_filter != "All":
        filtered_df = df[df["Status"] == status_filter]
    else:
        filtered_df = df

    st.write(f"Showing {len(filtered_df)} task(s)")
    st.dataframe(filtered_df, use_container_width=True)

    # 📊 Status breakdown
    st.subheader("📈 Task Status Breakdown")
    status_count = df["Status"].value_counts()
    st.bar_chart(status_count)

else:
    st.error("❌ Failed to load data from GitHub. Please check the CSV URL or try again later.")
