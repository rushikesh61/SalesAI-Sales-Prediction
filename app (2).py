import streamlit as st
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

try:
    model = load_model()
    model_error = None
except Exception as exc:
    model = None
    model_error = str(exc)

# =========================================================
# SESSION STATE
# =========================================================
if "night_mode" not in st.session_state:
    st.session_state.night_mode = False

# =========================================================
# THEME - NAVY BLUE + TEAL
# =========================================================
if st.session_state.night_mode:
    BG = "#071525"
    CARD = "#102338"
    CARD2 = "#142B40"
    TEXT = "#F1F7FC"
    MUTED = "#B8C9D9"
    BORDER = "#29445C"
    INPUT_BG = "#142B40"
    ACCENT = "#22D3EE"
    SIDEBAR_BG = "#0B1B2B"
else:
    BG = "#F0F7FB"
    CARD = "#FFFFFF"
    CARD2 = "#E8F4F8"
    TEXT = "#172B3A"
    MUTED = "#506779"
    BORDER = "#D4E3EC"
    INPUT_BG = "#FFFFFF"
    ACCENT = "#087F8C"
    SIDEBAR_BG = "#FFFFFF"

# =========================================================
# GLOBAL CSS - IMPROVED NIGHT MODE VISIBILITY
# =========================================================
st.html(f"""
<style>
.stApp {{
    background: {BG} !important;
    color: {TEXT} !important;
}}
section[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {BORDER} !important;
}}
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp p, .stApp label, .stApp li {{
    color: {TEXT};
}}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    color: {TEXT} !important;
}}
.stApp input,
.stApp textarea,
.stApp [data-baseweb="input"] input,
.stApp [data-baseweb="textarea"] textarea {{
    background-color: {INPUT_BG} !important;
    color: {TEXT} !important;
    -webkit-text-fill-color: {TEXT} !important;
    border-color: {BORDER} !important;
    caret-color: {ACCENT} !important;
}}
.stApp [data-baseweb="select"] > div {{
    background-color: {INPUT_BG} !important;
    color: {TEXT} !important;
    border-color: {BORDER} !important;
}}
.stApp [data-baseweb="select"] span,
.stApp [data-baseweb="select"] input {{
    color: {TEXT} !important;
    -webkit-text-fill-color: {TEXT} !important;
}}
div[data-baseweb="popover"],
div[data-baseweb="menu"],
div[role="listbox"] {{
    background-color: {CARD} !important;
}}
div[role="option"],
div[role="listbox"] *,
div[data-baseweb="popover"] * {{
    color: {TEXT} !important;
}}
div[data-testid="stDateInput"] *,
div[data-baseweb="calendar"] *,
div[data-baseweb="datepicker"] * {{
    color: {TEXT} !important;
}}
div[data-baseweb="calendar"],
div[data-baseweb="datepicker"] {{
    background-color: {CARD} !important;
}}
.stApp [data-testid="stNumberInput"] button {{
    background-color: {CARD2} !important;
    color: {TEXT} !important;
}}
div[data-testid="stMetric"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 14px;
    padding: 16px;
}}
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
    color: {TEXT} !important;
    -webkit-text-fill-color: {TEXT} !important;
}}
.stApp details {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px;
}}
.stApp details summary,
.stApp button[role="tab"] {{
    color: {TEXT} !important;
}}
.stButton > button {{
    background: linear-gradient(135deg, #087F8C, #0891B2);
    color: #FFFFFF !important;
    border: none;
    border-radius: 12px;
    font-weight: 700;
    min-height: 44px;
    transition: all 0.2s ease;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #06A6A6, #0284C7);
    color: #FFFFFF !important;
    transform: translateY(-1px);
    box-shadow: 0 5px 18px rgba(8, 145, 178, 0.25);
}}
.stApp a {{
    color: {ACCENT} !important;
}}
</style>
""")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.html(f"""
    <div style="padding:8px 4px 20px;border-bottom:1px solid {BORDER};margin-bottom:20px;">
        <div style="font-size:26px;font-weight:800;color:{TEXT};">📊 SalesAI</div>
        <div style="font-size:12px;color:{MUTED};margin-top:6px;line-height:1.5;">
            Sales Prediction &amp; Business Decision Support
        </div>
    </div>
    """)

    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🔮 Sales Prediction", "💡 Business Insights", "🤖 About Model"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🎨 Appearance")
    night = st.toggle("🌙 Night Mode", value=st.session_state.night_mode)
    if night != st.session_state.night_mode:
        st.session_state.night_mode = night
        st.rerun()

    st.markdown("---")
    st.markdown("### 🟢 Model Status")
    if model is not None:
        st.success("Model Loaded")
        st.caption("Gradient Boosting Regressor")
        st.metric("Model R²", "94.96%")
    else:
        st.error("Model could not be loaded")
        st.caption("Check that sales_prediction_final_model.pkl is in the same folder as app.py.")

