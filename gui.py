import numpy as np
import requests
import streamlit as st

st.set_page_config(page_title="Housing Price Predictor", page_icon="🏠")

API_URL = "http://api:5000/predict"

st.title("🏠 توقع سعر الشقة/البيت")
st.caption(
    "ترتيب الفيتشرز تحت لازم يبقى **نفس ترتيب التدريب بالظبط**. "
    "لو مش متأكد من الترتيب، ارجع لكود التدريب وأكد عليه."
)

col1, col2 = st.columns(2)

with col1:
    bedrooms = st.number_input("عدد الأوض (bedrooms)", min_value=0, value=3, step=1)
    bathrooms = st.number_input("عدد الحمامات (bathrooms)", min_value=0, value=1, step=1)
    stories = st.number_input("عدد الأدوار (stories)", min_value=0, value=1, step=1)
    parking = st.number_input("عدد أماكن الباركينج (parking)", min_value=0, value=0, step=1)
    area = st.number_input("المساحة (area) بالمتر/القدم", min_value=1.0, value=3000.0)

with col2:
    mainroad = st.selectbox("على شارع رئيسي؟ (mainroad)", ["yes", "no"])
    guestroom = st.selectbox("فيه غرفة ضيوف؟ (guestroom)", ["yes", "no"])
    basement = st.selectbox("فيه بدروم؟ (basement)", ["yes", "no"])
    hotwaterheating = st.selectbox("سخان مياه مركزي؟ (hotwaterheating)", ["yes", "no"])
    airconditioning = st.selectbox("تكييف؟ (airconditioning)", ["yes", "no"])
    prefarea = st.selectbox("في منطقة مميزة؟ (prefarea)", ["yes", "no"])
    furnishingstatus = st.selectbox(
        "حالة الفرش (furnishingstatus)",
        ["furnished", "semi-furnished", "unfurnished"],
    )

yes_no = {"yes": 1, "no": 0}
furnishing_map = {"furnished": 2, "semi-furnished": 1, "unfurnished": 0}

if st.button("احسب السعر المتوقع", type="primary"):
    area_log = np.log(area)

    features = [
        bedrooms,
        bathrooms,
        stories,
        yes_no[mainroad],
        yes_no[guestroom],
        yes_no[basement],
        yes_no[hotwaterheating],
        yes_no[airconditioning],
        parking,
        yes_no[prefarea],
        furnishing_map[furnishingstatus],
        area_log,
    ]

    try:
        response = requests.post(API_URL, json={"features": features}, timeout=10)
        response.raise_for_status()
        result = response.json()

        if "predictions" in result:
            price_log_pred = result["predictions"][0]
            price_pred = np.exp(price_log_pred)
            st.success(f"السعر المتوقع تقريبًا: **{price_pred:,.0f}**")
            st.caption(f"(price_log المتوقع = {price_log_pred:.4f})")
        else:
            st.error(f"رد غير متوقع من الـ API: {result}")

    except requests.exceptions.RequestException as e:
        st.error(f"مقدرتش أوصل للـ API: {e}")
