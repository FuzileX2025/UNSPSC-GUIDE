import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Sample Data
purchase_orders = [
    ["PO-1001", "2023-01-05", "Tech Corp", "Laptop Computers", 43211505, 45000],
    ["PO-1002", "2023-01-12", "OfficeWorld", "Office Furniture", 56101500, 12000],
    ["PO-1003", "2023-02-03", "MediSupply", "Medical Equipment", 42161500, 85000],
    ["PO-1004", "2023-02-15", "BuildIt", "Construction Materials", 30101608, 150000],
    ["PO-1005", "2023-03-01", "Tech Corp", "Network Servers", 43211603, 92000],
    ["PO-1006", "2023-03-15", "OfficeWorld", "Stationery Supplies", 44101802, 4500],
]

# Create DataFrame
df = pd.DataFrame(purchase_orders, 
                 columns=["PO Number", "Date", "Supplier", "Description", "UNSPSC Code", "Amount"])

# Streamlit App
st.title("UNSPSC Code Demonstration Tool")

# Tab 1: UNSPSC Explanation
tab1, tab2 = st.tabs(["About UNSPSC", "Spend Analysis Dashboard"])

with tab1:
    st.header("UNSPSC Codes Overview")
    st.subheader("What are UNSPSC Codes?")
    st.markdown("""
    - **Universal Standard for Products and Services Classification**
    - 8-digit hierarchical coding system
    - Four-level structure: Segment, Family, Class, Commodity
    - Example: 43 - IT Equipment (Segment)
        - 4321 - Computers (Family)
        - 432115 - Laptops (Class)
        - 43211505 - Business Laptops (Commodity)
    """)
    
    st.subheader("Purpose and Importance")
    st.markdown("""
    - **Standardized procurement classification**
    - Enables spend analysis and reporting
    - Facilitates supplier management
    - Supports strategic sourcing initiatives
    - Essential for:
        - Spend visibility
        - Category management
        - Contract compliance
        - Supplier rationalization
    """)

# Tab 2: Dashboard
with tab2:
    st.header("Procurement Spend Analysis")
    
    # Data Processing
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    df['UNSPSC Category'] = df['UNSPSC Code'].astype(str).str[:2]
    
    # Create two columns
    col1, col2 = st.columns([1,2])
    
    with col1:
        st.subheader("Raw Purchase Orders")
        st.dataframe(df[["PO Number", "Date", "Supplier", "Description", "UNSPSC Code", "Amount"]])
    
    with col2:
        st.subheader("Spend Analysis")
        
        # Time Series Chart
        time_series = df.groupby('Month')['Amount'].sum().reset_index()
        fig1 = px.line(time_series, x='Month', y='Amount', 
                       title="Monthly Spend Trend",
                       markers=True)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Category Breakdown
        category_spend = df.groupby('UNSPSC Category')['Amount'].sum().reset_index()
        fig2 = px.bar(category_spend, x='UNSPSC Category', y='Amount',
                      title="Spend by UNSPSC Category",
                      color='UNSPSC Category')
        st.plotly_chart(fig2, use_container_width=True)
        
    # Benefits Demonstration
    st.subheader("Key Insights & Benefits")
    st.markdown("""
    - **Clear spend visibility** across categories
    - Identification of **high-spend areas** (e.g., Construction Materials)
    - Better **supplier negotiation** through category analysis
    - **Trend spotting** for budget planning
    - **Compliance monitoring** against preferred suppliers
    """)

st.sidebar.markdown("### UNSPSC Code Legend")
st.sidebar.markdown("""
- **43**: IT Equipment
- **56**: Office Equipment
- **42**: Medical Equipment
- **30**: Structural Products
- **44**: Office Supplies
""")
