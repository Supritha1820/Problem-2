import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache
def load_data():
    return pd.read_csv("university_student_dashboard_data.csv")

data = load_data()

# Dashboard title
st.title("University Admissions, Retention & Satisfaction Dashboard")

# Sidebar filters
term_filter = st.sidebar.selectbox("Select Term", options=data['Term'].unique())
department_filter = st.sidebar.multiselect("Select Departments", options=data['Department'].unique(), default=data['Department'].unique())

# Filtered data
data_filtered = data[(data['Term'] == term_filter) & (data['Department'].isin(department_filter))]

# KPIs
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", data_filtered['Applications'].sum())
col2.metric("Total Admissions", data_filtered['Admissions'].sum())
col3.metric("Total Enrollments", data_filtered['Enrollments'].sum())

# Retention trends
df_retention = data.groupby(['Year'])['Retention Rate'].mean().reset_index()
st.subheader("Retention Rate Over Time")
fig_retention = px.line(df_retention, x='Year', y='Retention Rate', markers=True)
st.plotly_chart(fig_retention)

# Satisfaction Trends
df_satisfaction = data.groupby(['Year'])['Satisfaction Score'].mean().reset_index()
st.subheader("Student Satisfaction Trends")
fig_satisfaction = px.line(df_satisfaction, x='Year', y='Satisfaction Score', markers=True)
st.plotly_chart(fig_satisfaction)

# Enrollment by Department
st.subheader("Enrollment Breakdown by Department")
df_dept = data_filtered.groupby('Department')['Enrollments'].sum().reset_index()
fig_dept = px.bar(df_dept, x='Department', y='Enrollments', color='Department')
st.plotly_chart(fig_dept)

# Spring vs Fall Trends
st.subheader("Spring vs. Fall Term Trends")
df_term = data.groupby('Term')[['Applications', 'Admissions', 'Enrollments']].sum().reset_index()
fig_term = px.bar(df_term, x='Term', y=['Applications', 'Admissions', 'Enrollments'], barmode='group')
st.plotly_chart(fig_term)

# Department-wise Comparison
st.subheader("Department-wise Retention & Satisfaction")
df_dept_compare = data.groupby('Department')[['Retention Rate', 'Satisfaction Score']].mean().reset_index()
fig_compare = px.bar(df_dept_compare, x='Department', y=['Retention Rate', 'Satisfaction Score'], barmode='group')
st.plotly_chart(fig_compare)

st.write("### Key Findings & Insights:")
st.write("- Retention rates show a positive/negative trend over the years.")
st.write("- Student satisfaction levels have been increasing/decreasing.")
st.write("- Engineering/Business/etc. has the highest enrollment rates.")
st.write("- Fall/Spring term trends show XYZ pattern.")
