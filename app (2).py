import streamlit as st
import pandas as pd
import joblib
import sqlite3
from datetime import date
import os
from io import BytesIO

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
# THEME COLORS
# =========================================================

if st.session_state.night_mode:

    BG = "#07111F"
    CARD = "#0D1B2A"
    CARD_2 = "#10243A"
    TEXT = "#F8FAFC"
    MUTED = "#CBD5E1"
    BORDER = "#1E3A5F"
    INPUT_BG = "#0B1726"

else:

    BG = "#F4F7FB"
    CARD = "#FFFFFF"
    CARD_2 = "#F8FAFC"
    TEXT = "#0F172A"
    MUTED = "#475569"
    BORDER = "#D9E2EC"
    INPUT_BG = "#FFFFFF"


# =========================================================
# CUSTOM CSS
# =========================================================

st.html(
    f"""
<style>

html, body, [class*="css"] {{
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}}

.stApp {{
    background: {BG};
    color: {TEXT};
}}

.main {{
    background: {BG};
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
    color: {TEXT} !important;
}}

section[data-testid="stSidebar"] .stRadio label {{
    color: {TEXT} !important;
    font-weight: 600;
}}

section[data-testid="stSidebar"] .stCheckbox label {{
    color: {TEXT} !important;
}}

/* =====================================================
   GENERAL TEXT
   ===================================================== */

p, span, label, div {{
    color: {TEXT};
}}

h1, h2, h3, h4, h5, h6 {{
    color: {TEXT} !important;
}}

.stMarkdown {{
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
    border: 1px solid #1E40AF;
    border-radius: 24px;
    padding: 45px;
    margin-bottom: 28px;
    box-shadow: 0 20px 50px rgba(15,23,42,0.30);
}}

.hero-content {{
    max-width: 900px;
}}

.hero-badge {{
    display: inline-block;
    background: rgba(56,189,248,0.15);
    color: #7DD3FC !important;
    border: 1px solid rgba(125,211,252,0.35);
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 15px;
}}

.hero-title {{
    font-size: 52px;
    font-weight: 900;
    color: #FFFFFF !important;
    line-height: 1.1;
}}

.hero-subtitle {{
    margin-top: 12px;
    font-size: 19px;
    line-height: 1.6;
    color: #CBD5E1 !important;
}}

/* =====================================================
   SECTION HEADINGS
   ===================================================== */

.section-kicker {{
    color: #38BDF8 !important;
    font-size: 12px;
    font-weight: 850;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 20px;
}}

.section-title {{
    color: {TEXT} !important;
    font-size: 30px;
    font-weight: 850;
    margin-bottom: 8px;
}}

.section-description {{
    color: {MUTED} !important;
    font-size: 15px;
    margin-bottom: 22px;
}}

/* =====================================================
   KPI CARDS
   ===================================================== */

.kpi-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.10);
}}

.kpi-label {{
    color: {MUTED} !important;
    font-size: 13px;
    font-weight: 700;
}}

.kpi-value {{
    color: {TEXT} !important;
    font-size: 31px;
    font-weight: 900;
    margin-top: 8px;
}}

.kpi-sub {{
    color: #38BDF8 !important;
    font-size: 12px;
    font-weight: 700;
    margin-top: 5px;
}}

/* =====================================================
   INFO CARDS
   ===================================================== */

.info-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 24px;
    margin: 8px 0;
    min-height: 155px;
}}

.info-icon {{
    font-size: 28px;
}}

.info-title {{
    color: {TEXT} !important;
    font-size: 18px;
    font-weight: 800;
    margin-top: 8px;
}}

.info-text {{
    color: {MUTED} !important;
    font-size: 14px;
    line-height: 1.6;
    margin-top: 6px;
}}

/* =====================================================
   FORM LABELS
   ===================================================== */

.stSelectbox label,
.stNumberInput label,
.stDateInput label,
.stTextInput label {{
    color: {TEXT} !important;
    font-weight: 750 !important;
}}

.stSelectbox div,
.stNumberInput div,
.stDateInput div {{
    color: {TEXT} !important;
}}

/* =====================================================
   INPUTS
   ===================================================== */

.stSelectbox > div > div,
.stNumberInput > div > div,
.stDateInput > div > div {{
    background: {INPUT_BG} !important;
    border-color: {BORDER} !important;
}}

.stSelectbox input,
.stNumberInput input,
.stDateInput input {{
    color: {TEXT} !important;
    background: {INPUT_BG} !important;
}}

.stSelectbox [data-baseweb="select"] {{
    background: {INPUT_BG} !important;
}}

.stSelectbox [data-baseweb="select"] * {{
    color: {TEXT} !important;
}}

/* Dropdown menu */

div[data-baseweb="popover"] {{
    background: {CARD} !important;
}}

div[data-baseweb="menu"] {{
    background: {CARD} !important;
}}

div[data-baseweb="menu"] li {{
    background: {CARD} !important;
    color: {TEXT} !important;
}}

div[data-baseweb="menu"] li:hover {{
    background: #1E3A5F !important;
    color: #FFFFFF !important;
}}

/* Date picker */

div[data-baseweb="calendar"] {{
    background: {CARD} !important;
}}

div[data-baseweb="calendar"] * {{
    color: {TEXT} !important;
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
        0 8px 25px rgba(37,99,235,0.35);

    transition: all 0.2s ease;
}}

.stButton > button p {{
    color: #FFFFFF !important;
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
        0 14px 35px rgba(37,99,235,0.50);
}}

.stButton > button:focus {{
    color: #FFFFFF !important;
    border: 2px solid #7DD3FC;

    box-shadow:
        0 0 0 4px rgba(56,189,248,0.20);
}}

/* =====================================================
   DOWNLOAD BUTTON
   ===================================================== */

.stDownloadButton > button {{
    width: 100%;
    min-height: 50px;
    border-radius: 14px;
    border: 1px solid #38BDF8;
    padding: 13px 20px;
    font-size: 15px;
    font-weight: 800;
    color: #FFFFFF !important;

    background:
        linear-gradient(
            135deg,
            #0369A1 0%,
            #1D4ED8 50%,
            #4338CA 100%
        ) !important;

    box-shadow:
        0 7px 22px rgba(37,99,235,0.30);

    transition: all 0.2s ease;
}}

.stDownloadButton > button p {{
    color: #FFFFFF !important;
}}

.stDownloadButton > button:hover {{
    color: #FFFFFF !important;
    border: 1px solid #7DD3FC;
    transform: translateY(-2px);
    box-shadow:
        0 12px 30px rgba(37,99,235,0.45);
}}

/* =====================================================
   METRICS
   ===================================================== */

div[data-testid="stMetric"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 18px;
}}

div[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
}}

div[data-testid="stMetricValue"] {{
    color: {TEXT} !important;
}}

div[data-testid="stMetricDelta"] {{
    color: #38BDF8 !important;
}}

/* =====================================================
   DATAFRAME
   ===================================================== */

div[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 14px;
    overflow: hidden;
}}

/* =====================================================
   EXPANDER
   ===================================================== */

div[data-testid="stExpander"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
}}

div[data-testid="stExpander"] * {{
    color: {TEXT};
}}

/* =====================================================
   ALERT BOXES
   ===================================================== */

div[data-testid="stAlert"] {{
    border-radius: 14px;
}}

/* =====================================================
   FOOTER
   ===================================================== */

.footer {{
    text-align: center;
    padding: 30px 0 10px 0;
    color: {MUTED} !important;
    font-size: 13px;
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
            margin-bottom:5px;
        ">
            📊 SalesAI
        </div>

        <div style="
            color:#94A3B8;
            font-size:13px;
            margin-bottom:25px;
        ">
            Sales Prediction Platform
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

    st.markdown("---")

    night_mode = st.toggle(
        "🌙 Night Mode",
        value=st.session_state.night_mode
    )

    if night_mode != st.session_state.night_mode:
        st.session_state.night_mode = night_mode
        st.rerun()

    st.markdown("---")

    st.markdown("### 🤖 Model Status")

    if model_loaded:

        st.success("Model Loaded")

        st.markdown(
            """
            <div style="
                background:rgba(34,197,94,0.10);
                border:1px solid rgba(34,197,94,0.30);
                border-radius:10px;
                padding:10px;
                font-size:13px;
            ">
                Gradient Boosting Regressor
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.error("Model Not Found")

        st.caption(
            "Make sure sales_prediction_final_model.pkl "
            "is available in the repository."
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
            EXECUTIVE OVERVIEW
        </div>

        <div class="section-title">
            Sales Intelligence Dashboard
        </div>

        <div class="section-description">
            Monitor model performance and explore AI-powered
            sales analytics.
        </div>
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.html(
            """
            <div class="kpi-card">
                <div class="kpi-label">MODEL R²</div>
                <div class="kpi-value">94.96%</div>
                <div class="kpi-sub">Excellent Performance</div>
            </div>
            """
        )

    with col2:
        st.html(
            """
            <div class="kpi-card">
                <div class="kpi-label">MAE</div>
                <div class="kpi-value">150.10</div>
                <div class="kpi-sub">Low Prediction Error</div>
            </div>
            """
        )

    with col3:
        st.html(
            """
            <div class="kpi-card">
                <div class="kpi-label">RMSE</div>
                <div class="kpi-value">498.65</div>
                <div class="kpi-sub">Strong Accuracy</div>
            </div>
            """
        )

    with col4:
        st.html(
            """
            <div class="kpi-card">
                <div class="kpi-label">BEST MODEL</div>
                <div class="kpi-value">GBR</div>
                <div class="kpi-sub">Gradient Boosting</div>
            </div>
            """
        )

    st.markdown("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.html(
            """
            <div class="info-card">
                <div class="info-icon">🔮</div>
                <div class="info-title">Predict Sales</div>
                <div class="info-text">
                    Enter order and product details to generate
                    AI-powered sales predictions.
                </div>
            </div>
            """
        )

    with col2:
        st.html(
            """
            <div class="info-card">
                <div class="info-icon">💡</div>
                <div class="info-title">Business Insights</div>
                <div class="info-text">
                    Discover profitable products, regions and
                    important sales patterns.
                </div>
            </div>
            """
        )

    with col3:
        st.html(
            """
            <div class="info-card">
                <div class="info-icon">📊</div>
                <div class="info-title">Power BI Analytics</div>
                <div class="info-text">
                    Explore interactive dashboards for deeper
                    business analysis.
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

        <div class="section-description">
            Enter the order details below and let the trained
            Gradient Boosting model estimate expected sales.
        </div>
        """
    )

    if not model_loaded:

        st.error(
            "Model could not be loaded. "
            "Please check sales_prediction_final_model.pkl."
        )

    else:

        st.markdown("### 🧾 Order Information")

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
                value=20.0,
                step=1.0
            )

        st.markdown("### 📅 Order Date")

        col1, col2 = st.columns(2)

        with col1:

            order_date = st.date_input(
                "Order Date",
                value=date.today()
            )

        with col2:

            order_year = order_date.year
            order_month = order_date.month
            order_quarter = ((order_month - 1) // 3) + 1
            order_day = order_date.day
            order_dayofweek = order_date.weekday()

            st.info(
                f"Year: {order_year}  |  "
                f"Month: {order_month}  |  "
                f"Quarter: Q{order_quarter}"
            )

        st.markdown("### 🚚 Order Details")

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

        st.markdown("### 📦 Product Information")

        col1, col2 = st.columns(2)

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

        col1, col2 = st.columns(2)

        with col1:

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

        with col2:

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

        st.markdown("### 🌎 Region")

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

            try:

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

                st.session_state.last_prediction = prediction

                # =================================================
                # SALES CATEGORY
                # =================================================

                if prediction < 500:

                    category = "Low Sales 📉"

                elif prediction < 2000:

                    category = "Medium Sales 📊"

                else:

                    category = "High Sales 🚀"

                st.success(
                    "Sales prediction generated successfully!"
                )

                st.markdown("## 📈 Prediction Result")

                result_col1, result_col2 = st.columns(2)

                with result_col1:

                    st.metric(
                        "Predicted Sales",
                        f"{prediction:,.2f}"
                    )

                with result_col2:

                    st.metric(
                        "Sales Category",
                        category
                    )

                # =================================================
                # DOWNLOAD PREDICTION
                # =================================================

                st.markdown("---")

                st.markdown("### 📥 Download Prediction")

                # Combine input details + prediction
                prediction_details = input_data.copy()

                prediction_details["Predicted Sales"] = round(
                    prediction,
                    2
                )

                prediction_details["Sales Category"] = category

                prediction_details["Prediction Date"] = (
                    date.today().isoformat()
                )

                # Show complete prediction details
                st.dataframe(
                    prediction_details,
                    use_container_width=True,
                    hide_index=True
                )

                download_col1, download_col2 = st.columns(2)

                # =================================================
                # CSV DOWNLOAD
                # =================================================

                with download_col1:

                    csv_data = (
                        prediction_details
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        label="⬇️ Download Prediction CSV",
                        data=csv_data,
                        file_name="sales_prediction_result.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                # =================================================
                # EXCEL DOWNLOAD
                # =================================================

                with download_col2:

                    excel_buffer = BytesIO()

                    with pd.ExcelWriter(
                        excel_buffer,
                        engine="openpyxl"
                    ) as writer:

                        prediction_details.to_excel(
                            writer,
                            index=False,
                            sheet_name="Prediction"
                        )

                        worksheet = writer.sheets["Prediction"]

                        # Header formatting
                        header_fill = PatternFill(
                            fill_type="solid",
                            fgColor="1D4ED8"
                        )

                        header_font = Font(
                            color="FFFFFF",
                            bold=True
                        )

                        header_alignment = Alignment(
                            horizontal="center"
                        )

                        for cell in worksheet[1]:

                            cell.fill = header_fill
                            cell.font = header_font
                            cell.alignment = header_alignment

                        # Automatic column width
                        for column_cells in worksheet.columns:

                            max_length = 0

                            column_letter = (
                                get_column_letter(
                                    column_cells[0].column
                                )
                            )

                            for cell in column_cells:

                                try:

                                    max_length = max(
                                        max_length,
                                        len(str(cell.value))
                                    )

                                except Exception:

                                    pass

                            worksheet.column_dimensions[
                                column_letter
                            ].width = min(
                                max_length + 3,
                                35
                            )

                    excel_buffer.seek(0)

                    st.download_button(
                        label="📊 Download Prediction Excel",
                        data=excel_buffer.getvalue(),
                        file_name="sales_prediction_result.xlsx",
                        mime=(
                            "application/vnd.openxmlformats-officedocument."
                            "spreadsheetml.sheet"
                        ),
                        use_container_width=True
                    )

                # =================================================
                # BUSINESS RECOMMENDATION
                # =================================================

                st.markdown("### 💡 Business Recommendation")

                if prediction < 500:

                    st.warning(
                        "Expected sales are relatively low. "
                        "Consider reviewing pricing, discount strategy, "
                        "product demand and promotion."
                    )

                elif prediction < 2000:

                    st.info(
                        "Expected sales are moderate. "
                        "Maintain balanced inventory and monitor "
                        "customer demand."
                    )

                else:

                    st.success(
                        "Expected sales are high. "
                        "Consider maintaining sufficient inventory "
                        "and prioritizing this order."
                    )

            except Exception as e:

                st.error(
                    "Prediction failed. Please check the input "
                    "values and model compatibility."
                )

                st.exception(e)


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

        <div class="section-description">
            Key findings and recommendations from the sales dataset.
        </div>
        """
    )

    col1, col2 = st.columns(2)

    with col1:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">🍍</div>

                <div class="info-title">
                    Highest Sales Product
                </div>

                <div class="info-text">
                    Sliced Pineapple recorded the highest total sales.
                    This indicates strong demand and potential for
                    inventory prioritization.
                </div>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">💰</div>

                <div class="info-title">
                    Highest Profit Product
                </div>

                <div class="info-text">
                    Quail Eggs recorded the highest total profit,
                    making it an important product for profitability.
                </div>

            </div>
            """
        )

    col1, col2 = st.columns(2)

    with col1:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">🌎</div>

                <div class="info-title">
                    Strongest Region
                </div>

                <div class="info-text">
                    North region shows strong sales performance
                    compared with other regions.
                </div>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">📅</div>

                <div class="info-title">
                    Peak Sales Month
                </div>

                <div class="info-text">
                    November recorded the highest sales activity.
                    Inventory planning should consider seasonal demand.
                </div>

            </div>
            """
        )

    st.markdown("### 🎯 Strategic Recommendations")

    recommendations = [
        "Prioritize inventory for high-performing products.",
        "Review products such as Jams and Tuna where profitability is weak.",
        "Analyze negative profitability patterns in Haryana.",
        "Use regional sales patterns for targeted marketing.",
        "Prepare additional inventory before November.",
        "Use the ML prediction system to support sales planning."
    ]

    for item in recommendations:

        st.markdown(
            f"• {item}"
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
            About the Model
        </div>

        <div class="section-description">
            Performance, comparison and explainability of the
            trained sales prediction model.
        </div>
        """
    )

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

    st.markdown("### 🧠 Selected Model")

    st.html(
        """
        <div class="info-card">

            <div class="info-icon">🤖</div>

            <div class="info-title">
                Gradient Boosting Regressor
            </div>

            <div class="info-text">
                Gradient Boosting Regressor was selected as the final
                model because it achieved the highest R² score and
                lowest prediction error among the tested models.
            </div>

        </div>
        """
    )

    st.markdown("### 📊 Model Comparison")

    comparison_df = pd.DataFrame({
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
            The chart below shows the relative importance of the
            features used by the trained Gradient Boosting model.
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

        feature_importance = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importance_values
        })

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

        # VERTICAL FEATURE IMPORTANCE CHART
        st.bar_chart(
            chart_data,
            height=600
        )

        st.caption(
            "Top 15 features ranked by their contribution "
            "to the Gradient Boosting model."
        )

        st.dataframe(
            feature_importance,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.warning(
            f"Feature importance could not be loaded: {e}"
        )

    st.markdown("### 🧾 Prediction Inputs")

    prediction_inputs = pd.DataFrame({
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
    })

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
            SQL Analysis
        </div>

        <div class="section-description">
            Explore sales data using SQLite queries.
        </div>
        """
    )

    db_path = "sales_data.db"

    if os.path.exists(db_path):

        try:

            conn = sqlite3.connect(db_path)

            table_query = """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """

            tables = pd.read_sql_query(
                table_query,
                conn
            )

            if not tables.empty:

                st.success(
                    "SQLite database connected successfully."
                )

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

            else:

                st.warning(
                    "No tables found in the database."
                )

            conn.close()

        except Exception as e:

            st.error(
                f"Database error: {e}"
            )

    else:

        st.info(
            "SQLite database file not found. "
            "Upload sales_data.db to enable SQL analysis."
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

        <div class="section-description">
            Interactive Power BI dashboard for detailed sales analysis.
        </div>
        """
    )

    st.info(
        "Paste your Power BI Publish-to-Web embed URL below."
    )

    powerbi_url = st.text_input(
        "Power BI Dashboard URL",
        placeholder="https://app.powerbi.com/view?r=..."
    )

    if powerbi_url:

        st.components.v1.iframe(
            powerbi_url,
            height=700,
            scrolling=True
        )

    else:

        st.html(
            """
            <div class="info-card">

                <div class="info-icon">📊</div>

                <div class="info-title">
                    Power BI Dashboard
                </div>

                <div class="info-text">
                    Add your Power BI Publish-to-Web link above
                    to display the interactive dashboard here.
                </div>

            </div>
            """
        )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="footer">
        SalesAI • Sales Prediction & Business Decision Support System
        <br>
        Powered by Machine Learning, Python, SQL & Power BI
    </div>
    """
)
