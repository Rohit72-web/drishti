import numpy as np
from sklearn.linear_model import QuantileRegressor

BENCHMARKS = {
    "small":          {"daily_min": 2000,  "daily_max": 5000},
    "medium":         {"daily_min": 5000,  "daily_max": 15000},
    "large":          {"daily_min": 15000, "daily_max": 40000},
    "semi_wholesale": {"daily_min": 40000, "daily_max": 100000}
}

def get_store_tier(drishti_score):
    if drishti_score < 0.35:
        return "small"
    elif drishti_score < 0.60:
        return "medium"
    elif drishti_score < 0.80:
        return "large"
    else:
        return "semi_wholesale"

def estimate_cash_flow(drishti_score, visual_score, geo_score):
    tier = get_store_tier(drishti_score)
    bench = BENCHMARKS[tier]
    daily_min = bench["daily_min"] * (0.85 + drishti_score * 0.30)
    daily_max = bench["daily_max"] * (0.85 + drishti_score * 0.30)
    daily_min = max(bench["daily_min"], min(daily_min, bench["daily_max"]))
    daily_max = max(daily_min, min(daily_max, bench["daily_max"] * 1.15))
    monthly_min = daily_min * 26
    monthly_max = daily_max * 26
    income_min = monthly_min * 0.08
    income_max = monthly_max * 0.15
    confidence = round(
        (drishti_score * 0.6 +
         min(visual_score, geo_score) * 0.4), 2
    )
    return {
        "daily_sales_range": [int(daily_min), int(daily_max)],
        "monthly_revenue_range": [int(monthly_min), int(monthly_max)],
        "monthly_income_range": [int(income_min), int(income_max)],
        "confidence_score": confidence,
        "store_tier": tier
    }