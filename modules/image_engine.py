import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import requests
import base64

model = YOLO("yolov8n.pt")

def calculate_shelf_density(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    filled_pixels = np.count_nonzero(thresh)
    total_pixels = thresh.size
    sdi = filled_pixels / total_pixels
    return round(sdi, 2)

def detect_products(image_path):
    results = model(image_path)
    detected = []
    for r in results:
        for box in r.boxes:
            label = model.names[int(box.cls)]
            detected.append(label)
    sku_count = len(set(detected))
    sku_diversity_score = min(sku_count / 20, 1.0)
    return {
        "detected_items": detected,
        "sku_count": sku_count,
        "sku_diversity_score": round(sku_diversity_score, 2)
    }

def check_image_quality(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    blur = cv2.Laplacian(gray, cv2.CV_64F).var()
    quality_score = min((brightness / 128 + blur / 500) / 2, 1.0)
    is_acceptable = brightness > 40 and blur > 50
    return {
        "brightness": round(brightness, 2),
        "blur_score": round(blur, 2),
        "quality_score": round(quality_score, 2),
        "acceptable": is_acceptable
    }

def detect_brands_vision_api(image_path, api_key):
    try:
        with open(image_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")
        
        payload = {
            "requests": [{
                "image": {"content": content},
                "features": [
                    {"type": "LABEL_DETECTION", "maxResults": 20},
                    {"type": "TEXT_DETECTION"}
                ]
            }]
        }
        
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        response = requests.post(url, json=payload)
        data = response.json()

        # DEBUG — remove after fixing
        print("Vision API response:", data)

        # Check for API errors
        if "error" in data:
            print("Vision API error:", data["error"])
            return {"brands_detected": [], "brand_presence_score": 0.3}

        if "responses" not in data or not data["responses"]:
            print("No responses from Vision API")
            return {"brands_detected": [], "brand_presence_score": 0.3}

        response_data = data["responses"][0]

        # Check for response-level errors
        if "error" in response_data:
            print("Response error:", response_data["error"])
            return {"brands_detected": [], "brand_presence_score": 0.3}

        labels = [l["description"].lower() for l in
                  response_data.get("labelAnnotations", [])]

        known_brands = ["amul", "pepsi", "parle", "britannia",
                        "maggi", "haldiram", "coca cola", "dabur"]
        brand_hits = [b for b in known_brands if
                      any(b in label for label in labels)]
        brand_score = min(len(brand_hits) / 4, 1.0)

        return {
            "brands_detected": brand_hits,
            "brand_presence_score": round(brand_score, 2)
        }

    except Exception as e:
        print(f"Vision API exception: {e}")
        return {"brands_detected": [], "brand_presence_score": 0.3}

def detect_refill_signal(sdi):
    if 0.4 <= sdi <= 0.75:
        return {"refill_signal": True, "score": 0.8}
    elif sdi > 0.95:
        return {"refill_signal": False, "score": 0.3}
    else:
        return {"refill_signal": False, "score": 0.5}

def run_image_engine(image_paths, api_key):
    all_results = []
    for path in image_paths:
        quality = check_image_quality(path)
        if not quality["acceptable"]:
            all_results.append({"path": path, "skipped": True,
                                 "reason": "low quality"})
            continue
        sdi = calculate_shelf_density(path)
        products = detect_products(path)
        brands = detect_brands_vision_api(path, api_key)
        refill = detect_refill_signal(sdi)
        all_results.append({
            "path": path,
            "shelf_density_index": sdi,
            "sku_diversity_score": products["sku_diversity_score"],
            "sku_count": products["sku_count"],
            "brand_presence_score": brands["brand_presence_score"],
            "brands_detected": brands["brands_detected"],
            "refill_signal": refill["refill_signal"],
            "refill_score": refill["score"],
            "quality": quality
        })
    valid = [r for r in all_results if not r.get("skipped")]
    if not valid:
        return None
    avg = lambda key: sum(r[key] for r in valid) / len(valid)
    return {
        "shelf_density_index": round(avg("shelf_density_index"), 2),
        "sku_diversity_score": round(avg("sku_diversity_score"), 2),
        "brand_presence_score": round(avg("brand_presence_score"), 2),
        "refill_score": round(avg("refill_score"), 2),
        "image_count": len(valid),
        "skipped_count": len(all_results) - len(valid)
    }