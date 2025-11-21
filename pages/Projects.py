import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.title("📁 Projects Insights")

donations, projects, volunteers = load_data()

# Status chart
st.subheader("Projects by Status")
status_count = projects['status'].value_counts().reset_index()
status_count.columns = ['status', 'count']

fig = px.pie(status_count, names='status', values='count')
st.plotly_chart(fig, use_container_width=True)

# Beneficiaries by project
st.subheader("Beneficiaries per Project")
fig2 = px.bar(projects, x='project_name', y='beneficiaries')
st.plotly_chart(fig2, use_container_width=True)
