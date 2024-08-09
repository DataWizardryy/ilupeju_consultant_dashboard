import streamlit as st
import pandas as pd
import plotly.express as px

# Set page layout to wide
st.set_page_config(layout="wide")

# Load data
df = pd.read_excel('consultants_revenue.xlsx')

# Sidebar
st.sidebar.title("Filter Options")

# Consultant Dropdown with "Overall Analysis" option
consultants = ["Overall Analysis"] + list(df['Consultant Name'].unique())
selected_consultant = st.sidebar.selectbox("Select a Consultant", consultants)

# Customized Title with Styling
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-family: Arial, sans-serif;'>
    Ilupeju Fire Prevention Unit <br><span style='font-size: 24px;'>Consultant Revenue Dashboard</span>
    </h1>
""", unsafe_allow_html=True)

if selected_consultant == "Overall Analysis":
    # Overall Total Revenue
    total_revenue = df['Amount Charged'].sum()
    st.metric("Total Amount Charged", f"₦{total_revenue:,.2f}")

    # General Revenue Analysis
    st.subheader("Overall Charged Analysis")
    
    # Layout for 2 wider plots in each row with spacing
    col1, col2 = st.columns([5, 5])  # Adjust the width ratio to make columns wider

    with col1:
        # Revenue by Consultant
        st.subheader("Expected Revenue by Consultant")
        revenue_by_consultant = df.groupby('Consultant Name')['Amount Charged'].sum().reset_index()
        st.bar_chart(revenue_by_consultant.set_index('Consultant Name'))

    with col2:
        # Revenue by LGA
        st.subheader("Expected Revenue by LGA")
        revenue_by_lga = df.groupby('LGA')['Amount Charged'].sum().reset_index()
        st.bar_chart(revenue_by_lga.set_index('LGA'))

    # Next Row for Revenue by Facility Type
    st.subheader("Expected Revenue by Facility Type")
    revenue_by_facility = df.groupby('Type of Facilities')['Amount Charged'].sum().reset_index()
    st.bar_chart(revenue_by_facility.set_index('Type of Facilities'))

    # Next Row for Pie Chart
    st.subheader("Overall Compliance Status")
    compliance_status = df.groupby('Status')['Amount Charged'].agg(['count', 'sum']).reset_index()
    fig = px.pie(compliance_status, names='Status', values='count', 
                 hover_data={'sum': True}, 
                 title='Overall Compliance Status',
                 width=800, height=600)  # Increase width and height for wider pie chart
    fig.update_traces(hovertemplate='%{label}: %{value} cases<br>Sum of Amount: ₦%{customdata[0]:,.2f}')
    st.plotly_chart(fig)

else:
    # Revenue Analysis for Selected Consultant
    st.subheader(f"Detailed Revenue Analysis for {selected_consultant}")
    filtered_data = df[df['Consultant Name'] == selected_consultant]

    if selected_consultant in ["GreenFem", "SunnyWalls"]:
        # Total Revenue for Selected Consultant
        total_revenue_consultant = filtered_data['Amount Charged'].sum()
        st.metric("Total Expected Revenue for the Selected Consultant", f"₦{total_revenue_consultant:,.2f}")

    # Layout for 2 wider plots in each row with spacing
    col1, col2 = st.columns([5, 5])  # Adjust the width ratio to make columns wider

    with col1:
        # Revenue by LGA for Selected Consultant
        st.subheader("Expected Revenue by LGA")
        revenue_by_lga_filtered = filtered_data.groupby('LGA')['Amount Charged'].sum().reset_index()
        st.bar_chart(revenue_by_lga_filtered.set_index('LGA'))

    with col2:
        # Revenue by Facility Type for Selected Consultant
        st.subheader("Expected Revenue by Facility Type")
        revenue_by_facility_filtered = filtered_data.groupby('Type of Facilities')['Amount Charged'].sum().reset_index()
        st.bar_chart(revenue_by_facility_filtered.set_index('Type of Facilities'))

    # Compliance Status Pie Chart with hover information
    st.subheader("Compliance Status")
    compliance_status_filtered = filtered_data.groupby('Status')['Amount Charged'].agg(['count', 'sum']).reset_index()
    fig = px.pie(compliance_status_filtered, names='Status', values='count', 
                 hover_data={'sum': True}, 
                 title='Compliance Status',
                 width=800, height=600)  # Increase width and height for wider pie chart
    fig.update_traces(hovertemplate='%{label}: %{value} cases<br>Sum of Amount: ₦%{customdata[0]:,.2f}')
    st.plotly_chart(fig)

# Reload Button
if st.sidebar.button('Reload Data'):
    df = pd.read_excel('consultants_revenue.xlsx')
    st.success("Data reloaded!")
