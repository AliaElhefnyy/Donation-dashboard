import streamlit as st

st.set_page_config(page_title="Non-Profit Dashboard", layout="wide")

# ---------- HEADER ----------
st.title("Donations & Volunteers Analytics Dashboard")
st.markdown("""
Welcome to the central analytics hub designed for non-profit organizations.  
This dashboard provides **real-time insights** into donations, volunteer engagement, and project impact.
""")

st.markdown("---")

# ---------- CARDS ----------
st.subheader("Quick Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
        padding: 20px; 
        border-radius: 15px; 
        background-color: #f0f2f6;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    ">
        <h3 style="margin-bottom:10px;">💰 Donations</h3>
        <p>Track donation amounts, donor trends, and time-based contributions.</p>
        <a style="text-decoration:none;" href="/Donations">
            👉 <b>Go to Donations Dashboard</b>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        padding: 20px; 
        border-radius: 15px; 
        background-color: #f0f2f6;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    ">
        <h3 style="margin-bottom:10px;">🤝 Volunteers</h3>
        <p>See hours contributed, engagement levels, and volunteer impact.</p>
        <a style="text-decoration:none;" href="/Volunteers">
            👉 <b>Go to Volunteers Page</b>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        padding: 20px; 
        border-radius: 15px; 
        background-color: #f0f2f6;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    ">
        <h3 style="margin-bottom:10px;">📁 Projects</h3>
        <p>View active, completed, and upcoming projects with key metrics.</p>
        <a style="text-decoration:none;" href="/Projects">
            👉 <b>Go to Projects Premium Page</b>
        </a>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")

# ---------- ABOUT SECTION ----------
st.subheader("About This Dashboard")
st.write("""
This dashboard was built to support non-profits in making data-driven decisions.  
It includes:
- Donation tracking and trend analysis  
- Volunteer performance and engagement insights  
- Project monitoring with status and regional distribution  
- Interactive visualizations for easy exploration
- Real-time data updates
- Filterable views by region, time, and project status
- Auto-updated data from CSV files  
- Timestamp of last data update


If you would like to extend the dashboard, feel free to navigate through the sidebar.
""")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<center>Developed by <b>Alia Elhefny</b> — AI Engineer | Data Analyst</center>",
    unsafe_allow_html=True
)
