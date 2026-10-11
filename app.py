import os
import requests
import streamlit as st

API_URL = st.secrets.get(
    "API_URL",
    os.getenv("API_URL", "http://127.0.0.1:8000")
)
st.set_page_config(
    page_title="ShopSense | Purchase Intelligence",
    page_icon="🛍️",
    layout="wide",
)

st.title("🛍️ ShopSense")
st.subheader("Online Purchase Intention")
st.write(
    "Estimate purchase probability from an online shopping session "
    "using a trained machine learning model."
)

st.info(
    "This is a session-level research prototype, not a validated "
    "real-time production prediction system."
)

with st.sidebar:
    st.header("About ShopSense")
    st.write("Model: Random Forest")
    st.write("Decision threshold: 37%")
    st.write("Prediction API: FastAPI")

st.header("Shopping session")

with st.form("session_form"):
    col1, col2 = st.columns(2)

    with col1:
        administrative = st.number_input(
            "Administrative pages visited", min_value=0, value=1
        )
        administrative_duration = st.number_input(
            "Administrative duration", min_value=0.0, value=20.0
        )
        informational = st.number_input(
            "Informational pages visited", min_value=0, value=0
        )
        informational_duration = st.number_input(
            "Informational duration", min_value=0.0, value=0.0
        )
        product_related = st.number_input(
            "Product-related pages visited", min_value=0, value=5
        )
        product_duration = st.number_input(
            "Product-related duration", min_value=0.0, value=100.0
        )
        page_values = st.number_input(
            "Page values", min_value=0.0, value=0.0
        )
        special_day = st.number_input(
            "Special-day proximity", min_value=0.0,
            max_value=1.0, value=0.0, step=0.1
        )
        weekend = st.checkbox("Weekend session")

    with col2:
        bounce_rates = st.number_input(
            "Bounce rate", min_value=0.0, max_value=1.0,
            value=0.02, step=0.01, format="%.4f"
        )
        exit_rates = st.number_input(
            "Exit rate", min_value=0.0, max_value=1.0,
            value=0.04, step=0.01, format="%.4f"
        )
        month = st.selectbox(
            "Month",
            ["Feb", "Mar", "May", "June", "Jul",
             "Aug", "Sep", "Oct", "Nov", "Dec"]
        operating_system = st.number_input(
            "Operating system code", min_value=1, value=2
        )
        browser = st.number_input(
            "Browser code", min_value=1, value=2
        )
        region = st.number_input(
            "Region code", min_value=1, value=1
        )
        traffic_type = st.number_input(
            "Traffic type code", min_value=1, value=2
        )
        visitor_type = st.selectbox(
            "Visitor type",
            ["Returning_Visitor", "New_Visitor", "Other"]
        )

    submitted = st.form_submit_button(
        "Predict purchase intention", type="primary"
    )

if submitted:
    payload = {
        "Administrative": administrative,
        "Administrative_Duration": administrative_duration,
        "Informational": informational,
        "Informational_Duration": informational_duration,
        "ProductRelated": product_related,
        "ProductRelated_Duration": product_duration,
        "BounceRates": bounce_rates,
        "ExitRates": exit_rates,
        "PageValues": page_values,
        "SpecialDay": special_day,
        "Month": month,
        "OperatingSystems": operating_system,
        "Browser": browser,
        "Region": region,
        "TrafficType": traffic_type,
        "VisitorType": visitor_type,
        "Weekend": weekend,
    }

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        result = response.json()

        probability = result["purchase_probability"]
        prediction = result["predicted_purchase"]

        st.divider()
        st.header("Prediction result")

        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric(
            "Estimated purchase probability",
            f"{probability:.2%}",
        )
        metric_col2.metric(
            "Model decision",
            "Purchase predicted" if prediction == 1 else "No purchase predicted",
        )

        st.progress(probability)

        st.caption(
            f"Decision threshold: {result['decision_threshold']:.0%}. "
            "The probability is a model estimate, not a guarantee."
        )

    except requests.RequestException as exc:
        st.error(
            "Could not reach the prediction API. "
            "Check that FastAPI is running on port 8000."
        )
        st.caption(str(exc))
