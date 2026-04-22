def check_inventory_footfall_mismatch(sdi, footfall_score):
    if sdi > 0.9 and footfall_score < 0.3:
        return "inventory_footfall_mismatch"
    return None

def check_image_coverage(image_count):
    if image_count < 3:
        return "insufficient_image_coverage"
    return None

def check_brand_footfall_mismatch(brand_score, footfall_score):
    if brand_score > 0.8 and footfall_score < 0.2:
        return "brand_footfall_mismatch"
    return None

def check_cleanliness_anomaly(sdi, sku_score):
    if sdi > 0.98 and sku_score > 0.95:
        return "unusually_perfect_store"
    return None

def check_low_data_coverage(geo_data):
    scores = [
        geo_data.get("footfall_proxy_score", 0),
        geo_data.get("catchment_score", 0),
        geo_data.get("area_income_score", 0)
    ]
    if sum(scores) / len(scores) < 0.2:
        return "limited_geo_data_coverage"
    return None

def get_recommendation(flags, confidence):
    if len(flags) >= 2 or confidence < 0.4:
        return "reject"
    elif len(flags) == 1 or confidence < 0.6:
        return "needs_verification"
    else:
        return "approve"

def run_fraud_engine(image_data, geo_data, confidence):
    flags = []
    checks = [
        check_inventory_footfall_mismatch(
            image_data.get("shelf_density_index", 0),
            geo_data.get("footfall_proxy_score", 0)
        ),
        check_image_coverage(image_data.get("image_count", 0)),
        check_brand_footfall_mismatch(
            image_data.get("brand_presence_score", 0),
            geo_data.get("footfall_proxy_score", 0)
        ),
        check_cleanliness_anomaly(
            image_data.get("shelf_density_index", 0),
            image_data.get("sku_diversity_score", 0)
        ),
        check_low_data_coverage(geo_data)
    ]
    flags = [c for c in checks if c is not None]
    recommendation = get_recommendation(flags, confidence)
    return {
        "risk_flags": flags,
        "fraud_score": round(len(flags) / 5, 2),
        "recommendation": recommendation
    }