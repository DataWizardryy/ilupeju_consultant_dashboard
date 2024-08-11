# Ilupeju Fire Prevention Unit - Consultant Revenue Dashboard

## Overview

The **Consultant Revenue Dashboard** is a Streamlit-based application designed to visualize and analyze the 
revenue generated by consultants attached to the Ilupeju Fire Prevention Unit of Lagos State Fire and Rescue 
Services. The dashboard provides insights into the revenue generated across various consultants, local government 
areas (LGAs), and types of facilities. Additionally, it offers a compliance status analysis, enabling users to assess 
overall performance and trends effectively.

## Features

- **Consultant Selection:**
  - Filter data to view the overall analysis or focus on a specific consultant, such as GreenFem or Sunny Walls.
- **Interactive Visualizations:**
  - Bar charts for revenue by consultant, LGA, and facility type.
  - Pie charts displaying compliance status.
- **Dynamic Metrics:**
  - Total revenue metrics for the selected consultant or overall revenue.
- **Responsive Layout:**
  - The dashboard is designed with a wide layout, optimized for desktop viewing.
- **Sidebar with Filters:**
  - Users can select consultants and reload data via the sidebar, which also features the Lagos State Fire and Rescue Services logo.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DataWizardryy/ilupeju_consultant_dashboard.git

2. **Navigate to the project directory:**

   ```bash

   cd consultant-revenue-dashboard

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt

4. **Ensure the following files are present:**

   consultants_revenue.xlsx: The dataset containing revenue information.
   lsfrs_logo.jpeg: The logo image used in the sidebar.
   
5. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   This will open the dashboard in your default web browser.
