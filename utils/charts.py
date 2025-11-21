import streamlit as st
import plotly.express as px

def donations_over_time_chart(donations):
    df = donations.groupby('date')['donation_amount'].sum().reset_index()
    fig = px.line(df, x='date', y='donation_amount', title="Donations Over Time")
    st.plotly_chart(fig, use_container_width=True)

def top_donors_chart(donations, top_n=10):
    df = donations.groupby('donor_name')['donation_amount'].sum().sort_values(ascending=False).head(top_n).reset_index()
    fig = px.bar(df, x='donor_name', y='donation_amount', title=f"Top {top_n} Donors")
    st.plotly_chart(fig, use_container_width=True)
