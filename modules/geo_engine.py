import requests
import pandas as pd

def get_road_type(lat, lng, api_key):
    url = f"https://roads.googleapis.com/v1/nearestRoads?points={lat},{lng}&key={api_key}"
    r = requests.get(url).json()
    return r

def get_nearby_pois(lat, lng, api_key):
    types = ["school", "hospital", "bus_station",
             "shopping_mall", "office"]
    poi_count = 0
    for place_type in types:
        url = (f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
               f"?location={lat},{lng}&radius=1000"
               f"&type={place_type}&key={api_key}")
        r = requests.get(url).json()
        poi_count += len(r.get("results", []))
    footfall_proxy = min(poi_count / 20, 1.0)
    return {
        "poi_count": poi_count,
        "footfall_proxy_score": round(footfall_proxy, 2)
    }

def get_competition_density(lat, lng):
    query = f"""
    [out:json];
    node["shop"="convenience"](around:500,{lat},{lng});
    out count;
    """
    url = "https://overpass-api.de/api/interpreter"
    r = requests.post(url, data=query).json()
    count = r.get("elements", [{}])[0].get("tags", {}).get("total", 0)
    count = int(count) if count else 0
    if count <= 2:
        score = 0.8
    elif count <= 5:
        score = 0.6
    elif count <= 10:
        score = 0.4
    else:
        score = 0.2
    return {
        "competitor_count": count,
        "competition_score": round(score, 2)
    }

def get_catchment_population(lat, lng):
    query = f"""
    [out:json];
    node["place"~"village|suburb|neighbourhood"](around:1000,{lat},{lng});
    out;
    """
    url = "https://overpass-api.de/api/interpreter"
    r = requests.post(url, data=query).json()
    count = len(r.get("elements", []))
    catchment_score = min(count / 10, 1.0)
    return {
        "area_count": count,
        "catchment_score": round(catchment_score, 2)
    }

def get_area_income(pincode, census_path="data/census_pincode.csv"):
    try:
        df = pd.read_csv(census_path)
        row = df[df["pincode"] == int(pincode)]
        if row.empty:
            return {"area_income_score": 0.5}
        income = row["avg_income"].values[0]
        max_income = df["avg_income"].max()
        score = income / max_income
        return {"area_income_score": round(score, 2)}
    except:
        return {"area_income_score": 0.5}

def run_geo_engine(lat, lng, pincode, api_key):
    pois = get_nearby_pois(lat, lng, api_key)
    competition = get_competition_density(lat, lng)
    catchment = get_catchment_population(lat, lng)
    income = get_area_income(pincode)
    return {
        "footfall_proxy_score": pois["footfall_proxy_score"],
        "poi_count": pois["poi_count"],
        "competition_score": competition["competition_score"],
        "competitor_count": competition["competitor_count"],
        "catchment_score": catchment["catchment_score"],
        "area_income_score": income["area_income_score"]
    }