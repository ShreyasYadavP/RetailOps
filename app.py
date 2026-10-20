import streamlit as st
import pandas as pd
from generate_data import generate_retail_data
from anova_engine import run_anova
from diagnostics_testing import run_diagnostics
from visualizations import plot_sales_by_region, plot_footfall_vs_sales

st.set_page_config(page_title="RetailOps Analytics", layout="wide")

st.title("🛒 RetailOps: Retail Data Analytics & Diagnostics Engine")
st.markdown("Collaborative retail store performance and statistical evaluation dashboard.")

# --- 1. DATA SOURCE CONFIGURATION ---
st.sidebar.header("Data Source Configuration")
data_source = st.sidebar.radio("Choose Data Source", ["Default Synthetic Data", "Upload Custom File"])

df = None

if data_source == "Upload Custom File":
    uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.sidebar.success("File uploaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            df = generate_retail_data()
    else:
        st.sidebar.info("Awaiting file upload. Using default synthetic data for now.")
        df = generate_retail_data()
else:
    df = generate_retail_data()

# --- 2. COLUMN MAPPING FOR CUSTOM DATA ---
processed_df = df.copy()

if data_source == "Upload Custom File" and uploaded_file is not None:
    st.sidebar.subheader("Map Your Columns")
    available_cols = list(df.columns)
    
    # Attempt intelligent default guesses if column names look similar
    def get_default_index(options, keywords):
        for kw in keywords:
            for idx, col in enumerate(options):
                if kw in col.lower():
                    return idx
        return 0

    map_store = st.sidebar.selectbox("Store ID Column", available_cols, index=get_default_index(available_cols, ['store', 'id']))
    map_region = st.sidebar.selectbox("Region Column", available_cols, index=get_default_index(available_cols, ['region', 'location', 'zone']))
    map_category = st.sidebar.selectbox("Category Column", available_cols, index=get_default_index(available_cols, ['category', 'product', 'type']))
    map_sales = st.sidebar.selectbox("Sales Revenue Column", available_cols, index=get_default_index(available_cols, ['sales', 'revenue', 'price', 'amount']))
    map_footfall = st.sidebar.selectbox("Customer Footfall Column", available_cols, index=get_default_index(available_cols, ['footfall', 'customer', 'visitors', 'count']))
    map_marketing = st.sidebar.selectbox("Marketing Spend Column", available_cols, index=get_default_index(available_cols, ['marketing', 'spend', 'ads', 'cost']))

    # Standardize dataframe columns for backend modules
    processed_df = pd.DataFrame({
        'Store_ID': df[map_store],
        'Region': df[map_region],
        'Category': df[map_category],
        'Sales_Revenue': pd.to_numeric(df[map_sales], errors='coerce'),
        'Customer_Footfall': pd.to_numeric(df[map_footfall], errors='coerce'),
        'Marketing_Spend': pd.to_numeric(df[map_marketing], errors='coerce')
    }).dropna()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Filters")
if 'Region' in processed_df.columns:
    selected_region = st.sidebar.selectbox("Filter by Region", ["All"] + list(processed_df['Region'].unique()))
    if selected_region != "All":
        filtered_df = processed_df[processed_df['Region'] == selected_region]
    else:
        filtered_df = processed_df
else:
    filtered_df = processed_df

# --- 4. MAIN APPLICATION TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📁 Data Preview", "📊 Visualizations", "🔬 ANOVA Engine", "📋 Diagnostics"])

with tab1:
    st.subheader("Dataset Preview & Summary")
    st.dataframe(filtered_df, use_container_width=True)
    st.write(f"**Total Rows:** {len(filtered_df)} | **Total Columns:** {len(filtered_df.columns)}")

with tab2:
    st.subheader("Interactive Visual Analytics")
    try:
        st.plotly_chart(plot_sales_by_region(filtered_df), use_container_width=True)
        st.plotly_chart(plot_footfall_vs_sales(filtered_df), use_container_width=True)
    except Exception as e:
        st.error(f"Could not render visualizations. Please verify your mapped columns. Error: {e}")

with tab3:
    st.subheader("One-Way ANOVA Statistical Results")
    try:
        anova_res = run_anova(filtered_df)
        col1, col2, col3 = st.columns(3)
        col1.metric("F-Statistic", anova_res["F-Statistic"])
        col2.metric("P-Value", anova_res["P-Value"])
        col3.metric("Significant Difference?", str(anova_res["Significant"]))
    except Exception as e:
        st.error(f"ANOVA calculation failed. Ensure numeric 'Sales_Revenue' and categorical 'Region' are properly mapped. Error: {e}")

with tab4:
    st.subheader("Statistical Assumptions Diagnostics")
    try:
        diag_res = run_diagnostics(filtered_df)
        st.write("Diagnostic Testing Results:", diag_res)
    except Exception as e:
        st.error(f"Diagnostics routine failed: {e}")
