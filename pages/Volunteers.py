import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import os

# ======================
# PAGE SETTINGS
# ======================
st.set_page_config(layout="wide")
st.title(" Volunteers Dashboard")

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("data/volunteers.csv")
# Columns needed:
# volunteer_name, hours_contributed, project, region

# ======================
# STYLING
# ======================
st.markdown("""
<style>
.kpi-card {
    padding: 20px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(255,255,255,0.5));
    border: 1px solid rgba(0,0,0,0.08);
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    text-align: center;
    margin-bottom: 15px;
}
.kpi-title {
    font-size: 14px;
    font-weight: 600;
}
.kpi-value {
    font-size: 22px;
    font-weight: 700;
    color: #1b2a49;
}
</style>
""", unsafe_allow_html=True)

# ======================
# KPI SECTION
# ======================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Volunteers</div>
        <div class="kpi-value">{df['volunteer_name'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Volunteer Hours</div>
        <div class="kpi-value">{df['hours_contributed'].sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Avg Hours per Volunteer</div>
        <div class="kpi-value">{df['hours_contributed'].mean():.1f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ======================
# FILTERS
# ======================
st.subheader("Filter Volunteers")

col1, col2, col3, col4 = st.columns(4)

with col1:
    region_filter = st.selectbox(
        "Region",
        ["All"] + sorted(df["region"].unique().tolist())
    )

with col2:
    project_filter = st.selectbox(
        "Project",
        ["All"] + sorted(df["project"].unique().tolist())
    )

with col3:
    search_filter = st.text_input("Search Volunteer Name").strip().lower()

# sort volunteers alphpabetically, working hrs descending, and working hrs ascending
with col4:
    sort_option = st.selectbox(
        "Sort By",
        ["Name (A-Z)", "Hours (High to Low)", "Hours (Low to High)"]
    )

if sort_option == "Name (A-Z)":
    df = df.sort_values("volunteer_name", ascending=True)
elif sort_option == "Hours (High to Low)":
    df = df.sort_values("hours_contributed", ascending=False)
elif sort_option == "Hours (Low to High)":
    df = df.sort_values("hours_contributed", ascending=True)
    
# Apply filters
filtered = df.copy()

if region_filter != "All":
    filtered = filtered[filtered["region"] == region_filter]

if project_filter != "All":
    filtered = filtered[filtered["project"] == project_filter]

if search_filter:
    filtered = filtered[
        filtered["volunteer_name"].str.lower().str.contains(search_filter)
    ]

# ======================
# VOLUNTEER TABLE
# ======================
st.subheader("Volunteer List")

st.dataframe(
    filtered,
    use_container_width=True,
    height=500
)

st.markdown("---")

# ======================
# LEADERBOARD
# ======================
st.subheader("🏆 Top Volunteers by Hours")

leaderboard = (
    df.groupby("volunteer_name")["hours_contributed"]
      .sum()
      .reset_index()
      .sort_values("hours_contributed", ascending=False)
)

fig = px.bar(
    leaderboard.head(10),
    x="volunteer_name",
    y="hours_contributed",
    title="Top 10 Volunteers",
    text="hours_contributed"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ======================
# HOURS DISTRIBUTION
# ======================
st.subheader("⏳ Hours Contributed by Region")

hours_region = (
    df.groupby("region")["hours_contributed"]
      .sum()
      .reset_index()
)

fig2 = px.pie(
    hours_region,
    names="region",
    values="hours_contributed",
    title="Hours Distribution by Region"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------------------
#             LAST DASHBOARD UPDATE
# --------------------------------------------------------------
# Get the last modified time of the data file
file_path = "data/volunteers.csv"
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
