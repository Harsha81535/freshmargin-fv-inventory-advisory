from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# FreshMargin | F&V inventory and finance advisory POV
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"

st.set_page_config(page_title="FreshMargin | F&V Advisory POV", page_icon="🥑", layout="wide", initial_sidebar_state="collapsed")

NAVY = "#17324D"
TEAL = "#247C78"
GREEN = "#5C8A4B"
ORANGE = "#E79A48"
INK = "#203247"
MUTED = "#64758B"
BG = "#F5F8F5"

st.markdown(f"""
<style>
.stApp {{ background: {BG}; color: {INK}; }}
[data-testid="stSidebar"] {{ display: none; }}
[data-testid="collapsedControl"] {{ display: none; }}
.top-nav [role="radiogroup"] {{ gap: 8px; flex-wrap: wrap; }}
.top-nav [role="radio"] {{ background: #FFFFFF; border: 1px solid #D9E5DF; border-radius: 999px; padding: 8px 14px; }}
.top-nav [role="radio"] p {{ font-weight: 650; font-size: .88rem; }}
.scope-strip {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; background: #EAF4F1; border: 1px solid #D8E9E2; border-radius: 12px; padding: 12px 16px; margin: 0 0 22px 0; }}
.scope-pill {{ background: white; border: 1px solid #D7E6DF; padding: 6px 10px; border-radius: 999px; font-size: .78rem; color: {INK}; }}
.rec-card {{ position: relative; overflow: hidden; background: #FFFFFF; border: 1px solid #DCE8E1; border-radius: 17px; padding: 20px 20px 18px 20px; min-height: 208px; box-shadow: 0 5px 16px rgba(23,50,77,.045); }}
.rec-card:before {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 5px; background: {TEAL}; }}
.rec-card.orange:before {{ background: {ORANGE}; }}
.rec-card.green:before {{ background: {GREEN}; }}
.rec-icon {{ font-size: 1.8rem; margin-bottom: 12px; }}
.rec-number {{ color: {TEAL}; font-size: .72rem; font-weight: 850; letter-spacing: .12em; text-transform: uppercase; }}
.rec-card h3 {{ margin: 6px 0 9px 0; font-size: 1.08rem; }}
.rec-card p {{ color: {INK}; font-size: .92rem; line-height: 1.55; margin-bottom: 0; }}
.rec-flow {{ color: {TEAL}; font-size: 1.4rem; font-weight: 800; text-align: center; padding: 5px 0; }}
.block-container {{ padding-top: 1.5rem; padding-bottom: 2.5rem; max-width: 1450px; }}
h1,h2,h3,h4,p,li,label {{ color: {INK}; }}
.hero {{ background: linear-gradient(115deg, {NAVY} 0%, #28596A 70%, {TEAL} 100%); padding: 30px 34px; border-radius: 20px; color: white; margin-bottom: 20px; position: relative; overflow: hidden; }}
.hero h1 {{ color: white !important; font-size: 2.45rem; line-height: 1.12; margin: 8px 0 10px 0; }}
.hero p {{ color: #E7F2F0 !important; font-size: 1.05rem; max-width: 850px; margin: 0; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: .12em; font-size: .76rem; font-weight: 750; color: #B8E1D9; }}
.byline {{ text-align: right; color: #F4FAFC; font-size: .91rem; line-height: 1.5; padding-top: 4px; }}
.byline strong {{ color: white; font-size: 1rem; }}
.produce-strip {{ font-size: 1.55rem; letter-spacing: .12rem; margin-top: 16px; }}
.section-kicker {{ color: {TEAL}; font-size: .78rem; text-transform: uppercase; letter-spacing: .11em; font-weight: 800; margin-bottom: 3px; }}
.panel {{ background: white; border: 1px solid #E1EAE4; border-radius: 15px; padding: 18px 20px; height: 100%; }}
.panel h3 {{ margin-top: 0; font-size: 1.08rem; }}
.kpi {{ background: white; border: 1px solid #E1EAE4; border-radius: 15px; padding: 16px 18px; min-height: 116px; }}
.kpi-label {{ color: {MUTED}; font-size: .82rem; margin-bottom: 7px; }}
.kpi-value {{ color: {NAVY}; font-size: 1.8rem; font-weight: 800; line-height: 1.15; }}
.kpi-note {{ color: {MUTED}; font-size: .76rem; margin-top: 7px; }}
.note {{ background: #EAF4F1; border-left: 4px solid {TEAL}; border-radius: 9px; padding: 13px 16px; margin: 10px 0 16px 0; }}
.caution {{ background: #FFF5E6; border-left: 4px solid {ORANGE}; border-radius: 9px; padding: 13px 16px; margin: 10px 0 16px 0; }}
.step {{ background: white; border: 1px solid #E1EAE4; border-radius: 14px; padding: 16px; min-height: 145px; }}
.step-num {{ color: {TEAL}; font-size: .75rem; font-weight: 800; letter-spacing: .08em; }}
div[data-testid="stMetric"] {{ background: white; border: 1px solid #E1EAE4; padding: 14px; border-radius: 12px; }}
[data-testid="stDataFrame"] {{ border-radius: 12px; }}
footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def read_csv(name):
    p = OUT / name
    if p.exists():
        return pd.read_csv(p)
    return pd.DataFrame()

forecast = read_csv("demand_forecast_summary.csv")
closing = read_csv("closing_inventory_batches.csv")
projected = read_csv("projected_expiry_exposure.csv")
risk = read_csv("sku_inventory_risk.csv")
daily = read_csv("daily_inventory_ledger.csv")
expiry_events = read_csv("historical_simulated_expiry_events.csv")

# Summary values from the completed notebooks/README; clearly labelled as simulated or audited dataset observations.
WAPE = 67.40
FRN_ROWS = 4_500_000
FRN_STOCKOUT_SHARE = 44.27
FRN_AVG_STOCKOUT_HOURS = 3.18
FRN_FULL_WINDOW_SHARE = 4.04

closing_units = int(pd.to_numeric(closing.get("remaining_qty", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
closing_cost = float(pd.to_numeric(closing.get("inventory_value", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
expiry_units = int(pd.to_numeric(projected.get("projected_waste_units", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
expiry_cost = float(pd.to_numeric(projected.get("projected_waste_cost", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
skus = int(closing["item_id"].nunique()) if "item_id" in closing else (int(daily["item_id"].nunique()) if "item_id" in daily else 0)

# Consistent project header across pages
st.markdown(f"""
<div class="hero">
  <div class="eyebrow">Evidence-led business advisory POV · Fresh produce</div>
  <div style="display:flex; justify-content:space-between; gap:24px; align-items:flex-start; flex-wrap:wrap;">
