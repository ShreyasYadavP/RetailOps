import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def plot_sales_by_region(df):
  """Enhanced Box plot showing sales distribution across regions and categories."""
  fig = px.box(
      df,
      x="Region",
      y="Sales_Revenue",
      color="Category",
      points="all",
      hover_data=["Store_ID", "Customer_Footfall", "Marketing_Spend"],
      color_discrete_sequence=px.colors.qualitative.Bold,
      template="plotly_dark",
  )
  fig.update_layout(
      title="<b>Sales Revenue Distribution by Region & Category</b>",
      xaxis_title="<b>Store Region</b>",
      yaxis_title="<b>Sales Revenue ($)</b>",
      legend_title="<b>Product Category</b>",
      height=500,
      margin=dict(l=20, r=20, t=50, b=20),
  )
  return fig


def plot_footfall_vs_sales(df):
  """Enhanced OLS Regression scatter plot between Customer Footfall and Sales Revenue."""
  fig = px.scatter(
      df,
      x="Customer_Footfall",
      y="Sales_Revenue",
      color="Region",
      trendline="ols",
      hover_data=["Category", "Marketing_Spend"],
      color_discrete_sequence=px.colors.qualitative.Vivid,
      template="plotly_dark",
  )
  fig.update_layout(
      title="<b>Customer Footfall vs. Sales Revenue (with OLS Trendlines)</b>",
      xaxis_title="<b>Customer Footfall (Visitor Count)</b>",
      yaxis_title="<b>Sales Revenue ($)</b>",
      legend_title="<b>Region</b>",
      height=500,
      margin=dict(l=20, r=20, t=50, b=20),
  )
  return fig


def plot_marketing_efficiency(df):
  """New Chart: Marketing Spend vs Sales Revenue colored by ROI."""
  df_copy = df.copy()
  df_copy["Marketing_ROI"] = (
      df_copy["Sales_Revenue"] / df_copy["Marketing_Spend"]
  ).round(2)

  fig = px.scatter(
      df_copy,
      x="Marketing_Spend",
      y="Sales_Revenue",
      color="Marketing_ROI",
      size="Customer_Footfall",
      hover_data=["Store_ID", "Region", "Category"],
      color_continuous_scale="Viridis",
      template="plotly_dark",
  )
  fig.update_layout(
      title="<b>Marketing Spend Efficiency & ROI Analysis</b>",
      xaxis_title="<b>Marketing Spend ($)</b>",
      yaxis_title="<b>Sales Revenue ($)</b>",
      coloraxis_colorbar_title="<b>ROI Multiplier</b>",
      height=450,
      margin=dict(l=20, r=20, t=50, b=20),
  )
  return fig


def plot_category_bar(df):
  """New Chart: Average Sales Revenue by Product Category."""
  cat_avg = (
      df.groupby("Category")["Sales_Revenue"]
      .mean()
      .reset_index()
      .sort_values(by="Sales_Revenue", ascending=True)
  )

  fig = px.bar(
      cat_avg,
      x="Sales_Revenue",
      y="Category",
      orientation="h",
      text_auto=".2f",
      color="Category",
      color_discrete_sequence=px.colors.qualitative.Pastel,
      template="plotly_dark",
  )
  fig.update_layout(
      title="<b>Average Sales Revenue by Product Category</b>",
      xaxis_title="<b>Mean Sales Revenue ($)</b>",
      yaxis_title="<b>Category</b>",
      showlegend=False,
      height=450,
      margin=dict(l=20, r=20, t=50, b=20),
  )
  return fig
