import scipy.stats as stats
import pandas as pd

def run_anova(df, group_col='Region', value_col='Sales_Revenue'):
    """
    Runs a One-Way ANOVA test across categories or regions.
    """
    # Filter out groups with fewer than 2 elements to prevent scipy errors
    groups = [group[value_col].dropna().values for _, group in df.groupby(group_col) if len(group[value_col].dropna()) > 1]
    
    if len(groups) < 2:
        return {"F-Statistic": 0.0, "P-Value": 1.0, "Significant": False}

    f_val, p_val = stats.f_oneway(*groups)
    
    results = {
        "F-Statistic": round(f_val, 4),
        "P-Value": round(p_val, 4),
        "Significant": p_val < 0.05
    }
    return results
