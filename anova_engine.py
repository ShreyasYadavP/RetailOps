import numpy as np
import pandas as pd
from scipy import stats


def run_anova(df, group_col="Region", value_col="Sales_Revenue"):
  try:
    groups = [
        group[value_col].dropna().values for _, group in df.groupby(group_col)
    ]
    if len(groups) < 2:
      return None

    # Overall & group stats
    all_data = np.concatenate(groups)
    grand_mean = np.mean(all_data)
    N = len(all_data)
    k = len(groups)

    # Sum of Squares
    ss_between = sum(
        len(group) * ((np.mean(group) - grand_mean) ** 2) for group in groups
    )
    ss_within = sum(
        sum((x - np.mean(group)) ** 2 for x in group) for group in groups
    )
    ss_total = ss_between + ss_within

    # Degrees of Freedom & Mean Squares
    df_between = k - 1
    df_within = N - k
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within

    # F-Statistic & P-Value
    f_stat, p_val = stats.f_oneway(*groups)

    # 1. Standard ANOVA Summary Table
    anova_table = pd.DataFrame({
        "Source of Variation": ["Between Groups", "Within Groups", "Total"],
        "Sum of Squares (SS)": [
            round(ss_between, 2),
            round(ss_within, 2),
            round(ss_total, 2),
        ],
        "df": [df_between, df_within, N - 1],
        "Mean Square (MS)": [
            round(ms_between, 2),
            round(ms_within, 2),
            np.nan,
        ],
        "F-Statistic": [round(f_stat, 4), np.nan, np.nan],
        "p-value": [round(p_val, 4), np.nan, np.nan],
    })

    # 2. Group-Level Descriptive Statistics Table
    group_summary = (
        df.groupby(group_col)[value_col]
        .agg(
            Count="count",
            Mean="mean",
            Std_Dev="std",
            Std_Error=lambda x: stats.sem(x.dropna()),
        )
        .reset_index()
    )
    group_summary[["Mean", "Std_Dev", "Std_Error"]] = group_summary[
        ["Mean", "Std_Dev", "Std_Error"]
    ].round(2)

    return {
        "F-Statistic": round(f_stat, 4),
        "P-Value": round(p_val, 4),
        "Significant": bool(p_val < 0.05),
        "ANOVA_Table": anova_table,
        "Group_Summary": group_summary,
    }
  except Exception as e:
    return None


run_one_way_anova = run_anova
