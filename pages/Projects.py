import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os

# ================
#  PAGE CONFIG
# ================
st.set_page_config(layout="wide")
st.title("Projects Dashboard")

# ======================
# Load Data
# ======================


df = pd.read_csv("data/projects.csv")

# ======================
#  STYLING
# ======================
st.markdown("""
<style>
.kpi-card {
    padding: 20px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(255,255,255,0.80), rgba(255,255,255,0.45));
    border: 1px solid rgba(0,0,0,0.1);
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    text-align: center;
}
.kpi-title {
    font-size: 13px;
    font-weight: 600;
}
.kpi-value {
    font-size: 22px;
    font-weight: 700;
    color: #0f4c75;
}
</style>
""", unsafe_allow_html=True)

# ======================
# KPIs
# ======================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Projects</div>
        <div class="kpi-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Active Projects</div>
        <div class="kpi-value">{(df['status'] == "Ongoing").sum()}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Beneficiaries</div>
        <div class="kpi-value">{df['beneficiaries'].sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ======================
# Filters
# ======================
st.subheader("Filter Projects")

col1, col2, col3 = st.columns(3)

with col1:
    region_filter = st.selectbox(
        "Region",
        ["All"] + sorted(df["region"].unique().tolist())
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        ["All"] + sorted(df["status"].unique().tolist())
    )

with col3:
    search_keyword = st.text_input("Search Project Name", "").strip().lower()

# Apply filters
filtered_df = df.copy()

if region_filter != "All":
    filtered_df = filtered_df[filtered_df["region"] == region_filter]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]

if search_keyword:
    filtered_df = filtered_df[
        filtered_df["project_name"].str.lower().str.contains(search_keyword)
    ]

# ======================
# Display Table
# ======================
st.subheader("Project List")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

st.markdown("---")

# ======================
# PROJECT COUNT BY REGION
# ======================
st.subheader("📍 Project Distribution by Region")

region_count = df["region"].value_counts().reset_index()
region_count.columns = ["region", "count"]

fig = px.bar(
    region_count,
    x="region", y="count",
    title="Projects Per Region",
    text="count"
)

st.plotly_chart(fig, use_container_width=True)

# ======================
# PROJECT STATUS DISTRIBUTION
# ======================
st.subheader("📊 Project Status Breakdown")

status_count = df["status"].value_counts().reset_index()
status_count.columns = ["status", "count"]

fig2 = px.pie(
    status_count,
    names="status",
    values="count",
    title="Status Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------------------
#             LAST DASHBOARD UPDATE
# --------------------------------------------------------------
# Get the last modified time of the data file
file_path = "data/projects.csv"
last_modified_timestamp = os.path.getmtime(file_path)
last_modified = datetime.datetime.fromtimestamp(last_modified_timestamp)

# Format nicely
formatted_time = last_modified.strftime('%b %d, %Y, %H:%M:%S')

# Footer
st.markdown(
    f"""
    <style>
    .footer {{
        position: fixed;
        bottom: 10px;
        right: 20px;
        font-size: 12px;
        color: #888888;
        z-index: 100;
    }}
    </style>
    <div class="footer">🕒 Data last updated: {formatted_time}</div>
    """,
    unsafe_allow_html=True
)