def compute_visual_score(image_data):
    sdi = image_data.get("shelf_density_index", 0.5)
    sku = image_data.get("sku_diversity_score", 0.5)
    brand = image_data.get("brand_presence_score", 0.5)
    refill = image_data.get("refill_score", 0.5)
    visual_score = (
        sdi * 0.35 +
        sku * 0.25 +
        brand * 0.25 +
        refill * 0.15
    )
    return round(visual_score, 2)

def compute_geo_score(geo_data):
    footfall = geo_data.get("footfall_proxy_score", 0.5)
    competition = geo_data.get("competition_score", 0.5)
    catchment = geo_data.get("catchment_score", 0.5)
    income = geo_data.get("area_income_score", 0.5)
    geo_score = (
        footfall * 0.35 +
        catchment * 0.25 +
        income * 0.25 +
        competition * 0.15
    )
    return round(geo_score, 2)

def compute_optional_score(shop_size=None, rent=None, years=None):
    score = 0.5
    if shop_size:
        score += min(shop_size / 500, 1.0) * 0.1
    if rent:
        score += min(rent / 20000, 1.0) * 0.05
    if years:
        score += min(years / 20, 1.0) * 0.1
    return round(min(score, 1.0), 2)

def compute_drishti_score(visual_score, geo_score, optional_score,
                           visual_w=0.50, geo_w=0.35, opt_w=0.15):
    score = (visual_score * visual_w +
             geo_score * geo_w +
             optional_score * opt_w)
    return round(score, 2)