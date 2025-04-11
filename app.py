import streamlit as st
import pandas as pd
import requests
from io import StringIO

# URL of the raw CSV file on GitHub
csv_url = "https://raw.githubusercontent.com/Himanshu-hub21/Task_Tracker/main/data/tasks.csv"

# Fetch the CSV data from GitHub
@st.cache
def load_data():
    response = requests.get(csv_url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Error loading data from GitHub")
        return None

# Load data
df = load_data()

if df is not None:
    # Display the data
    st.title("Task Tracker Dashboard")

    # Show the entire dataset
    st.subheader("All Tasks")
    st.write(df)

    # Filters for Pending Tasks (or other statuses)
    status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])

    if status_filter != "All":
        filtered_df = df[df["Status"] == status_filter]
        st.write(filtered_df)
    else:
        st.write(df)

    # Display count of tasks by status
    st.subheader("Task Status Breakdown")
    status_count = df["Status"].value_counts()
    st.bar_chart(status_count)
