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
    [out:json][timeout:25];
    node["shop"="convenience"](around:500,{lat},{lng});
    out count;
    """
    url = "https://overpass-api.de/api/interpreter"
    
    try:
        response = requests.post(
            url, 
            data=query,
            timeout=30,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Check if response is valid
        if response.status_code != 200:
            print(f"Overpass API status: {response.status_code}")
            return {"competitor_count": 3, "competition_score": 0.6}
        
        # Check if response is actually JSON
        content_type = response.headers.get("Content-Type", "")
        if "json" not in content_type and "text" not in content_type:
            print(f"Unexpected content type: {content_type}")
            return {"competitor_count": 3, "competition_score": 0.6}

        text = response.text.strip()
        if not text or text.startswith("<"):
            print("Overpass returned HTML or empty — using fallback")
            return {"competitor_count": 3, "competition_score": 0.6}

        data = response.json()
        count = 0
        if "elements" in data:
            for el in data["elements"]:
                if el.get("tags", {}).get("total"):
                    count = int(el["tags"]["total"])
                    break

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

    except requests.exceptions.Timeout:
        print("Overpass API timed out — using fallback")
        return {"competitor_count": 3, "competition_score": 0.6}
    
    except requests.exceptions.ConnectionError:
        print("Overpass API connection failed — using fallback")
        return {"competitor_count": 3, "competition_score": 0.6}

    except Exception as e:
        print(f"Overpass API error: {e} — using fallback")
        return {"competitor_count": 3, "competition_score": 0.6}

def get_catchment_population(lat, lng):
    query = f"""
    [out:json][timeout:25];
    node["place"~"village|suburb|neighbourhood"](around:1000,{lat},{lng});
    out;
    """
    url = "https://overpass-api.de/api/interpreter"
    
    try:
        response = requests.post(
            url,
            data=query,
            timeout=30,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code != 200:
            return {"area_count": 3, "catchment_score": 0.5}

        text = response.text.strip()
        if not text or text.startswith("<"):
            print("Overpass catchment returned HTML — using fallback")
            return {"area_count": 3, "catchment_score": 0.5}

        data = response.json()
        count = len(data.get("elements", []))
        catchment_score = min(count / 10, 1.0)

        return {
            "area_count": count,
            "catchment_score": round(catchment_score, 2)
        }

    except requests.exceptions.Timeout:
        print("Overpass catchment timed out — using fallback")
        return {"area_count": 3, "catchment_score": 0.5}

    except Exception as e:
        print(f"Overpass catchment error: {e} — using fallback")
        return {"area_count": 3, "catchment_score": 0.5}
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