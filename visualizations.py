import plotly.express as px

def plot_sales_by_region(df):
    fig = px.box(df, x='Region', y='Sales_Revenue', color='Category', 
                 title="Sales Revenue Distribution by Region and Category")
    return fig

def plot_footfall_vs_sales(df):
    fig = px.scatter(df, x='Customer_Footfall', y='Sales_Revenue', color='Region',
                     trendline="ols", title="Customer Footfall vs Sales Revenue")
    return fig
