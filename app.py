import streamlit as st
import pandas as pd
from generate_data import generate_retail_data
from anova_engine import run_anova
from diagnostics_testing import run_diagnostics

from visualizations import plot_sales_by_region, plot_footfall_vs_sales, plot_total_sales_by_region, plot_sales_by_region, plot_footfall_vs_sales, plot_category_bar, plot_marketing_efficiency

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
        st.plotly_chart(plot_total_sales_by_region(filtered_df), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_marketing_efficiency(filtered_df), use_container_width=True)
        with col2:
            st.plotly_chart(plot_category_bar(filtered_df), use_container_width=True)

    except Exception as e:
        st.error(f"Could not render visualizations. Error: {e}")

with tab3:
  st.subheader("One-Way ANOVA Statistical Results")
  try:
    anova_res = run_anova(filtered_df)
    if anova_res:
      col1, col2, col3 = st.columns(3)
      col1.metric("F-Statistic", f"{anova_res['F-Statistic']:.4f}")
      col2.metric("P-Value", f"{anova_res['P-Value']:.4f}")
      col3.metric(
          "Significant Difference?", str(anova_res["Significant"])
      )

      st.markdown("---")
      st.markdown("### **ANOVA Table (Sum of Squares Breakdown)**")
      st.dataframe(anova_res["ANOVA_Table"], use_container_width=True)

      st.markdown("### **Group-Level Descriptive Statistics**")
      st.dataframe(anova_res["Group_Summary"], use_container_width=True)
    else:
      st.error("Could not compute ANOVA. Please verify column selections.")
  except Exception as e:
    st.error(f"ANOVA calculation failed: {e}")

with tab4:
  st.subheader("Statistical Assumptions Diagnostics")
  st.markdown(
      "Verifying parametric prerequisites for ANOVA: **Normality** (Shapiro-Wilk"
      " test) and **Homoscedasticity** (Levene's test)."
  )
  try:
    diag_res = run_diagnostics(filtered_df)
    if "Error" not in diag_res:
      # Display summary table
      st.markdown("### **Diagnostics Summary Table**")
      st.dataframe(diag_res["Diagnostics_Table"], use_container_width=True)

      st.markdown("---")
      st.markdown("### **Raw Diagnostic Output (JSON)**")
      st.json(diag_res)
    else:
      st.error(f"Diagnostics routine failed: {diag_res['Error']}")
  except Exception as e:
    st.error(f"Diagnostics routine failed: {e}")
