
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Energy Era Upskilling Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("clean_training_data.csv")

df = load_data()

st.title("⚡ Energy Era Employee Upskilling Dashboard")
st.markdown("Training analytics dashboard for external employee training programs.")

# Sidebar filters
agency_filter = st.sidebar.multiselect(
    "Select Training Agency",
    options=sorted(df["Training_Agency"].dropna().unique()),
    default=sorted(df["Training_Agency"].dropna().unique())
)

mode_filter = st.sidebar.multiselect(
    "Select Training Mode",
    options=sorted(df["Mode_of_Training"].dropna().unique()),
    default=sorted(df["Mode_of_Training"].dropna().unique())
)

filtered_df = df[
    (df["Training_Agency"].isin(agency_filter)) &
    (df["Mode_of_Training"].isin(mode_filter))
]

# KPIs
total_programs = filtered_df["Training_Program"].count()
total_participants = filtered_df["Total"].sum()
avg_days = filtered_df["No_of_Days"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Programs", int(total_programs))
col2.metric("Total Participants", int(total_participants))
col3.metric("Average Training Days", round(avg_days, 2))

st.divider()

# Participation by company
company_cols = ["GUVNL","GETCO","GSECL","PGVCL","DGVCL","UGVCL","MGVCL"]

company_totals = filtered_df[company_cols].sum().reset_index()
company_totals.columns = ["Company","Participants"]

fig1 = px.bar(
    company_totals,
    x="Company",
    y="Participants",
    title="Company-wise Participation"
)

st.plotly_chart(fig1, use_container_width=True)

# Training mode distribution
mode_counts = filtered_df["Mode_of_Training"].value_counts().reset_index()
mode_counts.columns = ["Mode","Count"]

fig2 = px.pie(
    mode_counts,
    names="Mode",
    values="Count",
    title="Training Mode Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# Top agencies
agency_counts = (
    filtered_df["Training_Agency"]
    .value_counts()
    .head(10)
    .reset_index()
)

agency_counts.columns = ["Agency","Programs"]

fig3 = px.bar(
    agency_counts,
    x="Programs",
    y="Agency",
    orientation="h",
    title="Top Training Agencies"
)

st.plotly_chart(fig3, use_container_width=True)

# Training locations
location_counts = (
    filtered_df["Place_of_Training"]
    .value_counts()
    .head(10)
    .reset_index()
)

location_counts.columns = ["Location","Programs"]

fig4 = px.bar(
    location_counts,
    x="Location",
    y="Programs",
    title="Top Training Locations"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Training Program Details")
st.dataframe(filtered_df)
