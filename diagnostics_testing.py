import pandas as pd
from scipy import stats


def run_diagnostics(df, group_col="Region", value_col="Sales_Revenue"):
  try:
    # 1. Shapiro-Wilk Normality Test
    shapiro_stat, shapiro_p = stats.shapiro(df[value_col].dropna())
    normality_passed = bool(shapiro_p > 0.05)

    # 2. Levene's Test for Homoscedasticity (Equal Variances)
    groups = [
        group[value_col].dropna().values for _, group in df.groupby(group_col)
    ]
    levene_stat, levene_p = stats.levene(*groups)
    variance_passed = bool(levene_p > 0.05)

    # Summary table for professional display
    diag_table = pd.DataFrame({
        "Assumption Tested": [
            "Normality (Shapiro-Wilk)",
            "Homoscedasticity (Levene's)",
        ],
        "Statistical Test": ["Shapiro-Wilk W", "Levene Test W"],
        "Statistic Value": [round(shapiro_stat, 4), round(levene_stat, 4)],
        "p-value": [round(shapiro_p, 4), round(levene_p, 4)],
        "Threshold (α)": [0.05, 0.05],
        "Assumption Met?": [
            "Yes (Retain H₀)" if normality_passed else "No",
            "Yes (Retain H₀)" if variance_passed else "No",
        ],
    })

    results_dict = {
        "Shapiro_Statistic": round(shapiro_stat, 4),
        "Shapiro_P_Value": round(shapiro_p, 4),
        "Normality_Passed": normality_passed,
        "Levene_Statistic": round(levene_stat, 4),
        "Levene_P_Value": round(levene_p, 4),
        "Equal_Variance_Passed": variance_passed,
        "Diagnostics_Table": diag_table,
    }

    return results_dict
  except Exception as e:
    return {"Error": str(e)}
