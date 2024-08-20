import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page layout to wide
st.set_page_config(layout="wide", page_title="Consultant Revenue Dashboard")

# Load data
df = pd.read_excel('consultants_revenue.xlsx')

# Sidebar Styling
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with Logo
st.sidebar.image("lsfrs_logo.jpeg", use_column_width=True)
st.sidebar.title("Filter Options")
st.sidebar.markdown("Use the dropdown to select a consultant or view the overall analysis.")

# Consultant Dropdown with "Overall Analysis" option
consultants = ["Overall Analysis"] + list(df['Consultant Name'].unique())
selected_consultant = st.sidebar.selectbox("Select a Consultant", consultants)

# Customized Title with Styling
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-family: Arial, sans-serif;'>
    Ilupeju Fire Prevention Unit <br><span style='font-size: 24px;'>Consultant Revenue Dashboard</span>
    </h1>
""", unsafe_allow_html=True)

# Define KPIs
total_companies = df.shape[0]
total_complied = df[df['Status'] == 'Complied'].shape[0]
total_revenue = df['Amount Charged'].sum()


# Standardized KPI Layout
st.markdown("### Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.metric("Total Inspected Companies", f"{total_companies:,}")

with kpi_col2:
    st.metric("Total Amount Charged", f"₦{total_revenue:,.2f}")

    
with kpi_col3:
    st.metric("Total Complied Facilities", f"{total_complied:,}")
    




# Overall Analysis or Selected Consultant Analysis

if selected_consultant == "Overall Analysis":
    st.subheader("Overall Charged Analysis")
    
    # Layout for 2 wider plots in each row with spacing
    col1, col2 = st.columns(2)

    with col1:
        # Revenue by Consultant
        st.subheader("Expected Revenue by Consultant")
        revenue_by_consultant = df.groupby('Consultant Name')['Amount Charged'].sum().reset_index()
        fig = px.bar(revenue_by_consultant, x='Consultant Name', y='Amount Charged',
                     text_auto=True, color='Consultant Name', title="Revenue by Consultant",
                     color_discrete_sequence=px.colors.qualitative.G10)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Revenue by LGA
        st.subheader("Expected Revenue by LGA")
        revenue_by_lga = df.groupby('LGA')['Amount Charged'].sum().reset_index()
        fig = px.bar(revenue_by_lga, x='LGA', y='Amount Charged',
                     text_auto=True, color='LGA', title="Revenue by LGA",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    # Revenue by Facility Type
    st.subheader("Expected Revenue by Facility Type")
    revenue_by_facility = df.groupby('Type of Facilities')['Amount Charged'].sum().reset_index()
    fig = px.bar(revenue_by_facility, x='Type of Facilities', y='Amount Charged',
                 text_auto=True, color='Type of Facilities', title="Revenue by Facility Type",
                 color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)

    # Compliance Status Pie Chart
    st.subheader("Overall Compliance Status")
    compliance_status = df.groupby('Status')['Amount Charged'].agg(['count', 'sum']).reset_index()
    fig = px.pie(compliance_status, names='Status', values='count', 
                 hover_data={'sum': True}, 
                 title='Overall Compliance Status',
                 width=800, height=600,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(hovertemplate='%{label}: %{value} cases<br>Sum of Amount: ₦%{customdata[0]:,.2f}')
    st.plotly_chart(fig)

else:
    st.subheader(f"Detailed Revenue Analysis for {selected_consultant}")
    filtered_data = df[df['Consultant Name'] == selected_consultant]

    if selected_consultant in ["GreenFem", "SunnyWalls"]:
        # Total Revenue for Selected Consultant
        total_revenue_consultant = filtered_data['Amount Charged'].sum()
        st.metric("Total Expected Revenue for the Selected Consultant", f"₦{total_revenue_consultant:,.2f}")

    # Layout for 2 wider plots in each row with spacing
    col1, col2 = st.columns(2)

    with col1:
        # Revenue by LGA for Selected Consultant
        st.subheader("Expected Revenue by LGA")
        revenue_by_lga_filtered = filtered_data.groupby('LGA')['Amount Charged'].sum().reset_index()
        fig = px.bar(revenue_by_lga_filtered, x='LGA', y='Amount Charged',
                     text_auto=True, color='LGA', title="Revenue by LGA",
                     color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Revenue by Facility Type for Selected Consultant
        st.subheader("Expected Revenue by Facility Type")
        revenue_by_facility_filtered = filtered_data.groupby('Type of Facilities')['Amount Charged'].sum().reset_index()
        fig = px.bar(revenue_by_facility_filtered, x='Type of Facilities', y='Amount Charged',
                     text_auto=True, color='Type of Facilities', title="Revenue by Facility Type",
                     color_discrete_sequence=px.colors.qualitative.Alphabet)
        st.plotly_chart(fig, use_container_width=True)

    # Compliance Status Pie Chart
    st.subheader("Compliance Status")
    compliance_status_filtered = filtered_data.groupby('Status')['Amount Charged'].agg(['count', 'sum']).reset_index()
    fig = px.pie(compliance_status_filtered, names='Status', values='count', 
                 hover_data={'sum': True}, 
                 title='Compliance Status',
                 width=800, height=600,
                 color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_traces(hovertemplate='%{label}: %{value} cases<br>Sum of Amount: ₦%{customdata[0]:,.2f}')
    st.plotly_chart(fig)

# Reload Button
if st.sidebar.button('Reload Data'):
    df = pd.read_excel('consultants_revenue.xlsx')
    st.success("Data reloaded!")
