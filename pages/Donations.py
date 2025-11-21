import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os



# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(layout="wide")
st.title("Donation Analytics Dashboard")


@st.cache_data(ttl=4)
def load_data():
    return pd.read_csv("data/donations.csv")

df = load_data()


# Load data
df = pd.read_csv("data/donations.csv")
df["date"] = pd.to_datetime(df["date"])

# --------------------------------------------------------------
#                     KEY METRICS
# --------------------------------------------------------------


st.markdown("""
<style>

.kpi-card {
    padding: 28px;
    height: 150px; /* increase card height */
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(255,255,255,0.75), rgba(255,255,255,0.35));
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.45);
    box-shadow: 0 10px 22px rgba(0,0,0,0.10);
    transition: all 0.25s ease-in-out;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 32px rgba(0,0,0,0.12);
}

.kpi-title {
    font-size: 12px;
    font-weight: 600;
    color: #1d2433;
    opacity: 0.9;
    text-align: center;
    white-space: nowrap; /* prevents wrapping */
}

.kpi-value {
    font-size: 12px;
    font-weight: 700;
    margin-top: 10px;
    text-align: center;
    background: linear-gradient(90deg, #0f4c75, #3282b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    white-space: nowrap; /* prevents wrapping */
}

</style>
""", unsafe_allow_html=True)


st.subheader("Key Insights for Donations")

# WIDER COLUMNS
c1, c2, c3, c4, c5 = st.columns([1.1, 1.1, 1.1, 1.1, 1.1])


with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 Total Donations</div>
        <div class="kpi-value">{df['donation_amount'].sum():,.0f} SAR</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🧑‍🤝‍🧑 Unique Donors</div>
        <div class="kpi-value">{df['donor_name'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📦 Avg Donation</div>
        <div class="kpi-value">{df['donation_amount'].mean():,.2f} SAR</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📍 Top Region</div>
        <div class="kpi-value">{df.groupby("region")["donation_amount"].sum().idxmax()}</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🎯 Top Project</div>
        <div class="kpi-value">{df.groupby("project")["donation_amount"].sum().idxmax()}</div>
    </div>
    """, unsafe_allow_html=True)



# --------------------------------------------------------------
#                   DONATION TRENDS OVER TIME
# --------------------------------------------------------------
st.subheader("📅 Daily Donation Trend")

daily = df.groupby("date")["donation_amount"].sum().reset_index()

fig1 = px.line(
    daily, x="date", y="donation_amount",
    markers=True, title="Daily Donation Trend"
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --------------------------------------------------------------
#                 DONOR RETENTION RATE
# --------------------------------------------------------------
st.subheader("🔁 Donor Retention Rate")

donor_counts = df.groupby("donor_name")["date"].nunique()
repeat_donors = (donor_counts > 1).sum()
retention_rate = repeat_donors / len(donor_counts) * 100

st.metric("Retention Rate (%)", f"{retention_rate:.1f}%")

st.caption("Percentage of donors who donated more than once.")

st.markdown("---")

# --------------------------------------------------------------
#                 TOP 10 DONORS
# --------------------------------------------------------------
st.subheader("🏆 Top 10 Donors")

top_donors = df.groupby("donor_name")["donation_amount"].sum().nlargest(10).reset_index()

fig2 = px.bar(
    top_donors,
    x="donor_name",
    y="donation_amount",
    title="Top 10 Donors",
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --------------------------------------------------------------
#             HEATMAP: MONTH × REGION
# --------------------------------------------------------------
# show the number of donations across months and regions
st.subheader("🌡️ Donation Heatmap (Month × Region)")

df["month"] = df["date"].dt.to_period("M").astype(str)

heatmap = df.groupby(["month", "region"])["donation_amount"].sum().reset_index()
pivot = heatmap.pivot(index="region", columns="month", values="donation_amount")

fig3 = px.imshow(
    pivot,
    aspect="auto",
    text_auto=True,
    color_continuous_scale="Blues",
    title="Donations by Month and Region"
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --------------------------------------------------------------
#                 PEAK DONATION DAYS
# --------------------------------------------------------------
st.subheader("📈 Peak Donation Days")

top_days = daily.nlargest(10, "donation_amount")

fig4 = px.bar(
    top_days,
    x="date",
    y="donation_amount",
    title="Top Donation Days"
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# --------------------------------------------------------------
#             SEASONAL TRENDS (Monthly Trend)
# --------------------------------------------------------------
st.subheader("📆 Seasonal Trends (Monthly)")

monthly = df.groupby(df["date"].dt.to_period("M").astype(str))["donation_amount"].sum().reset_index()

fig5 = px.line(
    monthly,
    x="date",
    y="donation_amount",
    markers=True,
    title="Monthly Donation Trend"
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# --------------------------------------------------------------
#             Donation DISTRIBUTION by region pie chart
# --------------------------------------------------------------
st.subheader("🌍 Donation Distribution by Region")
region_dist = df.groupby("region")["donation_amount"].sum().reset_index()
fig = px.pie(region_dist, values="donation_amount", names="region", title="Donation Distribution by Region")
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------
#             Donation DISTRIBUTION by Project pie chart
# --------------------------------------------------------------
st.subheader("📁 Donation Distribution by Project")
project_dist = df.groupby("project")["donation_amount"].sum().reset_index()
fig = px.pie(project_dist, values="donation_amount", names="project", title="Donation Distribution by Project")
st.plotly_chart(fig, use_container_width=True)








# --------------------------------------------------------------
#             ANOMALY DETECTION (Donation Spikes)
# --------------------------------------------------------------
st.subheader("⚠️ Anomaly Detection (Spikes)")

mean_val = daily["donation_amount"].mean()
std_val = daily["donation_amount"].std()

# A spike = value > mean + 2*std
daily["is_spike"] = daily["donation_amount"] > mean_val + 2 * std_val

fig6 = go.Figure()

fig6.add_trace(
    go.Scatter(
        x=daily["date"],
        y=daily["donation_amount"],
        mode="lines+markers",
        name="Donations",
    )
)

spikes = daily[daily["is_spike"]]

fig6.add_trace(
    go.Scatter(
        x=spikes["date"],
        y=spikes["donation_amount"],
        mode="markers",
        marker=dict(size=12, color="red"),
        name="Spike",
    )
)

fig6.update_layout(title="Donation Spikes Detected")

st.plotly_chart(fig6, use_container_width=True)


# --------------------------------------------------------------
#             LAST DASHBOARD UPDATE
# --------------------------------------------------------------
# Get the last modified time of the data file
file_path = "data/donations.csv"
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