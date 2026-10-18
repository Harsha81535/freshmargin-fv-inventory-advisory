from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# FreshMargin | F&V inventory and finance advisory POV
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"

st.set_page_config(page_title="FreshMargin | F&V Advisory POV", page_icon="🥑", layout="wide", initial_sidebar_state="expanded")

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
[data-testid="stSidebar"] {{ background: {NAVY}; }}
[data-testid="stSidebar"] * {{ color: #F8FBFD !important; }}
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

st.sidebar.markdown("# 🥑 FreshMargin")
st.sidebar.caption("F&V INVENTORY & FINANCE ADVISORY")
page = st.sidebar.radio("Explore the analysis", [
    "01 · Executive Brief", "02 · Demand & Forecasts", "03 · Inventory & Expiry Risk",
    "04 · F&V Scenario Lab", "05 · Financial Impact", "06 · Evidence & Recommendations"
], label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.markdown("**Research scope**")
st.sidebar.caption("Independent case study · Public datasets + simulated inventory mechanics")
st.sidebar.caption("Not Swiggy data. Not measured company performance.")
st.sidebar.markdown("---")
st.sidebar.caption("Prepared by Harshana · MBA Finance, IMT Ghaziabad")

# Consistent project header across pages
st.markdown(f"""
<div class="hero">
  <div class="eyebrow">Evidence-led business advisory POV · Fresh produce</div>
  <div style="display:flex; justify-content:space-between; gap:24px; align-items:flex-start; flex-wrap:wrap;">
    <div style="flex:1; min-width:280px;">
      <h1>FreshMargin</h1>
      <p><strong style="color:#FFFFFF;">Protecting margin without compromising availability.</strong><br>Connect demand signals, inventory risk and financial decisions in one practical view of a fresh-produce business.</p>
      <div class="produce-strip">🥑 🥦 🍅 🥕 🍎 🥬 🍋</div>
    </div>
    <div class="byline"><strong>Prepared by: Harshana</strong><br>MBA Finance<br>IMT Ghaziabad</div>
  </div>
</div>
""", unsafe_allow_html=True)


def kicker(text): st.markdown(f'<div class="section-kicker">{text}</div>', unsafe_allow_html=True)
def kpi(label, value, note):
    st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>', unsafe_allow_html=True)
def chart_style(fig, height=330):
    fig.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="white", font=dict(color=INK, size=12), margin=dict(l=12,r=12,t=30,b=12), height=height, legend_title_text="")
    fig.update_xaxes(showgrid=False, tickfont=dict(color=INK))
    fig.update_yaxes(gridcolor="#E7ECE8", tickfont=dict(color=INK), rangemode="tozero")
    return fig

if page == "01 · Executive Brief":
    kicker("Start here · The decision context")
    st.title("Why fresh inventory is a finance problem, too")
    st.write("Fresh produce creates a daily balancing act: too little stock can mean missed sales; too much can age out before it sells. The commercial question is not simply how to forecast demand—it is how to make better inventory decisions while protecting availability and contribution margin.")
    st.markdown('<div class="note"><strong>Advisory question</strong><br>How can a fresh-produce business balance demand, availability, inventory cost and potential expiry risk—and which interventions deserve a real-world pilot?</div>', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    with a: kpi("Products in M5 inventory model", f"{skus:,}", "Food-product SKUs in the selected dataset")
    with b: kpi("Forecast baseline WAPE", f"{WAPE:.2f}%", "High error; not operationally ready")
    with c: kpi("Modelled expiry cost exposure", f"${expiry_cost:,.0f}", f"{expiry_units:,} units in a simulated 7-day scenario")
    st.markdown("### The story: why → what → how")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="step"><div class="step-num">01 · WHY</div><h3>Freshness creates trade-offs</h3><p>Availability, excess stock and product life all affect the economics of fresh produce.</p>🍅 🥬</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="step"><div class="step-num">02 · WHAT</div><h3>Make the risk visible</h3><p>Connect demand forecasts with simulated stock, batch ageing and potential expiry exposure.</p>📦 📈</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="step"><div class="step-num">03 · HOW</div><h3>Test decisions, not assumptions</h3><p>Explore ordering, markdown and transfer scenarios—then validate with real operating data.</p>🧮 🎯</div>', unsafe_allow_html=True)
    st.markdown("### What the evidence currently supports")
    left,right = st.columns(2)
    with left:
        st.markdown('<div class="panel"><h3>What we have built</h3><ul><li>Demand baseline and held-out forecast evaluation</li><li>Inventory replenishment and batch-level simulation</li><li>Expiry-risk estimate and inventory reconciliation checks</li><li>Interactive produce scenario with editable financial assumptions</li></ul></div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>What we have not proved</h3><ul><li>Actual fresh-produce wastage or stockouts at any company</li><li>Realised savings or incremental contribution</li><li>That any one intervention is optimal</li><li>That the model is ready for live replenishment decisions</li></ul></div>', unsafe_allow_html=True)
    st.markdown('<div class="caution"><strong>Interpretation guardrail</strong><br>This is an independent advisory case study using public retail-food data and simulated inventory mechanics. It is not based on Swiggy data. The expiry figures represent modelled cost exposure—not confirmed waste, realised loss or guaranteed savings.</div>', unsafe_allow_html=True)

elif page == "02 · Demand & Forecasts":
    kicker("Signal quality · Forecast reliability")
    st.title("A forecast is only useful if its error is understood")
    st.write("The current model uses a simple recent-average demand baseline. It is a useful starting point for a prototype, but the evaluation result signals that forecast error must be addressed before using the output to drive operational orders.")
    c1,c2,c3 = st.columns(3)
    with c1: kpi("Forecast horizon", "28 days", "Held-out period in the existing model")
    with c2: kpi("WAPE", f"{WAPE:.2f}%", "Substantial forecast error")
    with c3: kpi("Forecast rows", f"{len(forecast):,}", "Daily forecast output available" if not forecast.empty else "Forecast output not found")
    if not forecast.empty and "date" in forecast and "forecast_units_rounded" in forecast:
        d = forecast.copy(); d["date"] = pd.to_datetime(d["date"], errors="coerce")
        fig = px.line(d, x="date", y="forecast_units_rounded", markers=True, title="Daily forecast · 28-day horizon")
        fig.update_traces(line_color=TEAL, marker_color=ORANGE, line_width=3)
        st.plotly_chart(chart_style(fig, 360), use_container_width=True)
        st.dataframe(d.rename(columns={"date":"Date", "forecast_units":"Forecast units (unrounded)", "forecast_units_rounded":"Forecast units (rounded)"}), use_container_width=True, hide_index=True)
    else:
        st.info("Forecast summary CSV is not available in the outputs folder.")
    st.markdown('<div class="caution"><strong>Decision implication</strong><br>Do not translate this baseline directly into purchase orders. Compare against stronger seasonal / day-of-week baselines, measure errors by SKU and forecast horizon, and evaluate stockout and excess-inventory trade-offs.</div>', unsafe_allow_html=True)
    st.markdown("#### What would improve confidence?")
    st.markdown("- Benchmark against naïve, seasonal-naïve and day-of-week forecasts.\n- Segment performance by SKU velocity and demand volatility.\n- Evaluate bias as well as WAPE; aggregate accuracy can hide poor SKU-level performance.\n- Back-test ordering decisions, not only forecast metrics.")

elif page == "03 · Inventory & Expiry Risk":
    kicker("Inventory mechanics · Simulated exposure")
    st.title("Where could inventory value be exposed?")
    st.write("The simulation reconstructs stock batches, tracks remaining quantity and assumed expiry dates, then estimates what could remain unsold under a defined demand scenario.")
    a,b,c,d = st.columns(4)
    with a: kpi("Closing stock", f"{closing_units:,} units", "Simulated model-end inventory")
    with b: kpi("Closing stock cost", f"${closing_cost:,.0f}", "At assumed procurement cost")
    with c: kpi("Potentially unsold", f"{expiry_units:,} units", "Seven-day expiry scenario")
    with d: kpi("Expiry cost exposure", f"${expiry_cost:,.0f}", "Modelled, not realised waste")
    st.markdown('<div class="note"><strong>How to read this</strong><br>Cost exposure is a prompt to investigate—not automatically a loss. Some stock may sell, be transferred or be marked down. The model assumes a flat seven-day shelf life and simplified demand/replenishment mechanics.</div>', unsafe_allow_html=True)
    left,right = st.columns(2)
    with left:
        if not projected.empty and "projected_waste_units" in projected:
            v = projected.copy(); v["projected_waste_units"] = pd.to_numeric(v["projected_waste_units"], errors="coerce").fillna(0)
            top = v.groupby("item_id", as_index=False)["projected_waste_units"].sum().nlargest(12, "projected_waste_units").sort_values("projected_waste_units")
            fig = px.bar(top, x="projected_waste_units", y="item_id", orientation="h", title="Products with highest projected unsold units")
            fig.update_traces(marker_color=ORANGE)
            st.plotly_chart(chart_style(fig, 420), use_container_width=True)
    with right:
        if not closing.empty and "remaining_shelf_life_days" in closing and "remaining_qty" in closing:
            v = closing.copy(); v["remaining_shelf_life_days"] = pd.to_numeric(v["remaining_shelf_life_days"], errors="coerce"); v["remaining_qty"] = pd.to_numeric(v["remaining_qty"], errors="coerce").fillna(0)
            v = v.dropna(subset=["remaining_shelf_life_days"]).groupby("remaining_shelf_life_days", as_index=False)["remaining_qty"].sum()
            fig = px.bar(v, x="remaining_shelf_life_days", y="remaining_qty", title="Remaining units by assumed shelf life")
            fig.update_traces(marker_color=TEAL)
            st.plotly_chart(chart_style(fig, 420), use_container_width=True)
    with st.expander("Inspect product-level risk output"):
        if not risk.empty:
            st.dataframe(risk.sort_values("potential_waste_cost", ascending=False).head(100), use_container_width=True, hide_index=True)
            st.download_button("Download product risk CSV", risk.to_csv(index=False).encode("utf-8"), "sku_inventory_risk.csv", "text/csv")
        else: st.info("Product-level risk output is not available.")
    st.markdown('<div class="caution"><strong>Evidence boundary</strong><br>Underlying M5 data is US retail-food sales, not fresh-produce batches or any company’s operational records. Procurement cost, lead time, safety stock and shelf life are assumptions. The projection is not a measured waste rate.</div>', unsafe_allow_html=True)

elif page == "04 · F&V Scenario Lab":
    kicker("Interactive scenario · Editable assumptions")
    st.title("What if we changed the inventory decision?")
    st.write("Use this simplified produce scenario to explore how demand over the usable window compares with stock on hand, and how a markdown assumption changes the residual quantity at risk.")
    left,right = st.columns(2)
    with left:
        produce = st.selectbox("Produce example", ["Tomatoes 🍅", "Leafy greens 🥬", "Bananas 🍌", "Apples 🍎", "Bell peppers 🫑"])
        stock = st.number_input("Stock available (kg)", min_value=0.0, max_value=100000.0, value=100.0, step=5.0)
        demand = st.number_input("Expected sales per day (kg)", min_value=0.0, max_value=10000.0, value=15.0, step=1.0)
        days = st.number_input("Usable shelf life remaining (days)", min_value=1, max_value=30, value=4, step=1)
    with right:
        purchase = st.number_input("Purchase cost (₹/kg)", min_value=0.0, max_value=100000.0, value=40.0, step=5.0)
        selling = st.number_input("Regular selling price (₹/kg)", min_value=0.0, max_value=100000.0, value=60.0, step=5.0)
        markdown_share = st.slider("Share of excess sold via markdown (%)", 0, 100, 30, 5)
        discount = st.slider("Markdown discount (%)", 0, 80, 20, 5)
    capacity = demand * days
    excess = max(stock - capacity, 0.0)
    regular_qty = min(stock, capacity)
    markdown_qty = excess * markdown_share / 100
    remaining = max(excess - markdown_qty, 0)
    markdown_price = selling * (1 - discount / 100)
    markdown_revenue = markdown_qty * markdown_price
    regular_revenue = regular_qty * selling
    sold_cost = (regular_qty + markdown_qty) * purchase
    gross_profit = regular_revenue + markdown_revenue - sold_cost
    m1,m2,m3,m4 = st.columns(4)
    with m1: kpi("Demand capacity", f"{capacity:,.1f} kg", "Demand × remaining usable days")
    with m2: kpi("Potential excess", f"{excess:,.1f} kg", "Stock less demand capacity")
    with m3: kpi("Cost exposed before action", f"₹{excess*purchase:,.0f}", "Potential excess × purchase cost")
    with m4: kpi("Residual unsold", f"{remaining:,.1f} kg", "After assumed markdown sales")
    comp = pd.DataFrame({"Measure":["Stock available", "Demand capacity", "Potential excess", "Sold via markdown", "Residual unsold"], "Quantity (kg)":[stock, capacity, excess, markdown_qty, remaining]})
    fig = px.bar(comp, x="Measure", y="Quantity (kg)", title=f"Illustrative stock balance · {produce}", text_auto=".1f")
    fig.update_traces(marker_color=TEAL)
    st.plotly_chart(chart_style(fig, 340), use_container_width=True)
    a,b,c = st.columns(3)
    with a: st.markdown(f'<div class="panel"><h3>📦 Order less</h3><p>Compare future orders against the usable-window demand of <strong>{capacity:,.1f} kg</strong>, with a practical buffer for uncertainty.</p></div>', unsafe_allow_html=True)
    with b: st.markdown(f'<div class="panel"><h3>🏪 Transfer stock</h3><p>Test whether another location can sell the excess before its usable life runs out. Transfer costs and receiving-store demand matter.</p></div>', unsafe_allow_html=True)
    with c: st.markdown(f'<div class="panel"><h3>🏷️ Markdown</h3><p>Illustrative markdown revenue: <strong>₹{markdown_revenue:,.0f}</strong>. Simplified gross profit on sold units: <strong>₹{gross_profit:,.0f}</strong> before other costs.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="caution"><strong>Scenario, not forecast</strong><br>All values are editable assumptions, not actual produce records. This calculator excludes labour, packaging, logistics, platform costs, quality deterioration, demand variation and other operating costs. Markdown sell-through is assumed, not predicted.</div>', unsafe_allow_html=True)

elif page == "05 · Financial Impact":
    kicker("Commercial judgement · Scenario economics")
    st.title("Cost exposure is not the same as savings")
    st.write("A sound intervention case should estimate what value can actually be recovered after the costs and trade-offs of acting. Use the controls to explore an illustrative markdown / recovery case; replace assumptions with operational data before making a decision.")
    st.markdown("#### Scenario inputs")
    a,b,c = st.columns(3)
    with a: exposed_cost = st.number_input("Inventory cost exposure (₹)", min_value=0.0, value=100000.0, step=10000.0)
    with b: recovery = st.slider("Share of exposure recovered (%)", 0, 100, 25, 5)
    with c: intervention_cost = st.number_input("Intervention cost (₹)", min_value=0.0, value=8000.0, step=1000.0)
    d,e,f = st.columns(3)
    with d: discount_impact = st.number_input("Margin / markdown impact (₹)", min_value=0.0, value=5000.0, step=1000.0)
    with e: transfer_handling = st.number_input("Transfer / handling cost (₹)", min_value=0.0, value=2000.0, step=500.0)
    with f: stockout_risk_cost = st.number_input("Estimated availability trade-off cost (₹)", min_value=0.0, value=0.0, step=1000.0)
    recovered_value = exposed_cost * recovery / 100
    net = recovered_value - intervention_cost - discount_impact - transfer_handling - stockout_risk_cost
    x,y,z = st.columns(3)
    with x: kpi("Gross recovered value", f"₹{recovered_value:,.0f}", "Assumed share of inventory cost exposure")
    with y: kpi("Incremental costs & trade-offs", f"₹{intervention_cost+discount_impact+transfer_handling+stockout_risk_cost:,.0f}", "All scenario inputs are illustrative")
    with z: kpi("Illustrative net value", f"₹{net:,.0f}", "Not a validated business case")
    waterfall = pd.DataFrame({"Component":["Gross recovered value", "Intervention cost", "Markdown impact", "Transfer / handling", "Availability trade-off"], "Value (₹)":[recovered_value, -intervention_cost, -discount_impact, -transfer_handling, -stockout_risk_cost]})
    fig = px.bar(waterfall, x="Component", y="Value (₹)", title="Illustrative value bridge", text_auto=".0f", color="Value (₹)", color_continuous_scale=["#D87945", "#E9EFEA", TEAL])
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(chart_style(fig, 350), use_container_width=True)
    st.markdown('<div class="note"><strong>Finance principle</strong><br>Use contribution after variable costs—not revenue—as the benefit measure. Avoid double-counting recovered inventory value and margin on the same units. Confirm whether reduced waste creates cash savings, margin recovery or only capacity / working-capital benefits.</div>', unsafe_allow_html=True)
    st.markdown("#### Minimum data required for a real business case")
    st.markdown("- Actual purchase cost and realised selling price by SKU / batch.\n- Actual waste, markdown, transfer and stockout records.\n- Demand and inventory snapshots with timestamp and usable life.\n- Incremental variable costs and contribution margin.\n- A comparable baseline or pilot/control design to estimate incremental impact.")

else:
    kicker("Decision memo · Evidence and next steps")
    st.title("What should management do next?")
    st.write("The current work is best treated as a diagnostic prototype. It demonstrates how data can connect demand, inventory and finance, but a pilot should be designed to test whether decisions improve in a real operating environment.")
    st.markdown("### Recommended next steps")
    steps = [
        ("1 · Improve the demand signal", "Benchmark stronger forecast baselines; evaluate SKU-level bias and error before translating forecasts into orders."),
        ("2 · Validate inventory mechanics", "Replace flat shelf-life and procurement-cost assumptions with product- and supplier-specific records."),
        ("3 · Select a narrow pilot", "Choose a manageable group of stores / products with reliable waste, stockout and cost data."),
        ("4 · Test an intervention", "Compare order rules, transfers or markdown timing against a baseline; measure both availability and financial outcomes."),
        ("5 · Reconcile realised impact", "Track waste, stockouts, contribution, markdown recovery and operational costs. Do not count scenario outputs as savings."),
    ]
    for title, body in steps:
        st.markdown(f'<div class="panel" style="margin-bottom:10px;"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
    st.markdown("### Evidence register")
    evidence = pd.DataFrame([
        ("M5 US retail-food sales", "Demand baseline and inventory simulation", "Public dataset; not fresh-produce or company data"),
        ("FreshRetailNet audit notebook", "Dataset-level stockout/availability exploration", "4.5M training rows; 898 stores; 865 products; 18 cities; category IDs are not named labels"),
        ("Inventory outputs", "Batch tracking and projected expiry exposure", "Simulated assumptions; reconciliation checks passed in project notes"),
        ("F&V Scenario Lab", "Editable decision scenario", "Illustrative assumptions; not a prediction or observed outcome"),
    ], columns=["Evidence source", "Used for", "Interpretation / limitation"])
    st.dataframe(evidence, use_container_width=True, hide_index=True)
    st.markdown('<div class="caution"><strong>Conclusion</strong><br>Proceed to data validation and a controlled pilot design—not immediate rollout. Current evidence supports an analytical approach and a set of testable hypotheses; it does not establish company-specific loss, preventable waste or guaranteed savings.</div>', unsafe_allow_html=True)

st.divider()
st.caption("FreshMargin · Independent portfolio case study · Public data + simulated inventory mechanics · Prepared by Harshana, MBA Finance, IMT Ghaziabad")
