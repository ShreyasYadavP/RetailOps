import scipy.stats as stats

def run_diagnostics(df, value_col='Sales_Revenue'):
    """
    Performs normality (Shapiro-Wilk) and variance homogeneity (Levene's) checks.
    """
    target_data = df[value_col].dropna()
    if len(target_data) < 3:
        return {
            "Shapiro_Statistic": 0.0, "Shapiro_P_Value": 1.0,
            "Levene_Statistic": 0.0, "Levene_P_Value": 1.0
        }

    sample_data = target_data.sample(min(len(target_data), 300), random_state=42)
    shapiro_stat, shapiro_p = stats.shapiro(sample_data)
    
    groups = [group[value_col].dropna().values for _, group in df.groupby('Region') if len(group[value_col].dropna()) > 1]
    if len(groups) > 1:
        levene_stat, levene_p = stats.levene(*groups)
    else:
        levene_stat, levene_p = 0.0, 1.0
    
    return {
        "Shapiro_Statistic": round(shapiro_stat, 4),
        "Shapiro_P_Value": round(shapiro_p, 4),
        "Levene_Statistic": round(levene_stat, 4),
        "Levene_P_Value": round(levene_p, 4)
    }