# =========================================================
# HERO BANNER
# =========================================================
st.html("""
<div style="
    background:linear-gradient(135deg,#0F766E 0%,#0891B2 48%,#2563EB 100%);
    border-radius:24px;padding:38px;margin-bottom:25px;
    box-shadow:0 18px 45px rgba(8,145,178,0.22);color:#FFFFFF;">
    <div style="font-size:42px;font-weight:900;color:#FFFFFF;margin-bottom:8px;">
        📊 SalesAI
    </div>
    <div style="font-size:20px;font-weight:600;color:#FFFFFF;margin-bottom:18px;">
        Intelligent Sales Prediction &amp; Business Decision Support
    </div>
    <div style="display:inline-block;padding:8px 16px;border-radius:30px;
        background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.3);
        font-size:14px;color:#FFFFFF;">
        🤖 Machine Learning &nbsp; • &nbsp; 📈 Business Analytics &nbsp; • &nbsp; 🔮 Sales Prediction
    </div>
</div>
""")

if model_error:
    st.error(f"Model loading error: {model_error}")
    st.stop()

# =========================================================
# DASHBOARD
# =========================================================
if page == "🏠 Dashboard":
    st.html(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;
        padding:25px;margin-bottom:20px;">
        <div style="font-size:25px;font-weight:800;color:{TEXT};">👋 Welcome to SalesAI</div>
        <div style="color:{MUTED};font-size:15px;margin-top:8px;">
            Analyze sales information, predict expected sales, and generate business-oriented insights.
        </div>
    </div>
    """)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("🎯", "Problem Type", "Regression"),
        ("🧠", "ML Algorithm", "Gradient Boosting"),
        ("📈", "Model Performance", "R² = 94.96%"),
        ("🇮🇳", "Market", "India")
    ]
    for col, (icon, label, value) in zip([c1, c2, c3, c4], cards):
        with col:
            st.html(f"""
            <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;
                padding:22px;min-height:130px;">
                <div style="font-size:28px;">{icon}</div>
                <div style="color:{MUTED};font-size:13px;margin-top:8px;">{label}</div>
                <div style="color:{TEXT};font-size:20px;font-weight:800;margin-top:5px;">{value}</div>
            </div>
            """)

    st.markdown("")
    st.subheader("🚀 What can you do?")
    a, b, c = st.columns(3)
    feature_cards = [
        ("🔮", "Predict Sales", "Enter order, product and regional information to estimate expected sales."),
        ("📊", "Analyze Business", "Understand product, segment, regional and seasonal sales performance."),
        ("💡", "Make Decisions", "Use predictions and business insights to support inventory and sales planning.")
    ]
    for col, (icon, title, desc) in zip([a, b, c], feature_cards):
        with col:
            st.html(f"""
            <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;
                padding:25px;min-height:180px;">
                <div style="font-size:35px;">{icon}</div>
                <div style="color:{TEXT};font-size:20px;font-weight:800;margin:10px 0 8px;">{title}</div>
                <div style="color:{MUTED};line-height:1.6;">{desc}</div>
            </div>
            """)

# =========================================================
# SALES PREDICTION
# =========================================================
elif page == "🔮 Sales Prediction":
    st.html(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;
        padding:25px;margin-bottom:20px;">
        <div style="font-size:25px;font-weight:800;color:{TEXT};">🔮 Sales Prediction</div>
        <div style="color:{MUTED};margin-top:7px;">
            Enter order and product information to predict expected sales.
        </div>
    </div>
    """)

    st.subheader("🛒 Order Information")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        unit_price = st.number_input("Unit Price", min_value=0.0, value=100.0, step=1.0)
    with c2:
        qty_ordered = st.number_input("Quantity Ordered", min_value=1, value=10, step=1)
    with c3:
        discount = st.number_input("Discount Offered", min_value=0.0, value=0.0, step=0.1)
    with c4:
        freight_expenses = st.number_input("Freight Expenses", min_value=0.0, value=10.0, step=1.0)

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

    st.subheader("📦 Product & Customer Information")
    c1, c2, c3 = st.columns(3)
    with c1:
        order_priority = st.selectbox("Order Priority", ["High", "Low", "Not Specified", "Medium", "Critical"])
        freight_mode = st.selectbox("Freight Mode", ["Regular Air", "Delivery Truck", "Express Air"])
        segment = st.selectbox("Segment", ["Hotels / Hospitals", "Restaurant Chain", "Personel Usage", "Stand Alone Restaurants"])
    with c2:
        product_type = st.selectbox("Product Type", ["Processed Meat", "Canned Foods", "Preserved Food"])
        product_sub_category = st.selectbox(
            "Product Sub-Category",
            ["Smoked Salmon", "Quail Eggs", "Bacon", "Marmalade", "Assorted Fruits",
             "Foie Gras", "Fresh Water Eel", "Sliced Pineapple", "Jams", "Jelly Fish",
             "Sundried Tomatoes", "Wild Berry", "Pickle", "Caviar", "Pacific Squid",
             "Oysters (Clam)", "Tuna"]
        )
    with c3:
        product_container = st.selectbox(
            "Product Container",
            ["Small Box", "Wrap Bag", "Small Pack", "Jumbo Drum", "Jumbo Box", "Medium Box", "Large Box"]
        )
        state = st.selectbox(
            "State",
            ["Uttar Pradesh", "Madhya Pradesh", "Bihar", "Tamil Nadu", "Maharashtra",
             "West Bengal", "Andhra Pradesh", "Gujarat", "Rajasthan", "Jharkhand",
             "Karnataka", "Haryana", "Telangana", "Assam", "Kerala"]
        )
        region = st.selectbox("Region", ["North", "West", "South", "East"])

    st.html(f"""
    <div style="background:{CARD2};border:1px solid {BORDER};border-radius:18px;
        padding:22px;margin-top:20px;margin-bottom:20px;">
        <div style="font-size:19px;font-weight:800;color:{TEXT};margin-bottom:15px;">
            ⚡ Live Prediction Summary
        </div>
        <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:15px;">
            <div><div style="color:{MUTED};font-size:12px;">Unit Price</div>
                <div style="color:{TEXT};font-size:18px;font-weight:700;">₹{unit_price:,.2f}</div></div>
            <div><div style="color:{MUTED};font-size:12px;">Quantity</div>
                <div style="color:{TEXT};font-size:18px;font-weight:700;">{qty_ordered}</div></div>
            <div><div style="color:{MUTED};font-size:12px;">Discount</div>
                <div style="color:{TEXT};font-size:18px;font-weight:700;">{discount:.1f}</div></div>
            <div><div style="color:{MUTED};font-size:12px;">Region</div>
                <div style="color:{TEXT};font-size:18px;font-weight:700;">{region}</div></div>
        </div>
    </div>
    """)

    st.subheader("🚀 Generate Prediction")
    if st.button("🔮 Predict Expected Sales", use_container_width=True, type="primary"):
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

        prediction = float(model.predict(input_data)[0])
        if prediction < 500:
            category, emoji = "Low Sales", "🔵"
        elif prediction < 2000:
            category, emoji = "Medium Sales", "🟡"
        else:
            category, emoji = "High Sales", "🟢"

        st.html(f"""
        <div style="background:linear-gradient(135deg,#0F766E,#0891B2,#2563EB);
            border:1px solid #38BDF8;border-radius:22px;padding:32px;margin-top:24px;
            text-align:center;box-shadow:0 12px 35px rgba(8,145,178,0.20);">
            <div style="font-size:18px;font-weight:600;color:#FFFFFF;margin-bottom:8px;">
                💰 Predicted Sales
            </div>
            <div style="font-size:44px;font-weight:900;color:#FFFFFF;margin:10px 0;">
                ₹{prediction:,.2f}
            </div>
            <div style="display:inline-block;background:rgba(255,255,255,0.18);
                border:1px solid rgba(255,255,255,0.35);border-radius:30px;
                padding:8px 18px;color:#FFFFFF;font-size:16px;font-weight:700;">
                {emoji} {category}
            </div>
        </div>
        """)

        st.subheader("💡 Business Recommendation")
        if prediction >= 2000:
            st.success("High expected sales. Consider maintaining sufficient inventory and preparing distribution capacity.")
        elif prediction >= 500:
            st.info("Medium expected sales. Monitor demand and maintain balanced inventory levels.")
        else:
            st.warning("Low expected sales. Review pricing, demand and promotional strategy before increasing inventory.")

        with st.expander("🔎 View Prediction Input Data"):
            st.dataframe(input_data, use_container_width=True)

