import streamlit as st
import pandas as pd
import joblib
import sqlite3
from datetime import date
import os

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SalesAI | Sales Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SESSION STATE
# =========================================================

if "night_mode" not in st.session_state:
    st.session_state.night_mode = True

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None


# =========================================================
# THEME
# =========================================================

if st.session_state.night_mode:

    BG = "#07111F"
    CARD = "#0D1B2A"
    CARD_2 = "#10243A"
    TEXT = "#F8FAFC"
    MUTED = "#94A3B8"
    BORDER = "#1E3A5F"
    INPUT_BG = "#0B1726"

else:

    BG = "#F4F7FB"
    CARD = "#FFFFFF"
    CARD_2 = "#F8FAFC"
    TEXT = "#0F172A"
    MUTED = "#64748B"
    BORDER = "#D9E2EC"
    INPUT_BG = "#FFFFFF"


# =========================================================
# PROFESSIONAL CSS
# =========================================================

st.html(
    f"""
<style>

    /* ---------------- GLOBAL ---------------- */

    .stApp {{
        background:
            radial-gradient(
                circle at 15% 5%,
                rgba(37,99,235,0.13),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 10%,
                rgba(6,182,212,0.10),
                transparent 25%
            ),
            {BG};

        color: {TEXT};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                #081421 0%,
                #0A1728 100%
            );

        border-right: 1px solid #19304B;
    }}

    [data-testid="stSidebar"] * {{
        color: #E2E8F0 !important;
    }}

    /* ---------------- TEXT ---------------- */

    h1, h2, h3, h4 {{
        color: {TEXT} !important;
        letter-spacing: -0.3px;
    }}

    p {{
        color: {MUTED};
    }}

    /* ---------------- HERO ---------------- */

    .hero {{
        position: relative;
        overflow: hidden;

        padding: 42px 46px;
        margin-bottom: 30px;

        border-radius: 26px;

        background:
            linear-gradient(
                135deg,
                #0F3B82 0%,
                #312E81 48%,
                #075985 100%
            );

        border: 1px solid rgba(148,163,184,0.22);

        box-shadow:
            0 25px 70px rgba(15,23,42,0.28);
    }}

    .hero::before {{
        content: "";
        position: absolute;

        width: 320px;
        height: 320px;

        right: -90px;
        top: -130px;

        border-radius: 50%;

        background: rgba(255,255,255,0.08);
    }}

    .hero::after {{
        content: "";
        position: absolute;

        width: 220px;
        height: 220px;

        right: 160px;
        bottom: -150px;

        border-radius: 50%;

        background: rgba(34,211,238,0.10);
    }}

    .hero-content {{
        position: relative;
        z-index: 2;
    }}

    .hero-badge {{
        display: inline-block;

        padding: 7px 13px;

        margin-bottom: 16px;

        border-radius: 999px;

        background: rgba(255,255,255,0.13);

        border: 1px solid rgba(255,255,255,0.20);

        color: #E0F2FE;

        font-size: 12px;
        font-weight: 700;

        letter-spacing: 0.8px;
    }}

    .hero-title {{
        font-size: 46px;
        font-weight: 850;

        color: white !important;

        margin: 0;
    }}

    .hero-subtitle {{
        color: #D9E8FF !important;

        font-size: 17px;

        max-width: 700px;

        margin-top: 12px;
        margin-bottom: 0;
    }}

    /* ---------------- SECTION ---------------- */

    .section-kicker {{
        color: #38BDF8;

        font-size: 12px;

        font-weight: 800;

        letter-spacing: 1.6px;

        text-transform: uppercase;

        margin-bottom: 5px;
    }}

    .section-title {{
        color: {TEXT};

        font-size: 27px;

        font-weight: 800;

        margin-bottom: 20px;
    }}

    /* ---------------- KPI ---------------- */

    .kpi-grid {{
        display: grid;

        grid-template-columns:
            repeat(4, 1fr);

        gap: 18px;

        margin: 20px 0 35px;
    }}

    .kpi {{
        position: relative;

        overflow: hidden;

        background: {CARD};

        border: 1px solid {BORDER};

        border-radius: 20px;

        padding: 22px;

        min-height: 135px;

        box-shadow:
            0 10px 35px rgba(15,23,42,0.07);
    }}

    .kpi::before {{
        content: "";

        position: absolute;

        left: 0;
        top: 0;

        width: 100%;
        height: 3px;

        background:
            linear-gradient(
                90deg,
                #2563EB,
                #06B6D4
            );
    }}

    .kpi-icon {{
        font-size: 23px;
        margin-bottom: 8px;
    }}

    .kpi-label {{
        color: {MUTED};

        font-size: 12px;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.8px;
    }}

    .kpi-value {{
        color: {TEXT};

        font-size: 29px;

        font-weight: 850;

        margin-top: 4px;
    }}

    .kpi-note {{
        color: {MUTED};

        font-size: 12px;

        margin-top: 5px;
    }}

    /* ---------------- CARDS ---------------- */

    .info-card {{
        background: {CARD};

        border: 1px solid {BORDER};

        border-radius: 20px;

        padding: 25px;

        height: 100%;

        box-shadow:
            0 10px 30px rgba(15,23,42,0.06);
    }}

    .info-icon {{
        font-size: 30px;

        margin-bottom: 13px;
    }}

    .info-title {{
        color: {TEXT};

        font-size: 18px;

        font-weight: 800;

        margin-bottom: 7px;
    }}

    .info-text {{
        color: {MUTED};

        line-height: 1.6;

        font-size: 14px;
    }}

    /* ---------------- PREDICTION RESULT ---------------- */

    .prediction-result {{
        position: relative;

        overflow: hidden;

        padding: 30px;

        border-radius: 24px;

        margin: 22px 0;

        background:
            linear-gradient(
                135deg,
                #0F3B82,
                #312E81,
                #075985
            );

        border: 1px solid rgba(96,165,250,0.30);

        box-shadow:
            0 20px 60px rgba(30,64,175,0.25);
    }}

    .prediction-label {{
        color: #BAE6FD;

        font-size: 12px;

        text-transform: uppercase;

        font-weight: 800;

        letter-spacing: 1.2px;
    }}

    .prediction-value {{
        color: white;

        font-size: 48px;

        font-weight: 900;

        margin: 5px 0;
    }}

    .prediction-unit {{
        color: #CBD5E1;

        font-size: 14px;
    }}

    .prediction-category {{
        display: inline-block;

        margin-top: 15px;

        padding: 8px 15px;

        border-radius: 999px;

        background: rgba(255,255,255,0.13);

        color: white;

        font-weight: 750;
    }}

    /* ---------------- FORM ---------------- */

    .form-card {{
        background: {CARD};

        border: 1px solid {BORDER};

        border-radius: 22px;

        padding: 25px;

        margin-bottom: 20px;

        box-shadow:
            0 10px 30px rgba(15,23,42,0.06);
    }}

    .form-title {{
        color: {TEXT};

        font-size: 19px;

        font-weight: 800;

        margin-bottom: 17px;
    }}

    /* ---------------- BUTTON ---------------- */

    .stButton > button {
    width: 100%;
    min-height: 52px;

    border-radius: 14px;

    border: 1px solid #38BDF8;

    padding: 14px 22px;

    font-size: 16px;
    font-weight: 850;

    color: #FFFFFF !important;

    background:
        linear-gradient(
            135deg,
            #1D4ED8 0%,
            #4338CA 50%,
            #0369A1 100%
        ) !important;

    box-shadow:
        0 8px 25px rgba(37,99,235,0.35);

    transition: all 0.2s ease;
}

.stButton > button:hover {
    color: #FFFFFF !important;

    background:
        linear-gradient(
            135deg,
            #1E40AF 0%,
            #3730A3 50%,
            #075985 100%
        ) !important;

    border: 1px solid #7DD3FC;

    transform: translateY(-2px);

    box-shadow:
        0 14px 35px rgba(37,99,235,0.50);
}

.stButton > button:focus {
    color: #FFFFFF !important;

    border: 2px solid #7DD3FC;

    box-shadow:
        0 0 0 4px rgba(56,189,248,0.20);
}
    /* ---------------- INPUTS ---------------- */

    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stSelectbox div[data-baseweb="select"] {{
        background: {INPUT_BG} !important;

        border-radius: 10px !important;

        border-color: {BORDER} !important;

        color: {TEXT} !important;
    }}

    /* ---------------- SIDEBAR BRAND ---------------- */

    .sidebar-brand {{
        padding: 18px 5px 25px;
    }}

    .sidebar-logo {{
        font-size: 32px;
    }}

    .sidebar-name {{
        font-size: 23px;

        font-weight: 900;

        color: white !important;

        margin-top: 4px;
    }}

    .sidebar-caption {{
        color: #94A3B8 !important;

        font-size: 12px;
    }}

    .status-card {{
        background: rgba(30,64,175,0.18);

        border: 1px solid rgba(96,165,250,0.22);

        border-radius: 14px;

        padding: 15px;

        margin-top: 15px;
    }}

    /* ---------------- FOOTER ---------------- */

    .footer {{
        text-align: center;

        color: {MUTED};

        font-size: 12px;

        padding: 35px 0 10px;
    }}

    /* ---------------- RESPONSIVE ---------------- */

    @media (max-width: 900px) {{

        .kpi-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}

        .hero-title {{
            font-size: 36px;
        }}

    }}

    @media (max-width: 600px) {{

        .kpi-grid {{
            grid-template-columns: 1fr;
        }}

        .hero {{
            padding: 30px 25px;
        }}

    }}

</style>
"""
)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    return joblib.load("sales_prediction_final_model.pkl")


