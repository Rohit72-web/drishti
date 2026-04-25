# DRISHTI
### Deep Retail Intelligence for Store Health & Transaction Inference

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Latest-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **"Where a Camera Sees a Shop, DRISHTI Sees a Balance Sheet"**

*A remote cash flow underwriting system for kirana stores using Vision + Geo Intelligence*

Built for **Poonawalla Fincorp Hackathon 2026** — Problem Statement: Remote Cash Flow Underwriting for Kirana Stores

</div>

---

## Table of Contents

- [What is DRISHTI](#what-is-drishti)
- [The Problem We Are Solving](#the-problem-we-are-solving)
- [How DRISHTI Works](#how-drishti-works)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the App](#running-the-app)
- [Running the API](#running-the-api)
- [API Reference](#api-reference)
- [Output Format](#output-format)
- [Datasets Used](#datasets-used)
- [Fraud Detection](#fraud-detection)
- [Limitations](#limitations)
- [Future Roadmap](#future-roadmap)
- [Team](#team)

---

## What is DRISHTI

DRISHTI is a remote underwriting engine that estimates the cash flow of a kirana store using only shop images and GPS coordinates — no bank statements, no GST records, no field officer visits required.

It reads a kirana store the way a bank reads a balance sheet:
- **Shelves** = working capital deployed
- **Products** = revenue velocity
- **Location** = demand potential
- **Brands** = creditworthiness signal

DRISHTI combines computer vision, geo intelligence, and economic reasoning to produce a calibrated, fraud-resistant cash flow estimate with a confidence score.

---

## The Problem We Are Solving

India has **13 million kirana stores** that collectively drive ₹50 lakh crore in annual retail. Yet less than 3% have access to formal credit.

Why? Because they have:
- No ITR or GST filings
- No formal bookkeeping
- No transaction history
- No credit bureau score

NBFCs like Poonawalla Fincorp want to lend to this segment but cannot underwrite what they cannot measure.

**Existing approaches fail:**

| Approach | Problem |
|---|---|
| Field officer surveys | ₹800–1,500 per visit, 4–5 visits/day max, subjective |
| Bank statement analysis | 90% of kiranas have no formal bank account |
| GST records | Majority are unregistered |
| CIBIL score | Zero credit history — score does not exist |
| Generic AI models | Built on digital footprints kiranas do not have |

**DRISHTI's approach:** Go to where the data actually lives — the physical shop itself.

---

## How DRISHTI Works

### 3 Pillars

**Pillar 1 — Visual Intelligence**
Reads the physical store through images. Detects products, measures shelf density, identifies brands, estimates inventory value, reads store zones.

**Pillar 2 — Geo Intelligence**
Reads the store's economic environment. Analyses catchment population, road type, nearby demand drivers, competition density, area income level.

**Pillar 3 — Fusion Engine**
Combines visual and geo signals using weighted scoring and quantile regression to produce calibrated cash flow ranges with confidence scores.

### 8-Step Pipeline

```
Step 1 → Field agent uploads 3–5 shop images + GPS coordinates
Step 2 → Image processing: YOLOv8 detects products, Vision API reads brands, OpenCV checks quality
Step 3 → Geo processing: Maps API pulls POIs, Overpass counts competitors, Census gives income
Step 4 → Feature engine converts all raw signals to normalised 0–1 scores
Step 5 → Fraud engine runs 5 parallel checks for inconsistencies
Step 6 → Fusion model combines all scores using quantile regression
Step 7 → FastAPI returns clean JSON with sales range, confidence, risk flags, recommendation
Step 8 → Streamlit dashboard displays everything visually for the loan officer
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                          │
│           Images + GPS Coordinates + Optional Data          │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│    IMAGE     │ │   GEO    │ │   OPTIONAL   │
│  PROCESSING  │ │  ENGINE  │ │    INPUTS    │
│  YOLOv8     │ │  GMaps   │ │  shop size   │
│  Vision API │ │  Overpass│ │  rent, years │
│  OpenCV     │ │  Census  │ │              │
└──────┬───────┘ └────┬─────┘ └──────┬───────┘
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
            ┌──────────────────┐
            │ FEATURE ENGINE   │
            │ 11 visual scores │
            │ 8 geo scores     │
            │ Python + Pandas  │
            └────────┬─────────┘
                     │
         ┌───────────┼───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│  FUSION MODEL   │    │  FRAUD DETECTOR  │
│  Scikit-learn   │    │  5 rule checks   │
│  Quantile Regr  │    │  OpenCV cross    │
│  Cash flow range│    │  validation      │
└────────┬────────┘    └────────┬─────────┘
         │                      │
         └──────────┬───────────┘
                    │
                    ▼
          ┌──────────────────┐
          │   FASTAPI OUTPUT │
          │   JSON Response  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ STREAMLIT DASH   │
          │ Gauge + Map +    │
          │ Risk flags +     │
          │ Recommendation   │
          └──────────────────┘
```

---

## Features

### Visual Intelligence
- **Shelf Density Index (SDI)** — measures how full the shelves are (0–1 score)
- **SKU Diversity Score** — counts distinct product categories detected
- **Brand Presence Score** — identifies trusted FMCG brands (Amul, Pepsi, Parle etc.)
- **Refill Signal** — partially empty shelves indicate recent sales activity
- **Image Quality Check** — flags dark, blurry, or incomplete images before processing
- **Counter Activity Score** — detects UPI QR codes and payment infrastructure

### Geo Intelligence
- **Catchment Population Score** — people within 1km radius of the shop
- **Footfall Proxy Index** — road type, nearby schools, offices, hospitals, transport
- **Competition Density** — number of rival shops within 500m
- **Area Income Score** — pincode-level spending power from Census data

### Fusion and Output
- **Quantile Regression** — produces honest cash flow RANGES not single numbers
- **Economic Guardrails** — output never exceeds real-world kirana benchmarks
- **Confidence Score** — tells loan officer how much to trust the output
- **Store Tier Classification** — small / medium / large / semi-wholesale
- **Fraud Detection** — 5 automated checks with risk flags
- **JSON API Output** — directly pluggable into any NBFC loan management system

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | Image upload, form, live dashboard |
| Backend API | FastAPI + Uvicorn | Production-ready REST API |
| Object Detection | YOLOv8 (Ultralytics) | Product detection on shelf images |
| Image Reading | Google Cloud Vision API | Brand names, text, logos from images |
| Image Processing | OpenCV | Quality checks, size estimation |
| Geo — POIs | Google Maps Places API | Nearby schools, offices, hospitals |
| Geo — Competitors | Overpass API (OpenStreetMap) | Competition density, population |
| Geo — Income | Census of India CSV | Pincode-level area income |
| Feature Engineering | Pandas + NumPy | Convert raw signals to 0–1 scores |
| ML Model | Scikit-learn | Quantile regression fusion model |
| GPS Processing | GeoPy + Shapely | Coordinate and catchment calculations |
| Map Display | Folium | Interactive map in dashboard |

**Total licensing cost — Rs 0. Everything is open source or free tier.**

---

## Project Structure

```
DRISHTI/
├── app.py                    ← Streamlit frontend dashboard
├── api.py                    ← FastAPI backend REST API
├── config.example.py         ← API key template (safe to commit)
├── requirements.txt          ← All Python dependencies
├── README.md                 ← This file
├── .gitignore                ← Excludes config.py and secrets
│
├── modules/
│   ├── __init__.py
│   ├── image_engine.py       ← YOLOv8 + OpenCV + Vision API
│   ├── geo_engine.py         ← Google Maps + Overpass API + Census
│   ├── feature_engine.py     ← Converts raw data to 0-1 scores
│   ├── fusion_model.py       ← Quantile regression cash flow model
│   ├── fraud_engine.py       ← 5 fraud detection checks
│   └── output_engine.py      ← Orchestrates full pipeline, returns JSON
│
├── data/
│   ├── benchmark.json        ← Kirana revenue benchmarks (RBI + NABARD)
│   ├── fmcg_prices.json      ← 95 Indian products with price bands
│   └── census_pincode.csv    ← 115 Indian pincodes with income data
│
└── assets/
    └── sample_images/        ← Test kirana store images
```

---

## Setup and Installation

### Prerequisites
- Python 3.10 or higher
- Google Cloud account (for Vision API and Maps API keys)
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/DRISHTI.git
cd DRISHTI
```

### Step 2 — Create virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up API keys

Copy the example config file:
```bash
# Windows
copy config.example.py config.py

# Mac / Linux
cp config.example.py config.py
```

Open `config.py` and add your actual API keys:
```python
GOOGLE_VISION_API_KEY = "your_actual_vision_api_key"
GOOGLE_MAPS_API_KEY = "your_actual_maps_api_key"
```

### Step 5 — Get API Keys

**Google Cloud Vision API:**
1. Go to console.cloud.google.com
2. Create a new project
3. Enable Cloud Vision API
4. Go to APIs and Services → Credentials → Create API Key
5. Copy the key into config.py

**Google Maps API:**
1. Same Google Cloud project
2. Enable Maps JavaScript API and Places API
3. Use the same or a new API key

Both have free tiers that cover all development and prototype usage.

---

## Running the App

### Streamlit Dashboard
```bash
python -m streamlit run app.py
```
Opens automatically at `http://localhost:8501`

### How to use the dashboard
1. Enter GPS coordinates (latitude and longitude) in the sidebar
2. Enter the shop's pincode
3. Optionally enter shop size, rent, and years in operation
4. Upload 3 to 5 shop images (shelf, counter, exterior)
5. Click **Run DRISHTI Analysis**
6. View results — cash flow range, confidence score, risk flags, recommendation

---

## Running the API

### FastAPI Backend
```bash
uvicorn api:app --reload
```
API runs at `http://localhost:8000`

Auto-generated documentation at `http://localhost:8000/docs`

---

## API Reference

### POST /analyse

Analyse a kirana store and return cash flow estimate.

**Request — multipart/form-data**

| Field | Type | Required | Description |
|---|---|---|---|
| images | file[] | Yes | 3–5 shop images (jpg/png) |
| lat | float | Yes | Shop latitude |
| lng | float | Yes | Shop longitude |
| pincode | string | Yes | Shop pincode |
| shop_size | float | No | Floor area in sq ft |
| rent | float | No | Monthly rent in Rs |
| years | float | No | Years in operation |

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/analyse" \
  -F "images=@shelf.jpg" \
  -F "images=@counter.jpg" \
  -F "images=@exterior.jpg" \
  -F "lat=19.0760" \
  -F "lng=72.8777" \
  -F "pincode=400001" \
  -F "shop_size=200" \
  -F "rent=8000" \
  -F "years=5"
```

---

## Output Format

```json
{
  "daily_sales_range": [6000, 9000],
  "monthly_revenue_range": [180000, 270000],
  "monthly_income_range": [25000, 45000],
  "confidence_score": 0.72,
  "store_tier": "medium",
  "drishti_score": 0.61,
  "visual_score": 0.58,
  "geo_score": 0.67,
  "risk_flags": [
    "inventory_footfall_mismatch"
  ],
  "fraud_score": 0.20,
  "recommendation": "needs_verification",
  "image_signals": {
    "shelf_density_index": 0.74,
    "sku_diversity_score": 0.45,
    "brand_presence_score": 0.50,
    "refill_score": 0.80,
    "image_count": 3,
    "skipped_count": 0
  },
  "geo_signals": {
    "footfall_proxy_score": 0.65,
    "poi_count": 8,
    "competition_score": 0.60,
    "competitor_count": 3,
    "catchment_score": 0.55,
    "area_income_score": 0.72
  }
}
```

### Field Definitions

| Field | Range | Meaning |
|---|---|---|
| daily_sales_range | Rs | Estimated lower and upper daily sales |
| monthly_revenue_range | Rs | Estimated monthly revenue band |
| monthly_income_range | Rs | Estimated net monthly income after costs |
| confidence_score | 0–1 | How reliable is this estimate (0.9 = very confident) |
| store_tier | small/medium/large/semi_wholesale | Store classification |
| drishti_score | 0–1 | Overall composite score |
| visual_score | 0–1 | Score from image analysis only |
| geo_score | 0–1 | Score from location analysis only |
| risk_flags | list | Specific fraud or quality warnings |
| fraud_score | 0–1 | Overall fraud risk (0 = clean, 1 = high risk) |
| recommendation | approve/needs_verification/reject | Suggested loan action |

---

## Datasets Used

### benchmark.json
Revenue benchmarks for 4 kirana store tiers sourced from:
- RBI Annual Report 2023
- NABARD Kirana Credit Study 2022
- CRISIL MSME Report 2023

Includes regional multipliers (metro/tier1/tier2/rural), seasonal multipliers for all 12 months, POI footfall boosts, road type multipliers, and competition impact scoring.

### fmcg_prices.json
95 real Indian FMCG products across 10 categories:
- Staples, dairy, beverages, snacks, biscuits, instant food, personal care, household, tobacco, confectionery
- Each product has market price, brand, margin percentage, and sales velocity
- Source: BigBasket and JioMart public listings January 2024

### census_pincode.csv
115 Indian pincodes across Bihar, Maharashtra, Delhi, Karnataka, Uttar Pradesh with:
- Population estimates
- Average household income
- Tier classification (metro/tier1/tier2/tier3/rural)
- Digital payment adoption rate
- Kirana store density per sq km
- State-level economic multipliers

---

## Fraud Detection

DRISHTI runs 5 automated fraud checks on every assessment:

| Check | What it detects |
|---|---|
| Inventory Footfall Mismatch | High stock in low traffic area — possible borrowed inventory |
| Insufficient Image Coverage | Less than 3 images — incomplete view of store |
| Brand Footfall Mismatch | Premium brands in very low footfall area — suspicious |
| Cleanliness Anomaly | Unusually perfect store — possible inspection-day staging |
| Low Geo Data Coverage | Sparse location data — confidence automatically reduced |

When 2 or more flags are raised the recommendation changes to `needs_verification` or `reject`. A human loan officer reviews all flagged cases.

---

## Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Image quality dependency | Low accuracy on dark or blurry images | Image quality checker requests retake |
| YOLOv8 not trained on Indian products | Generic object detection only | Fine-tune on kirana images in v2 |
| No ground truth training data | Heuristic formula not ML-trained weights | Collect real sales data for v2 |
| Overpass API unreliable | Geo signals may use fallback values | Fallback values maintain system stability |
| Census data covers 115 pincodes | Unknown pincodes use median values | Expand dataset in v2 |
| Seasonal variation | Festival stock looks like high steady sales | Month-based flags added |
| Regional model bias | Mumbai weights may not suit rural Bihar | Regional benchmarks partially address this |

---

## Future Roadmap

### Phase 2 — Month 1–6
- Fine-tune YOLOv8 on 1,000+ labelled Indian kirana images
- Peer benchmarking — compare shop against similar nearby shops
- Mobile app for field officers (React Native on FastAPI)
- Regional calibration with separate benchmarks per state
- Loan sizing module — recommend exact loan amount from income estimate

### Phase 3 — Month 6–12
- Seasonality intelligence — full multiplier model for 12 months
- Video analysis mode — 10 second shop video instead of static images
- Continuous learning pipeline — every loan outcome improves the model
- Full LMS integration for NBFC loan management systems
- RBI audit logging and compliance layer

### Phase 4 — Year 1–3
- DRISHTI Credit Bureau — India's first physical-world credit score
- Expand beyond kiranas to all informal businesses
- Government integration with SIDBI, NABARD, Mudra schemes
- International expansion — Bangladesh, Indonesia, Nigeria, Brazil

---

## Team

Built by 3 B.Tech CSE students for Poonawalla Fincorp Hackathon 2025.

| Member | Role |
|---|---|
| Member 1 | Solution architecture + fusion model + economic logic |
| Member 2 | Visual intelligence + YOLOv8 + fraud detection |
| Member 3 | Geo intelligence + Streamlit dashboard + presentation |

---

## Important Notes

- `config.py` is excluded from this repository via `.gitignore`
- Never commit your API keys to GitHub
- Use `config.example.py` as a template to create your own `config.py`
- All datasets in the `data/` folder are synthetic or publicly available — no proprietary data

---

## License

MIT License — free to use, modify, and distribute with attribution.

---

<div align="center">

**DRISHTI — A credit bureau for the physical world**

*13 million stores. Zero balance sheets. One solution.*

</div>