# =========================================================
# BUSINESS INSIGHTS
# =========================================================
elif page == "💡 Business Insights":
    st.html(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;
        padding:25px;margin-bottom:20px;">
        <div style="font-size:25px;font-weight:800;color:{TEXT};">💡 Business Insights</div>
        <div style="color:{MUTED};margin-top:7px;">Key findings obtained from the sales analysis.</div>
    </div>
    """)

    st.subheader("📦 Product Strategy")
    c1, c2 = st.columns(2)
    with c1:
        st.html(f"""
        <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;padding:25px;">
            <div style="font-size:32px;">🏆</div>
            <div style="color:{TEXT};font-size:20px;font-weight:800;margin-top:8px;">Sliced Pineapple</div>
            <div style="color:{MUTED};margin-top:8px;line-height:1.6;">
                Highest total sales among product sub-categories. Maintain sufficient inventory and strengthen marketing.
            </div>
        </div>
        """)
    with c2:
        st.html(f"""
        <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;padding:25px;">
            <div style="font-size:32px;">⚠️</div>
            <div style="color:{TEXT};font-size:20px;font-weight:800;margin-top:8px;">Jams &amp; Tuna</div>
            <div style="color:{MUTED};margin-top:8px;line-height:1.6;">
                Negative total profit. Review pricing, discounts and procurement costs.
            </div>
        </div>
        """)

    st.markdown("")
    st.subheader("🌍 Regional Strategy")
    c1, c2 = st.columns(2)
    with c1:
        st.html(f"""
        <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;padding:25px;">
            <div style="font-size:32px;">🥇</div>
            <div style="color:{TEXT};font-size:20px;font-weight:800;">North Region</div>
            <div style="color:{MUTED};margin-top:8px;">Highest total sales and total profit. Prioritize inventory, distribution and marketing.</div>
        </div>
        """)
    with c2:
        st.html(f"""
        <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;padding:25px;">
            <div style="font-size:32px;">📍</div>
            <div style="color:{TEXT};font-size:20px;font-weight:800;">Haryana</div>
            <div style="color:{MUTED};margin-top:8px;">Negative total profit. Investigate pricing, discounts and logistics costs.</div>
        </div>
        """)

    st.markdown("")
    st.subheader("👥 Segment Strategy")
    st.html(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;padding:25px;">
        <div style="font-size:32px;">🏢</div>
        <div style="color:{TEXT};font-size:20px;font-weight:800;margin-top:8px;">Stand Alone Restaurants</div>
        <div style="color:{MUTED};margin-top:8px;line-height:1.6;">
            This segment generated the highest total profit and average profit. It can be a priority segment for profitable customer-focused strategies.
        </div>
    </div>
    """)

    st.markdown("")
    st.subheader("📅 Seasonal Strategy")
    st.html("""
    <div style="background:linear-gradient(135deg,#C2410C,#BE185D);
        border-radius:18px;padding:28px;color:#FFFFFF;">
        <div style="font-size:34px;">🔥</div>
        <div style="color:#FFFFFF;font-size:24px;font-weight:800;">November Peak</div>
        <div style="color:#FFFFFF;margin-top:8px;line-height:1.6;">
            November recorded the highest total sales. Increase inventory and promotional planning before the peak period.
        </div>
    </div>
    """)

