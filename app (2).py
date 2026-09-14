import streamlit as st

import streamlit as st
import sqlite3
import pandas as pd
import joblib
from datetime import date

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SalesAI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    return joblib.load("sales_prediction_final_model.pkl")

model = load_model()

# =========================================================
# SESSION STATE
# =========================================================

if "night_mode" not in st.session_state:
    st.session_state.night_mode = False

# =========================================================
# THEME
# =========================================================

if st.session_state.night_mode:

    BG = "#0b1020"
    CARD = "#111827"
    CARD2 = "#172033"
    TEXT = "#f8fafc"
    MUTED = "#94a3b8"
    BORDER = "#263449"
    HERO_TEXT = "#ffffff"
    INPUT_BG = "#111827"

else:

    BG = "#f4f7fb"
    CARD = "#ffffff"
    CARD2 = "#f8fafc"
    TEXT = "#172033"
    MUTED = "#64748b"
    BORDER = "#e2e8f0"
    HERO_TEXT = "#ffffff"
    INPUT_BG = "#ffffff"


# =========================================================
# GLOBAL CSS
# =========================================================

st.html(f"""
<style>

.stApp {{
    background: {BG};
}}

section[data-testid="stSidebar"] {{
    background: {CARD};
    border-right: 1px solid {BORDER};
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT};
}}

.stButton > button {{
    border-radius: 12px;
    border: none;
    font-weight: 700;
    min-height: 46px;
    transition: all 0.2s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
}}

div[data-testid="stMetric"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 18px;
}}

h1, h2, h3, h4, p, label {{
    color: {TEXT};
}}

</style>
""")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.html(f"""
    <div style="
        padding:8px 4px 20px 4px;
        border-bottom:1px solid {BORDER};
        margin-bottom:20px;
    ">
        <div style="
            font-size:26px;
            font-weight:800;
            color:{TEXT};
        ">
            📊 SalesAI
        </div>

        <div style="
            font-size:12px;
            color:{MUTED};
            margin-top:6px;
            line-height:1.5;
        ">
            Sales Prediction & Business Decision Support
        </div>
    </div>
    """)

    st.markdown("### 🧭 Navigation")

    page = st.radio(
        "Navigation",
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

    st.markdown("---")

    st.markdown("### 🎨 Appearance")

    night = st.toggle(
        "🌙 Night Mode",
        value=st.session_state.night_mode
    )

    if night != st.session_state.night_mode:
        st.session_state.night_mode = night
        st.rerun()

    st.markdown("---")

    st.markdown("### 🟢 Model Status")

    st.success("Model Loaded")

    st.caption("Gradient Boosting Regressor")

    st.metric(
        "Model R²",
        "94.96%"
    )


# =========================================================
# HERO
# =========================================================

st.html(f"""
<div style="
    background:linear-gradient(135deg,#2563eb 0%,#7c3aed 50%,#0891b2 100%);
    border-radius:24px;
    padding:42px;
    margin-bottom:25px;
    box-shadow:0 18px 45px rgba(37,99,235,0.25);
    color:white;
">

    <div style="
        font-size:42px;
        font-weight:900;
        color:white;
        margin-bottom:8px;
    ">
        📊 SalesAI
    </div>

    <div style="
        font-size:20px;
        font-weight:600;
        color:white;
        margin-bottom:18px;
    ">
        Intelligent Sales Prediction & Business Decision Support
    </div>

    <div style="
        display:inline-block;
        padding:8px 16px;
        border-radius:30px;
        background:rgba(255,255,255,0.18);
        border:1px solid rgba(255,255,255,0.25);
        font-size:14px;
        color:white;
    ">
        🤖 Machine Learning &nbsp; • &nbsp;
        📈 Business Analytics &nbsp; • &nbsp;
        🔮 Sales Prediction
    </div>

</div>
""")


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.html(f"""
    <div style="
        background:{CARD};
        border:1px solid {BORDER};
        border-radius:18px;
        padding:25px;
        margin-bottom:20px;
    ">

        <div style="
            font-size:25px;
            font-weight:800;
            color:{TEXT};
        ">
            👋 Welcome to SalesAI
        </div>

        <div style="
            color:{MUTED};
            font-size:15px;
            margin-top:8px;
        ">
            Analyze sales information, predict expected sales,
            and generate business-oriented insights.
        </div>

    </div>
    """)

    # KPI CARDS

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:22px;
            min-height:130px;
        ">
            <div style="font-size:28px;">🎯</div>
            <div style="color:{MUTED};font-size:13px;margin-top:8px;">
                Problem Type
            </div>
            <div style="
                color:{TEXT};
                font-size:21px;
                font-weight:800;
                margin-top:5px;
            ">
                Regression
            </div>
        </div>
        """)

    with c2:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:22px;
            min-height:130px;
        ">
            <div style="font-size:28px;">🧠</div>
            <div style="color:{MUTED};font-size:13px;margin-top:8px;">
                ML Algorithm
            </div>
            <div style="
                color:{TEXT};
                font-size:21px;
                font-weight:800;
                margin-top:5px;
            ">
                Gradient Boosting
            </div>
        </div>
        """)

    with c3:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:22px;
            min-height:130px;
        ">
            <div style="font-size:28px;">📈</div>
            <div style="color:{MUTED};font-size:13px;margin-top:8px;">
                Model Performance
            </div>
            <div style="
                color:{TEXT};
                font-size:21px;
                font-weight:800;
                margin-top:5px;
            ">
                R² = 94.96%
            </div>
        </div>
        """)

    with c4:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:22px;
            min-height:130px;
        ">
            <div style="font-size:28px;">🇮🇳</div>
            <div style="color:{MUTED};font-size:13px;margin-top:8px;">
                Market
            </div>
            <div style="
                color:{TEXT};
                font-size:21px;
                font-weight:800;
                margin-top:5px;
            ">
                India
            </div>
        </div>
        """)

    st.markdown("")

    st.subheader("🚀 What can you do?")

    a, b, c = st.columns(3)

    with a:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:25px;
            min-height:180px;
        ">
            <div style="font-size:35px;">🔮</div>
            <h3 style="color:{TEXT};margin-bottom:8px;">
                Predict Sales
            </h3>
            <p style="color:{MUTED};line-height:1.6;">
                Enter order, product and regional information
                to estimate expected sales.
            </p>
        </div>
        """)

    with b:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:25px;
            min-height:180px;
        ">
            <div style="font-size:35px;">📊</div>
            <h3 style="color:{TEXT};margin-bottom:8px;">
                Analyze Business
            </h3>
            <p style="color:{MUTED};line-height:1.6;">
                Understand product, segment, regional and
                seasonal sales performance.
            </p>
        </div>
        """)

    with c:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:25px;
            min-height:180px;
        ">
            <div style="font-size:35px;">💡</div>
            <h3 style="color:{TEXT};margin-bottom:8px;">
                Make Decisions
            </h3>
            <p style="color:{MUTED};line-height:1.6;">
                Use predictions and business insights to
                support inventory and sales planning.
            </p>
        </div>
        """)


# =========================================================
# SALES PREDICTION
# =========================================================

elif page == "🔮 Sales Prediction":

    st.html(f"""
    <div style="
        background:{CARD};
        border:1px solid {BORDER};
        border-radius:18px;
        padding:25px;
        margin-bottom:20px;
    ">
        <div style="
            font-size:25px;
            font-weight:800;
            color:{TEXT};
        ">
            🔮 Sales Prediction
        </div>

        <div style="
            color:{MUTED};
            margin-top:7px;
        ">
            Enter order and product information to predict expected sales.
        </div>
    </div>
    """)

    # -----------------------------------------------------
    # ORDER INFORMATION
    # -----------------------------------------------------

    st.subheader("🛒 Order Information")

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

    st.subheader("📅 Order Date")

    order_date = st.date_input(
        "Select Order Date",
        value=date(2013, 11, 15),
        min_value=date(2000, 1, 1),
        max_value=date(2030, 12, 31)
    )

    order_year = order_date.year
    order_month = order_date.month
    order_day = order_date.day

    order_quarter = ((order_month - 1) // 3) + 1

    order_dayofweek = order_date.weekday()

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.metric("Year", order_year)

    with d2:
        st.metric("Month", order_month)

    with d3:
        st.metric("Quarter", f"Q{order_quarter}")

    with d4:
        st.metric("Day of Week", order_dayofweek)

    # -----------------------------------------------------
    # PRODUCT INFORMATION
    # -----------------------------------------------------

    st.subheader("📦 Product & Customer Information")

    c1, c2, c3 = st.columns(3)

    with c1:

        order_priority = st.selectbox(
            "Order Priority",
            [
                "High",
                "Low",
                "Not Specified",
                "Medium",
                "Critical"
            ]
        )

        freight_mode = st.selectbox(
            "Freight Mode",
            [
                "Regular Air",
                "Delivery Truck",
                "Express Air"
            ]
        )

        segment = st.selectbox(
            "Segment",
            [
                "Hotels / Hospitals",
                "Restaurant Chain",
                "Personel Usage",
                "Stand Alone Restaurants"
            ]
        )

    with c2:

        product_type = st.selectbox(
            "Product Type",
            [
                "Processed Meat",
                "Canned Foods",
                "Preserved Food"
            ]
        )

        product_sub_category = st.selectbox(
            "Product Sub-Category",
            [
                "Smoked Salmon",
                "Quail Eggs",
                "Bacon",
                "Marmalade",
                "Assorted Fruits",
                "Foie Gras",
                "Fresh Water Eel",
                "Sliced Pineapple",
                "Jams",
                "Jelly Fish",
                "Sundried Tomatoes",
                "Wild Berry",
                "Pickle",
                "Caviar",
                "Pacific Squid",
                "Oysters (Clam)",
                "Tuna"
            ]
        )

    with c3:

        product_container = st.selectbox(
            "Product Container",
            [
                "Small Box",
                "Wrap Bag",
                "Small Pack",
                "Jumbo Drum",
                "Jumbo Box",
                "Medium Box",
                "Large Box"
            ]
        )

        state = st.selectbox(
            "State",
            [
                "Uttar Pradesh",
                "Madhya Pradesh",
                "Bihar",
                "Tamil Nadu",
                "Maharashtra",
                "West Bengal",
                "Andhra Pradesh",
                "Gujarat",
                "Rajasthan",
                "Jharkhand",
                "Karnataka",
                "Haryana",
                "Telangana",
                "Assam",
                "Kerala"
            ]
        )

        region = st.selectbox(
            "Region",
            [
                "North",
                "West",
                "South",
                "East"
            ]
        )

    # -----------------------------------------------------
    # LIVE SUMMARY
    # -----------------------------------------------------

    st.html(f"""
    <div style="
        background:{CARD2};
        border:1px solid {BORDER};
        border-radius:18px;
        padding:22px;
        margin-top:20px;
        margin-bottom:20px;
    ">

        <div style="
            font-size:19px;
            font-weight:800;
            color:{TEXT};
            margin-bottom:15px;
        ">
            ⚡ Live Prediction Summary
        </div>

        <div style="
            display:flex;
            justify-content:space-between;
            flex-wrap:wrap;
            gap:15px;
        ">

            <div>
                <div style="color:{MUTED};font-size:12px;">
                    Unit Price
                </div>
                <div style="color:{TEXT};font-size:18px;font-weight:700;">
                    ₹{unit_price:,.2f}
                </div>
            </div>

            <div>
                <div style="color:{MUTED};font-size:12px;">
                    Quantity
                </div>
                <div style="color:{TEXT};font-size:18px;font-weight:700;">
                    {qty_ordered}
                </div>
            </div>

            <div>
                <div style="color:{MUTED};font-size:12px;">
                    Discount
                </div>
                <div style="color:{TEXT};font-size:18px;font-weight:700;">
                    {discount:.1f}%
                </div>
            </div>

            <div>
                <div style="color:{MUTED};font-size:12px;">
                    Region
                </div>
                <div style="color:{TEXT};font-size:18px;font-weight:700;">
                    {region}
                </div>
            </div>

        </div>
    </div>
    """)

    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    st.subheader("🚀 Generate Prediction")

    if st.button(
        "🔮 Predict Expected Sales",
        use_container_width=True,
        type="primary"
    ):

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

            "Product Sub-Category": [product_sub_category],

            "Product Container": [product_container],

            "State": [state],

            "Region": [region]
        })

        prediction = model.predict(input_data)[0]

        if prediction < 500:
            category = "Low Sales"
            emoji = "🔵"
        elif prediction < 2000:
            category = "Medium Sales"
            emoji = "🟡"
        else:
            category = "High Sales"
            emoji = "🟢"

        st.html(f"""
        <div style="
            background:linear-gradient(135deg,#2563eb,#7c3aed);
            border-radius:22px;
            padding:35px;
            margin-top:25px;
            text-align:center;
            color:white;
            box-shadow:0 15px 40px rgba(37,99,235,0.25);
        ">

            <div style="
                font-size:18px;
                color:white;
                opacity:0.9;
            ">
                💰 Predicted Sales
            </div>

            <div style="
                font-size:48px;
                font-weight:900;
                color:white;
                margin:8px 0;
            ">
                ₹{prediction:,.2f}
            </div>

            <div style="
                font-size:18px;
                color:white;
            ">
                {emoji} {category}
            </div>

        </div>
        """)

        # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------

        st.subheader("💡 Business Recommendation")

        if prediction >= 2000:

            st.success(
                "High expected sales. Consider maintaining sufficient inventory "
                "and preparing distribution capacity."
            )

        elif prediction >= 500:

            st.info(
                "Medium expected sales. Monitor demand and maintain balanced "
                "inventory levels."
            )

        else:

            st.warning(
                "Low expected sales. Review pricing, demand and promotional "
                "strategy before increasing inventory."
            )

        with st.expander("🔎 View Prediction Input Data"):

            st.dataframe(
                input_data,
                use_container_width=True
            )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

elif page == "💡 Business Insights":

    st.html(f"""
    <div style="
        background:{CARD};
        border:1px solid {BORDER};
        border-radius:18px;
        padding:25px;
        margin-bottom:20px;
    ">

        <div style="
            font-size:25px;
            font-weight:800;
            color:{TEXT};
        ">
            💡 Business Insights
        </div>

        <div style="
            color:{MUTED};
            margin-top:7px;
        ">
            Key findings obtained from the sales analysis.
        </div>

    </div>
    """)

    # PRODUCT

    st.subheader("📦 Product Strategy")

    c1, c2 = st.columns(2)

    with c1:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:25px;
        ">
            <div style="font-size:32px;">🏆</div>
            <div style="
                color:{TEXT};
                font-size:20px;
                font-weight:800;
                margin-top:8px;
            ">
                Sliced Pineapple
            </div>
            <div style="
                color:{MUTED};
                margin-top:8px;
                line-height:1.6;
            ">
                Highest total sales among product sub-categories.
                Maintain sufficient inventory and strengthen marketing.
            </div>
        </div>
        """)

    with c2:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:25px;
        ">
            <div style="font-size:32px;">⚠️</div>
            <div style="
                color:{TEXT};
                font-size:20px;
                font-weight:800;
                margin-top:8px;
            ">
                Jams & Tuna
            </div>
            <div style="
                color:{MUTED};
                margin-top:8px;
                line-height:1.6;
            ">
                Negative total profit. Review pricing, discounts
                and procurement costs.
            </div>
        </div>
        """)

    st.markdown("")

    # REGION

    st.subheader("🌍 Regional Strategy")

    c1, c2 = st.columns(2)

    with c1:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:25px;
        ">
            <div style="font-size:32px;">🥇</div>
            <div style="
                color:{TEXT};
                font-size:20px;
                font-weight:800;
            ">
                North Region
            </div>
            <div style="
                color:{MUTED};
                margin-top:8px;
            ">
                Highest total sales and total profit.
                Prioritize inventory, distribution and marketing.
            </div>
        </div>
        """)

    with c2:
        st.html(f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:18px;
            padding:25px;
        ">
            <div style="font-size:32px;">📍</div>
            <div style="
                color:{TEXT};
                font-size:20px;
                font-weight:800;
            ">
                Haryana
            </div>
            <div style="
                color:{MUTED};
                margin-top:8px;
            ">
                Negative total profit. Investigate pricing,
                discounts and logistics costs.
            </div>
        </div>
        """)

    st.markdown("")

    # SEGMENT

    st.subheader("👥 Segment Strategy")

    st.html(f"""
    <div style="
        background:{CARD};
        border:1px solid {BORDER};
        border-radius:18px;
        padding:25px;
    ">

        <div style="font-size:32px;">🏢</div>

        <div style="
            color:{TEXT};
            font-size:20px;
            font-weight:800;
            margin-top:8px;
        ">
            Stand Alone Restaurants
        </div>

        <div style="
            color:{MUTED};
            margin-top:8px;
            line-height:1.6;
        ">
            This segment generated the highest total profit and
            highest average profit. It can be a priority segment
            for profitable customer-focused strategies.
        </div>

    </div>
    """)

    st.markdown("")

    # SEASONAL

    st.subheader("📅 Seasonal Strategy")

    st.html(f"""
    <div style="
        background:linear-gradient(135deg,#f97316,#ec4899);
        border-radius:18px;
        padding:28px;
        color:white;
    ">

        <div style="font-size:34px;">🔥</div>

        <div style="
            color:white;
            font-size:24px;
            font-weight:800;
        ">
            November Peak
        </div>

        <div style="
            color:white;
            margin-top:8px;
            line-height:1.6;
        ">
            November recorded the highest total sales.
            Increase inventory and promotional planning before
            the peak period.
        </div>

    </div>
    """)
   

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.markdown("### 🎯 Business Recommendations")

    recommendations = [
        "🍍 Maintain sufficient inventory for high-sales products such as Sliced Pineapple.",
        "💰 Review pricing, discounts and procurement costs for low-profit products.",
        "🏆 Focus on profitable customer segments such as Stand Alone Restaurants.",
        "🗺️ Prioritize inventory and distribution planning in the North region.",
        "⚠️ Investigate pricing, discount and logistics factors affecting Haryana profitability.",
        "📅 Prepare inventory and promotional planning before the November sales peak.",
        "🤖 Use ML sales predictions to support inventory and future sales planning."
    ]

    for item in recommendations:

        st.write(item)

# =========================================================
# SQL ANALYSIS
# =========================================================

elif page == "🗄️ SQL Analysis":

    st.html(f"""
    <div style="
        background:{CARD};
        border:1px solid {BORDER};
        border-radius:18px;
        padding:25px;
        margin-bottom:20px;
    ">
        <div style="
            font-size:25px;
            font-weight:800;
            color:{TEXT};
        ">
            🗄️ SQL Analysis
        </div>

        <div style="
            color:{MUTED};
            margin-top:7px;
        ">
            Business analysis performed using SQLite and SQL queries.
        </div>
    </div>
    """)

    # -----------------------------------------------------
    # DATABASE CONNECTION
    # -----------------------------------------------------

    @st.cache_resource
    def get_connection():
        return sqlite3.connect("retail.db", check_same_thread=False)

    conn = get_connection()


    # -----------------------------------------------------
    # KPI ANALYSIS
    # -----------------------------------------------------

    st.subheader("📊 SQL Business KPIs")

    kpi_query = """
    SELECT
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        COUNT(*) AS Total_Orders,
        ROUND(AVG(Sales), 2) AS Average_Order_Value,
        ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin
    FROM retail
    """

    kpi = pd.read_sql_query(kpi_query, conn)

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Total Sales",
            f"₹{kpi.loc[0, 'Total_Sales']:,.2f}"
        )

    with c2:
        st.metric(
            "Total Profit",
            f"₹{kpi.loc[0, 'Total_Profit']:,.2f}"
        )

    with c3:
        st.metric(
            "Total Orders",
            f"{int(kpi.loc[0, 'Total_Orders']):,}"
        )

    with c4:
        st.metric(
            "Average Order Value",
            f"₹{kpi.loc[0, 'Average_Order_Value']:,.2f}"
        )

    with c5:
        st.metric(
            "Profit Margin",
            f"{kpi.loc[0, 'Profit_Margin']:.2f}%"
        )

    st.markdown("")

    # -----------------------------------------------------
    # PRODUCT TYPE
    # -----------------------------------------------------

    st.subheader("📦 Product Type Analysis")

    product_type_query = """
    SELECT
        [Product Type],
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        COUNT(*) AS Total_Orders,
        ROUND(
            (SUM(Profit) / SUM(Sales)) * 100,
            2
        ) AS Profit_Margin
    FROM retail
    GROUP BY [Product Type]
    ORDER BY Total_Sales DESC
    """

    product_type_sql = pd.read_sql_query(
        product_type_query,
        conn
    )

    st.dataframe(
        product_type_sql,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # SUB-CATEGORY
    # -----------------------------------------------------

    st.subheader("🏷️ Product Sub-Category Analysis")

    subcategory_query = """
    SELECT
        [Product Sub-Category],
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        COUNT(*) AS Total_Orders,
        ROUND(
            (SUM(Profit) / SUM(Sales)) * 100,
            2
        ) AS Profit_Margin
    FROM retail
    GROUP BY [Product Sub-Category]
    ORDER BY Total_Sales DESC
    """

    subcategory_sql = pd.read_sql_query(
        subcategory_query,
        conn
    )

    st.dataframe(
        subcategory_sql,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # REGION
    # -----------------------------------------------------

    st.subheader("🌍 Region Analysis")

    region_query = """
    SELECT
        Region,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        COUNT(*) AS Total_Orders,
        ROUND(
            (SUM(Profit) / SUM(Sales)) * 100,
            2
        ) AS Profit_Margin
    FROM retail
    GROUP BY Region
    ORDER BY Total_Sales DESC
    """

    region_sql = pd.read_sql_query(
        region_query,
        conn
    )

    st.dataframe(
        region_sql,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # STATE
    # -----------------------------------------------------

    st.subheader("📍 State Analysis")

    state_query = """
    SELECT
        State,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        COUNT(*) AS Total_Orders,
        ROUND(
            (SUM(Profit) / SUM(Sales)) * 100,
            2
        ) AS Profit_Margin
    FROM retail
    GROUP BY State
    ORDER BY Total_Sales DESC
    """

    state_sql = pd.read_sql_query(
        state_query,
        conn
    )

    st.dataframe(
        state_sql,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # SEGMENT
    # -----------------------------------------------------

    st.subheader("👥 Customer Segment Analysis")

    segment_query = """
    SELECT
        Segment,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        COUNT(*) AS Total_Orders,
        ROUND(
            (SUM(Profit) / SUM(Sales)) * 100,
            2
        ) AS Profit_Margin
    FROM retail
    GROUP BY Segment
    ORDER BY Total_Sales DESC
    """

    segment_sql = pd.read_sql_query(
        segment_query,
        conn
    )

    st.dataframe(
        segment_sql,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # MONTHLY SALES
    # -----------------------------------------------------

    st.subheader("📅 Monthly Sales Analysis")

    monthly_query = """
    SELECT
        strftime('%Y-%m', [Order Date]) AS Month,
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        COUNT(*) AS Total_Orders
    FROM retail
    GROUP BY Month
    ORDER BY Month
    """

    monthly_sql = pd.read_sql_query(
        monthly_query,
        conn
    )

    st.dataframe(
        monthly_sql,
        use_container_width=True,
        hide_index=True
    )

    st.line_chart(
        monthly_sql.set_index("Month")["Total_Sales"]
    )

    # -----------------------------------------------------
    # TOP 10 PRODUCTS
    # -----------------------------------------------------

    st.subheader("🏆 Top 10 Products by Sales")

    top_products_query = """
    SELECT
        [Product Sub-Category],
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        COUNT(*) AS Total_Orders
    FROM retail
    GROUP BY [Product Sub-Category]
    ORDER BY Total_Sales DESC
    LIMIT 10
    """

    top_products_sql = pd.read_sql_query(
        top_products_query,
        conn
    )

    st.dataframe(
        top_products_sql,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # LOSS MAKING PRODUCTS
    # -----------------------------------------------------

    st.subheader("⚠️ Loss-Making Products")

    loss_query = """
    SELECT
        [Product Sub-Category],
        ROUND(SUM(Sales), 2) AS Total_Sales,
        ROUND(SUM(Profit), 2) AS Total_Profit,
        COUNT(*) AS Total_Orders
    FROM retail
    GROUP BY [Product Sub-Category]
    HAVING SUM(Profit) < 0
    ORDER BY Total_Profit ASC
    """

    loss_sql = pd.read_sql_query(
        loss_query,
        conn
    )

    st.dataframe(
        loss_sql,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # SQL SUMMARY
    # -----------------------------------------------------

    st.success(
        "SQL Analysis successfully loaded from SQLite database."
    )

    st.caption(
        "Database: retail.db  |  Table: retail  |  Analysis: SQLite SQL"
    )
# =========================================================
# POWER BI DASHBOARD
# =========================================================

elif page == "📊 Power BI Dashboard":

    st.html(f"""
    <div style="
        background:{CARD};
        border:1px solid {BORDER};
        border-radius:18px;
        padding:25px;
        margin-bottom:20px;
    ">
        <div style="
            font-size:25px;
            font-weight:800;
            color:{TEXT};
        ">
            📊 Power BI Dashboard
        </div>

        <div style="
            color:{MUTED};
            margin-top:7px;
        ">
            Interactive Sales Analytics Dashboard
        </div>
    </div>
    """)

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNzUwZDI1NjYtZjQ2Zi00M2FmLWE1MDQtYjFlNWQ3ODAwZTUxIiwidCI6IjcwMzY2YzAyLTkwOTUtNDMwOS04MDFhLTQ1MzUyOTUwYzg0MiJ9"

    st.components.v1.iframe(
        src=powerbi_url,
        height=750,
        scrolling=True
    )
# =========================================================
# ABOUT MODEL
# =========================================================

elif page == "🤖 About Model":

    st.html(f"""
    <div style="
        background:{CARD};
        border:1px solid {BORDER};
        border-radius:18px;
        padding:25px;
        margin-bottom:20px;
    ">

        <div style="
            font-size:25px;
            font-weight:800;
            color:{TEXT};
        ">
            🤖 About the Machine Learning Model
        </div>

        <div style="
            color:{MUTED};
            margin-top:7px;
        ">
            Gradient Boosting based Sales Prediction Model
        </div>

    </div>
    """)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "R² Score",
            "94.96%"
        )

    with c2:
        st.metric(
            "RMSE",
            "498.65"
        )

    with c3:
        st.metric(
            "MAE",
            "150.10"
        )

    st.markdown("")

    st.subheader("📊 Model Comparison")

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

    st.subheader("⭐ Important Features")

    feature_importance = pd.DataFrame({
        "Feature": [
            "QtyOrdered",
            "Unit Price",
            "Discount offered",
            "Order Day",
            "Region West",
            "Freight Expenses",
            "Order Year"
        ],
        "Importance": [
            0.567236,
            0.403263,
            0.014899,
            0.003250,
            0.002119,
            0.001536,
            0.001186
        ]
    })

    st.bar_chart(
        feature_importance.set_index("Feature")
    )

    st.info(
        "Sales prediction is a regression problem. "
        "Therefore MAE, RMSE and R² are used to evaluate the model "
        "instead of classification accuracy."
    )


# =========================================================
# FOOTER
# =========================================================

st.html(f"""
<div style="
    margin-top:45px;
    padding:20px;
    text-align:center;
    border-top:1px solid {BORDER};
    color:{MUTED};
    font-size:13px;
">

    <div style="
        font-size:17px;
        font-weight:700;
        color:{TEXT};
    ">
        📊 SalesAI
    </div>

    <div style="margin-top:6px;">
        Sales Prediction & Business Decision Support System
    </div>

    <div style="margin-top:5px;">
        Built with Python • Streamlit • Machine Learning
    </div>

</div>
""")
