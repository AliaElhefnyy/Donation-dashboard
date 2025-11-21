import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.title("🙋 Volunteers Insights")

donations, projects, volunteers = load_data()

# Hours contributed
st.subheader("Volunteer Hours by Person")
fig = px.bar(volunteers, x='volunteer_name', y='hours_contributed')
st.plotly_chart(fig, use_container_width=True)

# Hours per project
st.subheader("Hours Contributed per Project")
fig2 = px.bar(volunteers.groupby('project')['hours_contributed'].sum().reset_index(),
              x='project', y='hours_contributed')
st.plotly_chart(fig2, use_container_width=True)
