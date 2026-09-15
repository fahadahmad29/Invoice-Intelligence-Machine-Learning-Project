import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flagging import predict_invoice_flag

#page configuration

st.set_page_config(
    page_title = "Vendor Invoice Intelligence Portal",
    page_icon = "📦",
    layout = "wide")

#custom styling (visual only — no app logic here)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #121212;
        color: #e0e0e0;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Hero header */
    .hero-box {
        background: linear-gradient(135deg, #0f2444 0%, #1b3b6f 55%, #2c5aa0 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 14px;
        color: #ffffff;
        margin-bottom: 1.4rem;
        box-shadow: 0 10px 26px rgba(15, 36, 68, 0.22);
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        font-weight: 500;
        color: #cfe0ff;
        margin-bottom: 1rem;
    }
    .hero-desc {
        font-size: 0.98rem;
        color: #e8eefc;
        line-height: 1.7;
    }
    .hero-badges {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .hero-badge {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.28);
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* Section text */
    h3, .stMarkdown h3 {
        color: #0f2444;
    }

    /* Forms as cards */
    div[data-testid="stForm"] {
        background: #1e1e1e;
        border: 1px solid #333333;
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }

    /* Ensure labels are white and bold for contrast against dark background */
    label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* Make the actual input boxes darker */
    input {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }

    /* Buttons */
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #1b3b6f, #2c5aa0);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.55rem 1.4rem;
        font-weight: 600;
        letter-spacing: 0.2px;
        transition: all 0.15s ease-in-out;
    }
    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 16px rgba(27, 59, 111, 0.3);
    }

    /* Metric card */
    div[data-testid="stMetric"] {
        background: #1e1e1e;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800;
    }
    div[data-testid="stMetricLabel"] {
        color: #cfcfcf !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 10px;
        font-weight: 500;
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f2444;
    }
    section[data-testid="stSidebar"] * {
        color: #eef3fc !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.18);
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

#header section
st.markdown("""
<div class="hero-box">
    <div class="hero-title">📦 Vendor Invoice Intelligence Portal</div>
    <div class="hero-subtitle">AI-Driven Freight Cost Prediction & Invoice Risk Flagging</div>
    <div class="hero-desc">
        This internal analytics portal leverages machine learning to forecast freight cost
        accurately, detect risky or abnormal vendor invoices, and reduce financial leakage
        and manual workload.
    </div>
    <div class="hero-badges">
        <div class="hero-badge">🚚 Freight Forecasting</div>
        <div class="hero-badge">🛡️ Risk Detection</div>
        <div class="hero-badge">⚡ Instant Predictions</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

#sidebar code 
st.sidebar.title("🧭 Model Selection")
selected_model = st.sidebar.radio(
    "Choose Prediction Model",
    [
        "Freight Cost Prediction",
        "Invoice Manual Approval Flag"
    ]
)

st.sidebar.markdown("""
---
**📈 Business Impact**
- Improve cost forecasting
- Reduced invoice fraud & anomalies
- Faster finance operations
""")

#freight cost prediction

if selected_model == "Freight Cost Prediction":
    st.subheader("🚚 Freight Cost Prediction")

    st.markdown("""
    **Objective:**
    Predict freight cost for a vendor invoice using **Dollars**
    to support budgeting, forecasting, and vendor negotiations.
    """)

    with st.form("freight_form"):
        col1 = st.columns(1)[0]

        with col1:
            dollars = st.number_input(
                "💵 Invoice Dollars",
                min_value=1.0,
                value = 18500.0
            )
        submit_freight = st.form_submit_button("🚀 Predict Freight Cost")

    if submit_freight:
        input_data = {
            "Dollars" : [dollars]
        }
        prediction = predict_freight_cost(input_data)['Predicted_Freight']

        st.success("Prediction completed successfully.")

        st.metric(
            label = "Estimated Freight Cost",
            value = f"${prediction[0]:,.2f}"
        )


#invoice flag prediction

else:
    st.subheader("🧾 Invoice Manual Approval Prediction")

    st.markdown("""
    **Objective:**
    Predict whether a vendor invoice should be **flagged for manual approval** 
    based on abnormal cost, freight, or delivery patterns. """)

    with st.form("invoice_flag_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            invoice_quantity = st.number_input(
                "📦 Invoice Quantity",
                min_value=1,
                value=50
            )
            freight = st.number_input(
                "🚚 Freight Cost",
                min_value = 0.0,
                value = 1.73
            )
        with col2:
            invoice_dollars = st.number_input(
                "💵 Invoice Dollars",
                min_value=1.0,
                value=352.95
            )
            total_item_quantity = st.number_input(
                "📊 Total Item Quantity",
                min_value = 1,
                value = 162
            )
        with col3:
            total_item_dollars = st.number_input(
                "💰 Total Item Dollars",
                min_value=1.0,
                value = 2476.0
            )
        submit_flag = st.form_submit_button("🔍 Evaluate Invoice Risk")

    if submit_flag:
        input_data = {
            "invoice_quantity" : [invoice_quantity],
            "invoice_dollars" : [invoice_dollars],
            "Freight" : [freight],
            "total_item_quantity" : [total_item_quantity],
            "total_item_dollars" : [total_item_dollars]
        }
        flag_prediction = predict_invoice_flag(input_data)['Predicted_Flag']

        is_flagged = bool(flag_prediction[0])

        if is_flagged:
            st.error("Invoice requires **MANUAL APPROVAL**")
        else:
            st.success("Invoice is **SAFE for Auto-Approval**")

st.markdown("""
<div style="text-align:center; color:#8a93a6; font-size:0.85rem; margin-top:2rem;">
    Vendor Invoice Intelligence Portal · ML-Powered Analytics
</div>
""", unsafe_allow_html=True)