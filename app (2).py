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
# CUSTOM CSS
# =========================================================

st.html(
    f"""
<style>

html, body, [class*="css"] {{
    font-family: "Segoe UI", Arial, sans-serif;
}}

.stApp {{
    background: {BG};
    color: {TEXT};
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {{
    background: {CARD};
    border-right: 1px solid {BORDER};
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT};
}}


/* =====================================================
   HERO
   ===================================================== */

.hero {{
    background:
        linear-gradient(
            135deg,
            #0F172A 0%,
            #172554 45%,
            #075985 100%
        );

    border-radius: 24px;
    padding: 42px;
    margin-bottom: 28px;

    border: 1px solid #1E40AF;

    box-shadow:
        0 20px 50px rgba(15, 23, 42, 0.35);
}}

.hero-badge {{
    display: inline-block;

    padding: 7px 14px;

    border-radius: 30px;

    background: rgba(56, 189, 248, 0.12);

    border: 1px solid rgba(125, 211, 252, 0.35);

    color: #7DD3FC;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1.2px;

    margin-bottom: 15px;
}}

.hero-title {{
    font-size: 48px;

    font-weight: 900;

    color: #FFFFFF;

    margin-bottom: 8px;
}}

.hero-subtitle {{
    font-size: 18px;

    color: #CBD5E1;

    max-width: 800px;

    line-height: 1.6;
}}


/* =====================================================
   SECTION
   ===================================================== */

.section-kicker {{
    color: #38BDF8;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1.5px;

    margin-top: 28px;

    margin-bottom: 6px;
}}

.section-title {{
    font-size: 30px;

    font-weight: 850;

    color: {TEXT};

    margin-bottom: 8px;
}}


/* =====================================================
   KPI CARDS
   ===================================================== */

.kpi-card {{
    background: {CARD};

    border: 1px solid {BORDER};

    border-radius: 18px;

    padding: 22px;

    min-height: 130px;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.08);
}}

.kpi-label {{
    color: {MUTED};

    font-size: 13px;

    font-weight: 700;

    margin-bottom: 8px;
}}

.kpi-value {{
    color: {TEXT};

    font-size: 29px;

    font-weight: 900;
}}

.kpi-sub {{
    color: #38BDF8;

    font-size: 12px;

    margin-top: 6px;

    font-weight: 700;
}}


/* =====================================================
   INFO CARDS
   ===================================================== */

.info-card {{
    background: {CARD};

    border: 1px solid {BORDER};

    border-radius: 18px;

    padding: 24px;

    height: 100%;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.06);
}}

.info-icon {{
    font-size: 30px;

    margin-bottom: 10px;
}}

.info-title {{
    color: {TEXT};

    font-size: 19px;

    font-weight: 850;

    margin-bottom: 8px;
}}

.info-text {{
    color: {MUTED};

    font-size: 14px;

    line-height: 1.6;
}}


/* =====================================================
   BUTTON
   ===================================================== */

.stButton > button {{
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
        0 8px 25px rgba(37, 99, 235, 0.35);

    transition: all 0.2s ease;
}}

.stButton > button:hover {{
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
        0 14px 35px rgba(37, 99, 235, 0.50);
}}

.stButton > button:focus {{
    color: #FFFFFF !important;

    border: 2px solid #7DD3FC;

    box-shadow:
        0 0 0 4px rgba(56, 189, 248, 0.20);
}}


/* =====================================================
   INPUTS
   ===================================================== */

div[data-baseweb="input"],
div[data-baseweb="select"] {{
    border-radius: 10px;
}}

input {{
    color: {TEXT} !important;
}}

textarea {{
    color: {TEXT} !important;
}}


/* =====================================================
   DATAFRAME
   ===================================================== */

div[data-testid="stDataFrame"] {{
    border-radius: 14px;
    overflow: hidden;
}}


/* =====================================================
   ALERTS
   ===================================================== */

.stAlert {{
    border-radius: 14px;
}}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {{
    text-align: center;

    color: {MUTED};

    font-size: 13px;

    padding: 30px 0 10px;

    border-top: 1px solid {BORDER};

    margin-top: 45px;
}}

</style>
"""
)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    model_path = "sales_prediction_final_model.pkl"

    return joblib.load(model_path)


try:

    model = load_model()

    model_loaded = True

