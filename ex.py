import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np

UN_data = pd.read_csv("university_student_dashboard_data.csv")

st.title("University Admissions & Student Satisfaction EDA")

st.header("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", UN_data["Applications"].sum())
col2.metric("Total Admissions", UN_data["Admitted"].sum())
col3.metric("Total Enrollments", UN_data["Enrolled"].sum())

col4, col5 = st.columns(2)
col4.metric("Average Retention Rate (%)", round(UN_data["Retention Rate (%)"].mean(), 2))
col5.metric("Average Student Satisfaction (%)", round(UN_data["Student Satisfaction (%)"].mean(), 2))

# Display dataset overview
st.subheader("Dataset Overview")
st.write(UN_data.head())

st.subheader("Summary Statistics")
st.write(UN_data.describe())
st.write("Given data show a reprentation of university key insights, with this, one could conclude that there is a good retention rate of students and good satisfaction overall.")

st.subheader("Admission and enrollment percentages")

df_sorted = UN_data.sort_values(by="Year")
# Calculate Admission and enrollment percentages
df_sorted["Admission Rate (%)"] = (df_sorted["Admitted"] / df_sorted["Applications"]) * 100
df_sorted["Enrollment Rate (%)"] = (df_sorted["Enrolled"] / df_sorted["Admitted"]) * 100
df_sorted["Overall Enrollment Rate (%)"] = (df_sorted["Enrolled"] / df_sorted["Applications"]) * 100

st.write(df_sorted[["Year", "Applications", "Admitted", "Admission Rate (%)", "Enrolled", "Enrollment Rate (%)", "Overall Enrollment Rate (%)"]])

st.write("In all years, for all the applicants, there is an approximately 23% of people that enroll, approx 40% of admitted people enroll")

# Admissions Trends
st.subheader("Admissions Trends Over Time")
fig_admissions = px.line(UN_data, x="Year", y=["Applications", "Admitted", "Enrolled"], markers=True, 
                         title="Admissions Trends Over Time", color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96"])
st.plotly_chart(fig_admissions)

# Retention and Satisfaction Trends
st.subheader("Retention & Satisfaction by Department")
retention_satisfaction_df = UN_data.melt(id_vars=["Year"], value_vars=["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"], 
                                     var_name="Department", value_name="Enrolled")
retention_satisfaction_df["Retention Rate (%)"] = UN_data["Retention Rate (%)"]
retention_satisfaction_df["Student Satisfaction (%)"] = UN_data["Student Satisfaction (%)"]

fig_retention_dept = px.line(retention_satisfaction_df, x="Year", y="Retention Rate (%)", color="Department", markers=True,
                             title="Retention Rate by Department")
st.plotly_chart(fig_retention_dept, use_container_width=True)

fig_satisfaction_dept = px.line(retention_satisfaction_df, x="Year", y="Student Satisfaction (%)", color="Department", markers=True,
                                title="Student Satisfaction by Department")
st.plotly_chart(fig_satisfaction_dept, use_container_width=True)

# Enrollment by Department
st.subheader("Enrollment Breakdown by Department")
fig_department = px.bar(UN_data, x="Year", y=["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"], 
                        barmode="group", title="Enrollment Breakdown by Department", color_discrete_sequence=["#636EFA", "#EF553B", "#00CC96", "#FFA15A"])
st.plotly_chart(fig_department)

# Compare Spring vs Fall Trends
st.subheader("Spring vs Fall Enrollment Distribution")
fig_term = px.box(UN_data, x="Term", y="Enrolled", color="Term", title="Enrollment Distribution: Spring vs Fall", 
                  color_discrete_sequence=["#19D3F3", "#FF6692"])
st.plotly_chart(fig_term)

# Improved Correlation Heatmap
st.subheader("Feature Correlation Heatmap")
numeric_df = UN_data.select_dtypes(include=[np.number])  # Select only numeric columns
correlation_matrix = numeric_df.corr()

fig_corr = go.Figure(data=go.Heatmap(z=correlation_matrix.values,
                                     x=correlation_matrix.columns,
                                     y=correlation_matrix.index,
                                     colorscale="plasma",
                                     zmin=-1, zmax=1,
                                     text=correlation_matrix.values.round(2),
                                     texttemplate="%{text}",
                                     hoverinfo="text"))
fig_corr.update_layout(title="Feature Correlation Heatmap", 
                       xaxis_title="Features", 
                       yaxis_title="Features",
                       width=800, height=700)
st.plotly_chart(fig_corr)

st.header("Key Takeaways & Insights")
st.markdown("📈 **Admissions are Growing!** More students are applying every year, showing a strong reputation. To keep up, enhancing application processing and outreach could be beneficial.")
st.markdown("📊 **Retention is Steady** (85-87%). While this is great, there's always room to keep students engaged and supported through mentorship and academic assistance.")
st.markdown("😊 **Student Satisfaction is Improving!** A positive trend, but some departments may need extra attention to ensure all students have a great experience.")
st.markdown("🏫 **Engineering Leads in Enrollment.** Other fields like Arts and Science could benefit from additional promotions, scholarships, or interdisciplinary programs.")
st.markdown("🍂 **Fall vs Spring Admissions are Close.** Fall sees slightly higher enrollments, so optimizing resources accordingly can ensure a smooth student experience year-round.")

