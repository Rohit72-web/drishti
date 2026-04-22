import streamlit as st
import tempfile
import os
from modules.output_engine import run_drishti

st.set_page_config(page_title="DRISHTI", layout="wide")
st.title("DRISHTI — Kirana Store Underwriting Engine")
st.caption("Deep Retail Intelligence for Store Health & Transaction Inference")

with st.sidebar:
    st.header("Store Details")
    lat = st.number_input("Latitude", value=19.0760)
    lng = st.number_input("Longitude", value=72.8777)
    pincode = st.text_input("Pincode", value="400001")
    st.subheader("Optional Inputs")
    shop_size = st.number_input("Shop size (sq ft)", value=0)
    rent = st.number_input("Monthly rent (Rs)", value=0)
    years = st.number_input("Years in operation", value=0)

images = st.file_uploader(
    "Upload 3-5 shop images (shelf, counter, exterior)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if st.button("Run DRISHTI Analysis") and images:
    with st.spinner("Analysing store..."):
        tmp_paths = []
        for img in images:
            tmp = tempfile.NamedTemporaryFile(delete=False,
                                               suffix=".jpg")
            tmp.write(img.read())
            tmp_paths.append(tmp.name)

        result = run_drishti(
            tmp_paths, lat, lng, pincode,
            shop_size or None, rent or None, years or None
        )

        for p in tmp_paths:
            os.unlink(p)

    if "error" in result:
        st.error(result["error"])
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Daily Sales Range",
                    f"Rs {result['daily_sales_range'][0]:,} – "
                    f"{result['daily_sales_range'][1]:,}")
        col2.metric("Monthly Revenue",
                    f"Rs {result['monthly_revenue_range'][0]:,} – "
                    f"{result['monthly_revenue_range'][1]:,}")
        col3.metric("Confidence Score",
                    f"{result['confidence_score']}")
        col4.metric("Recommendation",
                    result["recommendation"].upper())

        st.subheader("Scores")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("DRISHTI Score", result["drishti_score"])
        c2.metric("Visual Score", result["visual_score"])
        c3.metric("Geo Score", result["geo_score"])
        c4.metric("Fraud Score", result["fraud_score"])

        if result["risk_flags"]:
            st.warning("Risk Flags Detected")
            for flag in result["risk_flags"]:
                st.error(f"🚩 {flag}")
        else:
            st.success("No fraud flags detected")

        with st.expander("Image Signals"):
            st.json(result["image_signals"])

        with st.expander("Geo Signals"):
            st.json(result["geo_signals"])

        with st.expander("Full JSON Output"):
            st.json(result)