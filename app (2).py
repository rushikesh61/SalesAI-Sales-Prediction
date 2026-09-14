```python
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
```