try:

    model = load_model()

    model_loaded = True

except Exception as e:

    model = None
    model_loaded = False


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">

            <div class="sidebar-logo">📊</div>

            <div class="sidebar-name">
                SalesAI
            </div>

            <div class="sidebar-caption">
                Intelligent Sales Prediction
            </div>

        </div>
        """
    )

    st.markdown("### Navigation")

    page = st.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "🔮 Sales Prediction",
            "💡 Business Insights",
            "🤖 About Model",
            "🗄️ SQL Analysis",
            "📊 Power BI Dashboard"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    night = st.toggle(
        "🌙 Night Mode",
        value=st.session_state.night_mode
    )

    if night != st.session_state.night_mode:

        st.session_state.night_mode = night
        st.rerun()

    if model_loaded:

        st.html(
            """
            <div class="status-card">

                <div style="font-size:12px;color:#93C5FD;">
                    MODEL STATUS
                </div>

                <div style="
                    font-size:16px;
                    font-weight:800;
                    margin-top:5px;
                ">
                    🟢 Model Loaded
                </div>

                <div style="
                    font-size:12px;
                    color:#94A3B8;
                    margin-top:5px;
                ">
                    Gradient Boosting Regressor
                </div>

            </div>
            """
        )

    else:

        st.error("Model file not found.")

    st.markdown("")

    st.html(
        """
        <div style="
            padding:12px;
            color:#64748B;
            font-size:11px;
            line-height:1.5;
        ">
            SalesAI uses Machine Learning to
            predict sales and support
            business decisions.
        </div>
        """
    )


# =========================================================
# HERO
# =========================================================

st.html(
    """
    <div class="hero">

        <div class="hero-content">

            <div class="hero-badge">
                AI-POWERED SALES ANALYTICS PLATFORM
            </div>

            <div class="hero-title">
                SalesAI
            </div>

            <div class="hero-subtitle">
                Sales Prediction & Business Decision Support System
                powered by Machine Learning.
            </div>

        </div>

    </div>
    """
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.html(
        """
        <div class="section-kicker">
            OVERVIEW
        </div>

        <div class="section-title">
            Sales Intelligence Dashboard
        </div>
        """
    )

    st.html(
        """
        <div class="kpi-grid">

            <div class="kpi">
                <div class="kpi-icon">🎯</div>
                <div class="kpi-label">Model R²</div>
                <div class="kpi-value">94.96%</div>
                <div class="kpi-note">
                    Prediction performance
                </div>
            </div>

            <div class="kpi">
                <div class="kpi-icon">📉</div>
                <div class="kpi-label">MAE</div>
                <div class="kpi-value">150.10</div>
                <div class="kpi-note">
                    Mean Absolute Error
                </div>
            </div>

            <div class="kpi">
                <div class="kpi-icon">📐</div>
                <div class="kpi-label">RMSE</div>
                <div class="kpi-value">498.65</div>
                <div class="kpi-note">
                    Root Mean Square Error
                </div>
            </div>

            <div class="kpi">
                <div class="kpi-icon">🤖</div>
                <div class="kpi-label">Best Model</div>
                <div class="kpi-value">GBR</div>
                <div class="kpi-note">
                    Gradient Boosting
                </div>
            </div>

        </div>
        """
    )

    st.html(
        """
        <div class="section-kicker">
            PLATFORM
        </div>

        <div class="section-title">
            What can you do?
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">🔮</div>

                <div class="info-title">
                    Predict Sales
                </div>

                <div class="info-text">
                    Enter order, product and customer
                    information to generate an
                    AI-based sales prediction.
                </div>

            </div>
            """
        )

    with c2:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">💡</div>

                <div class="info-title">
                    Business Insights
                </div>

                <div class="info-text">
                    Understand products, regions,
                    states and monthly trends to
                    support business decisions.
                </div>

            </div>
            """
        )

    with c3:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">📊</div>

                <div class="info-title">
                    Power BI Analytics
                </div>

                <div class="info-text">
                    Explore the interactive Power BI
                    dashboard for deeper sales and
                    profitability analysis.
                </div>

            </div>
            """
        )


# =========================================================
# SALES PREDICTION
# =========================================================

elif page == "🔮 Sales Prediction":

    st.html(
        """
        <div class="section-kicker">
            MACHINE LEARNING
        </div>

        <div class="section-title">
            Sales Prediction
        </div>

        <p>
            Configure the order details below and let
            SalesAI estimate the expected sales value.
        </p>
        """
    )

    # -----------------------------------------------------
    # ORDER INFORMATION
    # -----------------------------------------------------

    st.html(
        """
        <div class="form-card">

            <div class="form-title">
                🧾 Step 1 — Order Information
            </div>

        </div>
        """
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        unit_price = st.number_input(
            "Unit Price",
            min_value=0.0,
            value=100.0,
            step=1.0
        )

    with c2:

        qty_ordered = st.number_input(
            "Quantity Ordered",
            min_value=1,
            value=10,
            step=1
        )

    with c3:

        discount = st.number_input(
            "Discount Offered",
            min_value=0.0,
            value=0.0,
            step=0.1
        )

    with c4:

        freight_expenses = st.number_input(
            "Freight Expenses",
            min_value=0.0,
            value=10.0,
            step=1.0
        )

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    st.html(
        """
        <div class="form-card">

            <div class="form-title">
                📅 Step 2 — Order Date
            </div>

        </div>
        """
    )

    order_date = st.date_input(
        "Order Date",
        value=date.today()
    )

    order_year = order_date.year
    order_month = order_date.month
    order_quarter = ((order_month - 1) // 3) + 1
    order_day = order_date.day
    order_dayofweek = order_date.weekday()

    st.caption(
        f"Year: {order_year}  •  "
        f"Month: {order_month}  •  "
        f"Quarter: Q{order_quarter}  •  "
        f"Day: {order_day}  •  "
        f"Day of Week: {order_dayofweek}"
    )

    # -----------------------------------------------------
    # PRODUCT INFORMATION
    # -----------------------------------------------------

    st.html(
        """
        <div class="form-card">

            <div class="form-title">
                🛒 Step 3 — Product & Customer Information
            </div>

        </div>
        """
    )

    c1, c2 = st.columns(2)

    with c1:

        order_priority = st.selectbox(
            "Order Priority",
            [
                "Critical",
                "High",
                "Medium",
                "Low"
            ]
        )

        freight_mode = st.selectbox(
            "Freight Mode",
            [
                "Delivery Truck",
                "Express Air",
                "Regular Air"
            ]
        )

        segment = st.selectbox(
            "Segment",
            [
                "Consumer",
                "Corporate",
                "Home Office"
            ]
        )

        product_type = st.selectbox(
            "Product Type",
            [
                "Office Supplies",
                "Technology",
                "Furniture"
            ]
        )

    with c2:

        product_sub_category = st.selectbox(
            "Product Sub-Category",
            [
                "Appliances",
                "Binders and Binder Accessories",
                "Bookcases",
                "Chairs & Chairmats",
                "Computer Peripherals",
                "Copiers and Fax",
                "Envelopes",
                "Labels",
                "Office Furnishings",
                "Paper",
                "Pens & Art Supplies",
                "Rubber Bands",
                "Scissors, Rulers and Trimmers",
                "Storage & Organization",
                "Tables"
            ]
        )

        product_container = st.selectbox(
            "Product Container",
            [
                "Small Box",
                "Medium Box",
                "Large Box",
                "Jumbo Box",
                "Small Pack",
                "Medium Pack",
                "Large Pack"
            ]
        )

        state = st.selectbox(
            "State",
            [
                "Andhra Pradesh",
                "Assam",
                "Bihar",
                "Delhi",
                "Goa",
                "Gujarat",
                "Haryana",
                "Himachal Pradesh",
                "Jammu and Kashmir",
                "Jharkhand",
                "Karnataka",
                "Kerala",
                "Madhya Pradesh",
                "Maharashtra",
                "Manipur",
                "Meghalaya",
                "Mizoram",
                "Nagaland",
                "Odisha",
                "Punjab",
                "Rajasthan",
                "Sikkim",
                "Tamil Nadu",
                "Telangana",
                "Tripura",
                "Uttar Pradesh",
                "Uttarakhand",
                "West Bengal"
            ]
        )

        region = st.selectbox(
            "Region",
            [
                "North",
                "South",
                "East",
                "West"
            ]
        )

    # -----------------------------------------------------
    # LIVE SUMMARY
    # -----------------------------------------------------

    st.html(
        """
        <div class="section-kicker">
            LIVE SUMMARY
        </div>

        <div class="section-title">
            Order Overview
        </div>
        """
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "Unit Price",
            f"{unit_price:,.2f}"
        )

    with s2:
        st.metric(
            "Quantity",
            f"{qty_ordered:,}"
        )

    with s3:
        st.metric(
            "Discount",
            f"{discount:,.2f}"
        )

    with s4:
        st.metric(
            "Freight",
            f"{freight_expenses:,.2f}"
        )

    st.markdown("")

    predict_button = st.button(
        "🚀 Generate Sales Prediction",
        use_container_width=True
    )

    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    if predict_button:

        if not model_loaded:

            st.error(
                "Model file not found. "
                "Please upload sales_prediction_final_model.pkl."
            )

        else:

            input_data = pd.DataFrame({

                "Unit Price": [unit_price],

                "QtyOrdered": [qty_ordered],

                "Discount offered": [discount],

                "Freight Expenses": [freight_expenses],

                "Order Year": [order_year],

                "Order Month": [order_month],

                "Order Quarter": [order_quarter],

                "Order Day": [order_day],

                "Order DayOfWeek": [order_dayofweek],

                "Order Priority": [order_priority],

                "Freight Mode": [freight_mode],

                "Segment": [segment],

                "Product Type": [product_type],

                "Product Sub-Category": [
                    product_sub_category
                ],

                "Product Container": [
                    product_container
                ],

                "State": [state],

                "Region": [region]

            })

            try:

                prediction = model.predict(
                    input_data
                )[0]

                st.session_state.last_prediction = prediction

            except Exception as e:

                st.error(
                    f"Prediction error: {e}"
                )

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    if st.session_state.last_prediction is not None:

        prediction = st.session_state.last_prediction

        if prediction < 500:

            category = "Low Sales"
            emoji = "📉"

        elif prediction < 2000:

            category = "Medium Sales"
            emoji = "📊"

        else:

            category = "High Sales"
            emoji = "🚀"

        st.html(
            f"""
            <div class="prediction-result">

                <div class="prediction-label">
                    AI PREDICTED SALES
                </div>

                <div class="prediction-value">
                    {prediction:,.2f}
                </div>

                <div class="prediction-unit">
                    Estimated sales value
                </div>

                <div class="prediction-category">
                    {emoji} {category}
                </div>

            </div>
            """
        )

        # Recommendation

        st.html(
            """
            <div class="form-card">

                <div class="form-title">
                    💡 AI Business Recommendation
                </div>

            </div>
            """
        )

        if category == "High Sales":

            st.success(
                "Strong sales potential detected. "
                "Consider maintaining inventory levels, "
                "prioritizing this order and monitoring "
                "customer demand."
            )

        elif category == "Medium Sales":

            st.info(
                "Moderate sales potential detected. "
                "Review pricing, discount strategy, "
                "product demand and regional performance."
            )

        else:

            st.warning(
                "Low sales potential detected. "
                "Consider reviewing pricing, product "
                "selection, discounts and market demand."
            )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

elif page == "💡 Business Insights":

    st.html(
        """
        <div class="section-kicker">
            BUSINESS INTELLIGENCE
        </div>

        <div class="section-title">
            Business Insights
        </div>

        <p>
            Key findings generated from the sales analysis.
        </p>
        """
    )

    c1, c2 = st.columns(2)

    with c1:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    🍍
                </div>

                <div class="info-title">
                    Top Sales Product
                </div>

                <div class="info-text">
                    Sliced Pineapple recorded the
                    highest total sales.
                </div>

            </div>
            """
        )

    with c2:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    🏆
                </div>

                <div class="info-title">
                    Highest Profit Product
                </div>

                <div class="info-text">
                    Quail Eggs recorded the highest
                    total profit.
                </div>

            </div>
            """
        )

    st.markdown("")

    c1, c2 = st.columns(2)

    with c1:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    🌎
                </div>

                <div class="info-title">
                    Strongest Region
                </div>

                <div class="info-text">
                    North region generated the
                    highest total sales and strong
                    profitability.
                </div>

            </div>
            """
        )

    with c2:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    📅
                </div>

                <div class="info-title">
                    Peak Month
                </div>

                <div class="info-text">
                    November recorded the highest
                    sales performance.
                </div>

            </div>
            """
        )

    st.markdown("")

    st.html(
        """
        <div class="section-kicker">
            ACTIONABLE RECOMMENDATIONS
        </div>

        <div class="section-title">
            What should the business do?
        </div>
        """
    )

    recommendations = [

        "Focus inventory planning on high-performing products.",

        "Review negative-profit products such as Jams and Tuna.",

        "Investigate Haryana's negative profitability.",

        "Use regional demand patterns for targeted sales strategies.",

        "Prepare additional inventory before November demand peaks.",

        "Use the ML prediction system to support order-level decisions."

    ]

    for item in recommendations:

        st.markdown(
            f"• **{item}**"
        )


# =========================================================
# ABOUT MODEL
# =========================================================

elif page == "🤖 About Model":

    st.html(
        """
        <div class="section-kicker">
            MACHINE LEARNING
        </div>

        <div class="section-title">
            Model Performance
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "R² Score",
            "94.96%"
        )

    with c2:

        st.metric(
            "MAE",
            "150.10"
        )

    with c3:

        st.metric(
            "RMSE",
            "498.65"
        )

    st.markdown("")

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">
                🤖
            </div>

            <div class="info-title">
                Gradient Boosting Regressor
            </div>

            <div class="info-text">
                The final SalesAI prediction system
                uses Gradient Boosting Regression.
                The model achieved an R² score of
                94.96%, making it the strongest
                performing model among the evaluated
                algorithms.
            </div>

        </div>
        """
    )

    st.markdown("")

    st.html(
        """
        <div class="section-kicker">
            MODEL COMPARISON
        </div>

        <div class="section-title">
            Algorithm Performance
        </div>
        """
    )

    comparison = pd.DataFrame({

        "Model": [
            "Gradient Boosting",
            "Random Forest",
            "Decision Tree",
            "Linear Regression"
        ],

        "MAE": [
            150.10,
            189.51,
            268.96,
            884.79
        ],

        "RMSE": [
            498.65,
            783.40,
            1241.98,
            1612.60
        ],

        "R²": [
            0.9496,
            0.8756,
            0.6874,
            0.4729
        ]

    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("")

    st.html(
        """
        <div class="section-kicker">
            FEATURES
        </div>

        <div class="section-title">
            Prediction Inputs
        </div>
        """
    )

    features = [

        "Unit Price",
        "QtyOrdered",
        "Discount offered",
        "Freight Expenses",
        "Order Year",
        "Order Month",
        "Order Quarter",
        "Order Day",
        "Order DayOfWeek",
        "Order Priority",
        "Freight Mode",
        "Segment",
        "Product Type",
        "Product Sub-Category",
        "Product Container",
        "State",
        "Region"

    ]

    feature_df = pd.DataFrame({
        "Feature": features
    })

    st.dataframe(
        feature_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# SQL ANALYSIS
# =========================================================

elif page == "🗄️ SQL Analysis":

    st.html(
        """
        <div class="section-kicker">
            DATABASE ANALYTICS
        </div>

        <div class="section-title">
            SQL Analysis
        </div>

        <p>
            Explore sales data stored in SQLite.
        </p>
        """
    )

    db_candidates = [
        "sales.db",
        "sales_database.db",
        "retail.db",
        "sales_ai.db"
    ]

    db_file = None

    for file in db_candidates:

        if os.path.exists(file):

            db_file = file
            break

    if db_file is None:

        st.warning(
            "SQLite database was not found in the "
            "current project folder."
        )

        st.info(
            "Upload your SQLite database file "
            "to enable SQL Analysis."
        )

    else:

        try:

            conn = sqlite3.connect(
                db_file
            )

            tables = pd.read_sql_query(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                """,
                conn
            )

            if len(tables) > 0:

                selected_table = st.selectbox(
                    "Select Table",
                    tables["name"].tolist()
                )

                query = f"""
                SELECT *
                FROM "{selected_table}"
                LIMIT 100
                """

                result = pd.read_sql_query(
                    query,
                    conn
                )

                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )

                st.caption(
                    f"Showing first 100 rows from "
                    f"`{selected_table}`"
                )

            else:

                st.warning(
                    "No tables found in database."
                )

            conn.close()

        except Exception as e:

            st.error(
                f"Database error: {e}"
            )


# =========================================================
# POWER BI
# =========================================================

elif page == "📊 Power BI Dashboard":

    st.html(
        """
        <div class="section-kicker">
            BUSINESS INTELLIGENCE
        </div>

        <div class="section-title">
            Power BI Dashboard
        </div>

        <p>
            Interactive sales analytics dashboard.
        </p>
        """
    )

    powerbi_url = (
        "https://app.powerbi.com/view?"
        "r=eyJrIjoiNzUwZDI1NjYtZjQ2Zi00M2FmLWE1MDQtYjFlNWQ3ODAwZTUx"
        "IiwidCI6IjcwMzY2YzAyLTkwOTUtNDMwOS04MDFhLTQ1MzUyOTUwYzg0MiJ9"
    )

    st.components.v1.iframe(
        powerbi_url,
        height=750,
        scrolling=True
    )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="footer">

        <strong>SalesAI</strong>
        <br>

        Sales Prediction & Business Decision Support System
        <br><br>

        Built with Python • Streamlit • Machine Learning • Power BI

    </div>
    """
)