# =========================================================
# ABOUT MODEL
# =========================================================
elif page == "🤖 About Model":
    st.html(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:18px;
        padding:25px;margin-bottom:20px;">
        <div style="font-size:25px;font-weight:800;color:{TEXT};">🤖 About the Machine Learning Model</div>
        <div style="color:{MUTED};margin-top:7px;">Gradient Boosting based Sales Prediction Model</div>
    </div>
    """)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("R² Score", "94.96%")
    with c2:
        st.metric("RMSE", "498.65")
    with c3:
        st.metric("MAE", "150.10")

    st.markdown("")
    st.subheader("📊 Model Comparison")
    comparison = pd.DataFrame({
        "Model": ["Gradient Boosting", "Random Forest", "Decision Tree", "Linear Regression"],
        "MAE": [150.10, 189.51, 268.96, 884.79],
        "RMSE": [498.65, 783.40, 1241.98, 1612.60],
        "R²": [0.9496, 0.8756, 0.6874, 0.4729]
    })
    st.dataframe(comparison, use_container_width=True, hide_index=True)

    st.subheader("⭐ Important Features")
    feature_importance = pd.DataFrame({
        "Feature": [
            "QtyOrdered", "Unit Price", "Discount offered", "Order Day",
            "Region West", "Freight Expenses", "Order Year"
        ],
        "Importance": [0.567236, 0.403263, 0.014899, 0.003250, 0.002119, 0.001536, 0.001186]
    })
    st.bar_chart(feature_importance.set_index("Feature"))

    st.info(
        "Sales prediction is a regression problem. Therefore, MAE, RMSE and R² are used "
        "to evaluate the model instead of classification accuracy."
    )

# =========================================================
# FOOTER
# =========================================================
st.html(f"""
<div style="margin-top:45px;padding:20px;text-align:center;border-top:1px solid {BORDER};
    color:{MUTED};font-size:13px;">
    <div style="font-size:17px;font-weight:700;color:{TEXT};">📊 SalesAI</div>
    <div style="margin-top:6px;">Sales Prediction &amp; Business Decision Support System</div>
    <div style="margin-top:5px;">Built with Python • Streamlit • Machine Learning</div>
</div>
""")