except Exception:

    model = None

    model_loaded = False


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:900;
            margin-bottom:4px;
        ">
        📊 SalesAI
        </div>

        <div style="
            color:#38BDF8;
            font-size:12px;
            font-weight:700;
            margin-bottom:25px;
        ">
        SALES INTELLIGENCE PLATFORM
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔮 Sales Prediction",
            "💡 Business Insights",
            "🤖 About Model",
            "🗄️ SQL Analysis",
            "📊 Power BI Dashboard"
        ]
    )

    st.divider()

    st.session_state.night_mode = st.toggle(
        "🌙 Night Mode",
        value=st.session_state.night_mode
    )

    st.divider()

    st.markdown("### 🤖 Model Status")

    if model_loaded:

        st.success("Model Loaded")

        st.caption(
            "Gradient Boosting Regressor"
        )

    else:

        st.error("Model Not Loaded")

        st.caption(
            "Check sales_prediction_final_model.pkl"
        )


# =========================================================
# HERO
# =========================================================

st.html(
    """
    <div class="hero">

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
    """
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.html(
        """
        <div class="section-kicker">
            EXECUTIVE OVERVIEW
        </div>

        <div class="section-title">
            Sales Intelligence Dashboard
        </div>
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.html(
            """
            <div class="kpi-card">

                <div class="kpi-label">
                    MODEL R²
                </div>

                <div class="kpi-value">
                    94.96%
                </div>

                <div class="kpi-sub">
                    Excellent Predictive Performance
                </div>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="kpi-card">

                <div class="kpi-label">
                    MAE
                </div>

                <div class="kpi-value">
                    150.10
                </div>

                <div class="kpi-sub">
                    Mean Absolute Error
                </div>

            </div>
            """
        )

    with col3:

        st.html(
            """
            <div class="kpi-card">

                <div class="kpi-label">
                    RMSE
                </div>

                <div class="kpi-value">
                    498.65
                </div>

                <div class="kpi-sub">
                    Root Mean Square Error
                </div>

            </div>
            """
        )

    with col4:

        st.html(
            """
            <div class="kpi-card">

                <div class="kpi-label">
                    BEST MODEL
                </div>

                <div class="kpi-value">
                    GBR
                </div>

                <div class="kpi-sub">
                    Gradient Boosting
                </div>

            </div>
            """
        )

    st.markdown("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    🔮
                </div>

                <div class="info-title">
                    Predict Sales
                </div>

                <div class="info-text">
                    Enter order and product information
                    to generate an AI-powered sales prediction.
                </div>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    💡
                </div>

                <div class="info-title">
                    Business Insights
                </div>

                <div class="info-text">
                    Explore product, region, profit and
                    seasonal business patterns.
                </div>

            </div>
            """
        )

    with col3:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    📊
                </div>

                <div class="info-title">
                    Power BI Analytics
                </div>

                <div class="info-text">
                    Explore interactive business dashboards
                    and visual analytics.
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
            🔮 Sales Prediction
        </div>

        <p>
            Enter order, product and customer information
            to estimate expected sales.
        </p>
        """
    )

    if not model_loaded:

        st.error(
            "Model could not be loaded. "
            "Please upload sales_prediction_final_model.pkl."
        )

    else:

        st.markdown("### 💰 Order Information")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            unit_price = st.number_input(
                "Unit Price",
                min_value=0.0,
                value=100.0,
                step=1.0
            )

        with col2:

            qty_ordered = st.number_input(
                "Quantity Ordered",
                min_value=1,
                value=5,
                step=1
            )

        with col3:

            discount = st.number_input(
                "Discount Offered",
                min_value=0.0,
                value=0.0,
                step=0.5
            )

        with col4:

            freight_expenses = st.number_input(
                "Freight Expenses",
                min_value=0.0,
                value=10.0,
                step=1.0
            )

        st.markdown("### 📅 Order Date")

        order_date = st.date_input(
            "Select Order Date",
            value=date.today()
        )

        order_year = order_date.year
        order_month = order_date.month

        if order_month in [1, 2, 3]:

            order_quarter = 1

        elif order_month in [4, 5, 6]:

            order_quarter = 2

        elif order_month in [7, 8, 9]:

            order_quarter = 3

        else:

            order_quarter = 4

        order_day = order_date.day

        order_dayofweek = order_date.weekday()

        st.markdown("### 📦 Order Details")

        col1, col2, col3 = st.columns(3)

        with col1:

            order_priority = st.selectbox(
                "Order Priority",
                [
                    "Critical",
                    "High",
                    "Medium",
                    "Low"
                ]
            )

        with col2:

            freight_mode = st.selectbox(
                "Freight Mode",
                [
                    "Delivery Truck",
                    "Express Air",
                    "Regular Air"
                ]
            )

        with col3:

            segment = st.selectbox(
                "Segment",
                [
                    "Consumer",
                    "Corporate",
                    "Home Office"
                ]
            )

        st.markdown("### 🛒 Product Information")

        col1, col2, col3 = st.columns(3)

        with col1:

            product_type = st.selectbox(
                "Product Type",
                [
                    "Office Supplies",
                    "Technology",
                    "Furniture"
                ]
            )

        with col2:

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

        with col3:

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

        st.markdown("### 📍 Location")

        col1, col2 = st.columns(2)

        with col1:

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

        with col2:

            region = st.selectbox(
                "Region",
                [
                    "North",
                    "South",
                    "East",
                    "West"
                ]
            )

        st.markdown("")

        predict_button = st.button(
            "🚀 Generate Sales Prediction",
            use_container_width=True
        )

        if predict_button:

            input_data = pd.DataFrame(
                {
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
                    "Product Sub-Category": [product_sub_category],
                    "Product Container": [product_container],
                    "State": [state],
                    "Region": [region]
                }
            )

            try:

                prediction = model.predict(input_data)[0]

                st.session_state.last_prediction = prediction

                st.success(
                    "Prediction generated successfully!"
                )

                st.markdown("### 🎯 Predicted Sales")

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Predicted Sales",
                        f"{prediction:,.2f}"
                    )

                if prediction < 500:

                    category = "Low Sales 📉"

                elif prediction < 2000:

                    category = "Medium Sales 📊"

                else:

                    category = "High Sales 🚀"

                with col2:

                    st.metric(
                        "Sales Category",
                        category
                    )

                with col3:

                    st.metric(
                        "Model",
                        "Gradient Boosting"
                    )

                st.markdown("### 💡 Recommendation")

                if prediction < 500:

                    st.warning(
                        "Expected sales are relatively low. "
                        "Consider improving pricing, promotion, "
                        "product positioning or order quantity."
                    )

                elif prediction < 2000:

                    st.info(
                        "Expected sales are moderate. "
                        "Maintain competitive pricing and "
                        "optimize inventory availability."
                    )

                else:

                    st.success(
                        "Expected sales are high. "
                        "Ensure sufficient inventory, "
                        "logistics capacity and customer support."
                    )

                with st.expander("🔎 View Input Data"):

                    st.dataframe(
                        input_data,
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    f"Prediction failed: {e}"
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
            💡 Business Insights
        </div>

        <p>
            Key findings and recommendations from the sales dataset.
        </p>
        """
    )

    col1, col2 = st.columns(2)

    with col1:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    🍍
                </div>

                <div class="info-title">
                    Highest Sales Product
                </div>

                <div class="info-text">
                    Sliced Pineapple recorded the highest
                    total sales in the analyzed dataset.
                </div>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    💰
                </div>

                <div class="info-title">
                    Highest Profit Product
                </div>

                <div class="info-text">
                    Quail Eggs generated the highest
                    total profit among analyzed products.
                </div>

            </div>
            """
        )

    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    🗺️
                </div>

                <div class="info-title">
                    Strongest Region
                </div>

                <div class="info-text">
                    The North region showed strong overall
                    sales performance.
                </div>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">
                    📅
                </div>

                <div class="info-title">
                    Peak Sales Month
                </div>

                <div class="info-text">
                    November was identified as the strongest
                    sales month in the analysis.
                </div>

            </div>
            """
        )

    st.markdown("### 📌 Business Recommendations")

    recommendations = [
        "Focus inventory planning on high-performing products.",
        "Monitor products with negative or low profitability.",
        "Analyze Haryana profitability carefully.",
        "Use regional sales patterns for targeted strategies.",
        "Prepare additional inventory before November.",
        "Use ML-based sales prediction to support inventory and planning decisions."
    ]

    for recommendation in recommendations:

        st.write(
            f"• {recommendation}"
        )


