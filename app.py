import streamlit as st
import pandas as pd
import plotly.express as px

# Page layout
st.set_page_config(layout="wide", page_title="Consultant Revenue Dashboard")

# Load data
df = pd.read_excel('consultants_revenue.xlsx')

# Sidebar with Logo and Filter Options
st.sidebar.image("lsfrs_logo.jpeg", use_column_width=True)
st.sidebar.title("Filter Options")
st.sidebar.markdown("Use the dropdown to select a consultant or view the overall analysis.")

# Consultant Dropdown with "Overall Analysis" option
consultants = ["Overall Analysis"] + list(df['Consultant Name'].unique())
selected_consultant = st.sidebar.selectbox("Select a Consultant", consultants)

# Title
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; font-family: Arial, sans-serif;'>
    Ilupeju Fire Prevention Unit <br><span style='font-size: 24px;'>Consultant Revenue Dashboard</span>
    </h1>
""", unsafe_allow_html=True)

# KPIs based on selected consultant
if selected_consultant == "Overall Analysis":
    filtered_data = df
else:
    filtered_data = df[df['Consultant Name'] == selected_consultant]

total_companies = filtered_data.shape[0]
total_complied = filtered_data[filtered_data['Status'] == 'Complied'].shape[0]
total_revenue = filtered_data['Amount Charged'].sum()
total_complied_revenue = filtered_data[filtered_data['Status'] == 'Complied']['Amount Charged'].sum()

# Styling for KPIs
st.markdown("""
    <style>
    .kpi-container {
        display: flex;
        justify-content: space-between;
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .kpi-card {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        flex: 1;
        margin: 0 5px;
    }
    .kpi-card h2 {
        font-size: 1.5em;
        color: #4CAF50;
        margin: 0;
    }
    .kpi-card p {
        font-size: 1em;
        color: #7a7a7a;
        margin: 5px 0 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# Compact KPI Layout
st.markdown("### Key Performance Indicators")
st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <p>Total Inspected Companies</p>
            <h2>{total_companies:,}</h2>
        </div>
        <div class="kpi-card">
            <p>Total Amount Charged</p>
            <h2>₦{total_revenue:,}</h2>
        </div>
        <div class="kpi-card">
            <p>Total Complied Facilities</p>
            <h2>{total_complied:,}</h2>
        </div>
        <div class="kpi-card">
            <p>Total Amount from Complied Facilities</p>
            <h2>₦{total_complied_revenue:,}</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

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
