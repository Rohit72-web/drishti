from modules.image_engine import run_image_engine
from modules.geo_engine import run_geo_engine
from modules.feature_engine import (compute_visual_score,
                                     compute_geo_score,
                                     compute_optional_score,
                                     compute_drishti_score)
from modules.fusion_model import estimate_cash_flow
from modules.fraud_engine import run_fraud_engine
from config import GOOGLE_VISION_API_KEY, GOOGLE_MAPS_API_KEY

def run_drishti(image_paths, lat, lng, pincode,
                shop_size=None, rent=None, years=None):

    image_data = run_image_engine(image_paths, GOOGLE_VISION_API_KEY)
    if not image_data:
        return {"error": "All images failed quality check. Please retake."}

    geo_data = run_geo_engine(lat, lng, pincode, GOOGLE_MAPS_API_KEY)

    visual_score = compute_visual_score(image_data)
    geo_score = compute_geo_score(geo_data)
    optional_score = compute_optional_score(shop_size, rent, years)
    drishti_score = compute_drishti_score(visual_score,
                                           geo_score,
                                           optional_score)

    cash_flow = estimate_cash_flow(drishti_score, visual_score, geo_score)
    fraud = run_fraud_engine(image_data, geo_data,
                              cash_flow["confidence_score"])

    return {
        "daily_sales_range": cash_flow["daily_sales_range"],
        "monthly_revenue_range": cash_flow["monthly_revenue_range"],
        "monthly_income_range": cash_flow["monthly_income_range"],
        "confidence_score": cash_flow["confidence_score"],
        "store_tier": cash_flow["store_tier"],
        "drishti_score": drishti_score,
        "visual_score": visual_score,
        "geo_score": geo_score,
        "risk_flags": fraud["risk_flags"],
        "fraud_score": fraud["fraud_score"],
        "recommendation": fraud["recommendation"],
        "image_signals": image_data,
        "geo_signals": geo_data
    }