# =========================================================
# ABOUT MODEL
# =========================================================

elif page == "🤖 About Model":

    st.html(
        """
        <div class="section-kicker">
            MACHINE LEARNING MODEL
        </div>

        <div class="section-title">
            🤖 About SalesAI Model
        </div>

        <p>
            SalesAI uses a Gradient Boosting Regressor
            to predict sales based on historical order,
            product and geographical information.
        </p>
        """
    )

    st.markdown("### 📈 Model Performance")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "R² Score",
            "94.96%"
        )

    with col2:

        st.metric(
            "MAE",
            "150.10"
        )

    with col3:

        st.metric(
            "RMSE",
            "498.65"
        )

    st.markdown("### 🏆 Selected Model")

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">
                🚀
            </div>

            <div class="info-title">
                Gradient Boosting Regressor
            </div>

            <div class="info-text">
                Gradient Boosting achieved the best
                predictive performance among the tested
                regression algorithms.
            </div>

        </div>
        """
    )

    st.markdown("### 📊 Model Comparison")

    comparison_df = pd.DataFrame(
        {
            "Model": [
                "Linear Regression",
                "Decision Tree",
                "Random Forest",
                "Gradient Boosting"
            ],
            "MAE": [
                884.79,
                268.96,
                189.51,
                150.10
            ],
            "RMSE": [
                1612.60,
                1241.98,
                783.40,
                498.65
            ],
            "R² Score": [
                0.4729,
                0.6874,
                0.8756,
                0.9496
            ]
        }
    )

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # ACTUAL FEATURE IMPORTANCE
    # =====================================================

    st.html(
        """
        <div class="section-kicker">
            MODEL EXPLAINABILITY
        </div>

        <div class="section-title">
            Feature Importance
        </div>

        <p>
            The chart below shows the relative importance
            of features used by the trained Gradient Boosting
            model.
        </p>
        """
    )

    try:

        estimator = model.named_steps["model"]

        preprocessor = model.named_steps["preprocessor"]

        feature_names = (
            preprocessor
            .get_feature_names_out()
        )

        importance_values = (
            estimator.feature_importances_
        )

        feature_importance = pd.DataFrame(
            {
                "Feature": feature_names,
                "Importance": importance_values
            }
        )

        feature_importance["Feature"] = (
            feature_importance["Feature"]
            .str.replace(
                "num__",
                "",
                regex=False
            )
            .str.replace(
                "cat__",
                "",
                regex=False
            )
        )

        feature_importance = (
            feature_importance
            .sort_values(
                "Importance",
                ascending=False
            )
            .head(15)
            .reset_index(drop=True)
        )

        chart_data = (
            feature_importance
            .set_index("Feature")
        )

        st.bar_chart(
            chart_data,
            y="Importance",
            horizontal=True,
            height=600
        )

        st.caption(
            "Top 15 features ranked by their contribution "
            "to the Gradient Boosting model."
        )

        with st.expander("📋 View Feature Importance Values"):

            st.dataframe(
                feature_importance,
                use_container_width=True,
                hide_index=True
            )

    except Exception as e:

        st.warning(
            f"Feature importance could not be loaded: {e}"
        )


    # =====================================================
    # PREDICTION INPUTS
    # =====================================================

    st.markdown("### 🧾 Prediction Inputs")

    prediction_inputs = pd.DataFrame(
        {
            "Feature": [
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
            ],
            "Type": [
                "Numerical",
                "Numerical",
                "Numerical",
                "Numerical",
                "Numerical",
                "Numerical",
                "Numerical",
                "Numerical",
                "Numerical",
                "Categorical",
                "Categorical",
                "Categorical",
                "Categorical",
                "Categorical",
                "Categorical",
                "Categorical",
                "Categorical"
            ]
        }
    )

    st.dataframe(
        prediction_inputs,
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
            🗄️ SQL Analysis
        </div>

        <p>
            Explore sales data stored in the SQLite database.
        </p>
        """
    )

    possible_databases = [
        "sales.db",
        "sales_database.db",
        "retail.db",
        "sales_ai.db"
    ]

    existing_database = None

    for database in possible_databases:

        if os.path.exists(database):

            existing_database = database
            break

    if existing_database is None:

        st.warning(
            "No SQLite database found. "
            "Upload your database file to the repository."
        )

    else:

        st.success(
            f"Database found: {existing_database}"
        )

        try:

            conn = sqlite3.connect(
                existing_database
            )

            tables = pd.read_sql_query(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                ORDER BY name
                """,
                conn
            )

            if tables.empty:

                st.warning(
                    "No tables found in the database."
                )

            else:

                table_names = tables["name"].tolist()

                selected_table = st.selectbox(
                    "Select Table",
                    table_names
                )

                query = (
                    f'SELECT * FROM "{selected_table}" LIMIT 100'
                )

                data = pd.read_sql_query(
                    query,
                    conn
                )

                st.markdown(
                    f"### 📋 {selected_table}"
                )

                st.dataframe(
                    data,
                    use_container_width=True,
                    hide_index=True
                )

                st.caption(
                    f"Showing first {len(data)} rows."
                )

            conn.close()

        except Exception as e:

            st.error(
                f"Database error: {e}"
            )


# =========================================================
# POWER BI DASHBOARD
# =========================================================

elif page == "📊 Power BI Dashboard":

    st.html(
        """
        <div class="section-kicker">
            BUSINESS VISUALIZATION
        </div>

        <div class="section-title">
            📊 Power BI Dashboard
        </div>

        <p>
            Interactive Power BI dashboard for sales
            and business performance analysis.
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
        — AI-Powered Sales Prediction & Business Decision Support System

        <br><br>

        Built with Python • Streamlit • Machine Learning • SQL • Power BI

    </div>
    """
)
