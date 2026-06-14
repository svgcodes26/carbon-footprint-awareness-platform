import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import requests

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EcoTrack – Carbon Footprint Platform",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global dark background ── */
    .stApp {
        background: #0d1117 !important;
        color: #e6edf3 !important;
    }
    .main .block-container {
        background: #0d1117 !important;
        padding-top: 2rem;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    section[data-testid="stSidebar"] * {
        color: #e6edf3 !important;
    }

    /* ── All text ── */
    p, span, label, div, li { color: #e6edf3 !important; }
    h1 { color: #39d353 !important; font-size: 2.2em !important; }
    h2 { color: #39d353 !important; }
    h3 { color: #7ee787 !important; }

    /* ── Metric cards ── */
    .metric-card {
        background: #161b22;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #30363d;
        border-left: 4px solid #39d353;
        margin: 8px 0;
        color: #e6edf3 !important;
    }
    .metric-card h2, .metric-card h3, .metric-card p {
        color: #e6edf3 !important;
    }

    /* ── Tip cards ── */
    .tip-card {
        background: #1c2128;
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid #39d353;
        border: 1px solid #30363d;
    }
    .tip-card p { color: #c9d1d9 !important; }

    /* ── AI response card ── */
    .ai-response {
        background: #1c2128;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #58a6ff;
        border: 1px solid #30363d;
    }
    .ai-response h3 { color: #58a6ff !important; }
    .ai-response p { color: #c9d1d9 !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2ea043, #39d353) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(57, 211, 83, 0.3) !important;
    }

    /* ── Input fields ── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: #21262d !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }

    /* ── Selectbox dropdown ── */
    .stSelectbox [data-baseweb="select"] > div {
        background: #21262d !important;
        border-color: #30363d !important;
        color: #e6edf3 !important;
    }

    /* ── Metrics ── */
    [data-testid="stMetricValue"] {
        color: #39d353 !important;
        font-size: 1.6em !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] { color: #8b949e !important; }
    [data-testid="stMetricDelta"] { font-size: 0.85em !important; }

    /* ── Dataframe ── */
    .stDataFrame { border: 1px solid #30363d !important; border-radius: 8px; }
    iframe { background: #161b22 !important; }

    /* ── Divider ── */
    hr { border-color: #30363d !important; }

    /* ── Radio buttons ── */
    .stRadio label { color: #c9d1d9 !important; }
    .stRadio [data-baseweb="radio"] { accent-color: #39d353; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: #161b22 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        background: #0d1117 !important;
        border: 1px solid #30363d !important;
    }

    /* ── Info/warning boxes ── */
    .stAlert { background: #1c2128 !important; border-radius: 8px !important; }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #39d353 !important; }

    /* ── Caption / small text ── */
    .stCaption, small { color: #8b949e !important; }

    /* ── Success message ── */
    .stSuccess { background: #1c2128 !important; border-left: 4px solid #39d353 !important; }
    .stWarning { background: #1c2128 !important; border-left: 4px solid #d29922 !important; }
    .stInfo    { background: #1c2128 !important; border-left: 4px solid #58a6ff !important; }

    /* ── Number input buttons ── */
    .stNumberInput button {
        background: #21262d !important;
        color: #e6edf3 !important;
        border-color: #30363d !important;
    }

    /* ── Date input ── */
    .stDateInput input {
        background: #21262d !important;
        color: #e6edf3 !important;
        border-color: #30363d !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #39d353; }
</style>
""", unsafe_allow_html=True)

# ── Session State Init ────────────────────────────────────────────────────────
if "activities" not in st.session_state:
    st.session_state.activities = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Eco Warrior"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Emission Factors (kg CO₂e per unit) ──────────────────────────────────────
EMISSION_FACTORS = {
    "Transport": {
        "Car (Petrol) – per km":    0.21,
        "Car (Diesel) – per km":    0.17,
        "Car (Electric) – per km":  0.05,
        "Bus – per km":             0.089,
        "Train – per km":           0.041,
        "Flight (Domestic) – per km": 0.255,
        "Flight (International) – per km": 0.195,
        "Motorbike – per km":       0.114,
        "Bicycle / Walking":        0.0,
    },
    "Food": {
        "Beef meal":        6.61,
        "Pork meal":        2.42,
        "Chicken meal":     1.02,
        "Fish meal":        1.34,
        "Vegetarian meal":  0.50,
        "Vegan meal":       0.35,
        "Dairy (1 glass milk)": 0.63,
        "Cheese (100 g)":   1.32,
        "Eggs (1 egg)":     0.20,
    },
    "Home Energy": {
        "Electricity (kWh)": 0.82,
        "Natural Gas (kWh)": 0.20,
        "LPG (kg)":          2.98,
        "Coal (kg)":         2.42,
        "Solar/Renewable":   0.0,
    },
    "Shopping & Waste": {
        "New clothing item":         10.0,
        "Electronics (smartphone)": 70.0,
        "Electronics (laptop)":    300.0,
        "Plastic bag":               0.01,
        "Recycled 1 kg waste":      -0.21,
        "Composting 1 kg":          -0.10,
    }
}

TIPS_DB = {
    "Transport": [
        "🚴 Switch to cycling or walking for trips under 5 km — saves ~1 kg CO₂ per trip.",
        "🚌 Use public transport instead of a petrol car — cuts emissions by ~58%.",
        "⚡ Consider an electric vehicle — 76% lower emissions than petrol cars.",
        "✈️ Opt for train over domestic flights — 6x lower carbon footprint.",
        "🚗 Carpool with colleagues — halves your transport emissions.",
    ],
    "Food": [
        "🥗 One vegan day/week saves ~0.9 tonnes CO₂ per year.",
        "🍗 Replace beef with chicken — 6x lower emissions per meal.",
        "🥦 Buy local & seasonal produce — reduces food transport emissions.",
        "🍱 Reduce food waste — 8% of global emissions come from wasted food.",
        "🌱 Try plant-based proteins (lentils, beans) — nearly zero emissions.",
    ],
    "Home Energy": [
        "💡 Switch to LED bulbs — uses 75% less energy than incandescent.",
        "🌡️ Lower thermostat by 1°C — saves ~3% on heating bills & emissions.",
        "☀️ Install solar panels — eliminates home electricity emissions.",
        "🔌 Unplug devices on standby — saves ~10% on electricity.",
        "🪟 Improve home insulation — reduces heating/cooling needs by 25%.",
    ],
    "Shopping & Waste": [
        "♻️ Recycle consistently — saves 1 tonne CO₂ per year for a family.",
        "👕 Buy second-hand clothing — fashion is 10% of global emissions.",
        "📱 Keep your phone 1 extra year — avoids 70 kg CO₂ in manufacturing.",
        "🛍️ Use reusable bags — eliminates plastic waste emissions.",
        "🌿 Compost food scraps — diverts methane from landfills.",
    ],
}

GLOBAL_AVG_KG_PER_DAY = 13.0  # ~4.7 tonnes/year global average


# ── Helper Functions ──────────────────────────────────────────────────────────
@st.cache_data
def get_emission_factors():
    """Cache emission factors for efficiency."""
    return EMISSION_FACTORS

@st.cache_data
def get_tips_db():
    """Cache tips database for efficiency."""
    return TIPS_DB

@st.cache_data
def calculate_emissions(category: str, activity: str, quantity: float) -> float:
    """
    Calculate CO2 emissions for a given activity.
    
    Args:
        category: Activity category (Transport, Food, etc.)
        activity: Specific activity name
        quantity: Amount/quantity of the activity
    
    Returns:
        Emissions in kg CO2e, rounded to 3 decimal places
    """
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    factor = EMISSION_FACTORS.get(category, {}).get(activity, 0)
    return round(factor * quantity, 3)

@st.cache_data
def get_daily_summary(activities: tuple) -> pd.DataFrame:
    """Cache and compute daily summary from activities."""
    if not activities:
        return pd.DataFrame()
    df = pd.DataFrame(list(activities))
    df["date"] = pd.to_datetime(df["date"])
    return df.groupby("date")["emissions"].sum().reset_index()

@st.cache_data
def get_category_summary(activities: tuple) -> pd.DataFrame:
    """Cache and compute category breakdown."""
    if not activities:
        return pd.DataFrame()
    df = pd.DataFrame(list(activities))
    return df.groupby("category")["emissions"].sum().reset_index()

def get_badge(total_kg: float) -> tuple:
    """Return badge name and color based on emissions."""
    if total_kg <= 3:    return ("🌟 Eco Hero", "#39d353")
    elif total_kg <= 7:  return ("🌿 Green Warrior", "#7ee787")
    elif total_kg <= 13: return ("🌱 Earth Aware", "#e3b341")
    elif total_kg <= 20: return ("⚡ Taking Action", "#f0883e")
    else:                return ("🔥 High Impact", "#f85149")

def get_ai_suggestions(user_data_summary: str) -> str:
    """Call Claude API for personalized AI suggestions."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    
    system_prompt = """You are EcoAdvisor, an expert carbon footprint coach. 
    Analyze the user's activity data and give 4-5 specific, actionable, personalized suggestions 
    to reduce their carbon footprint. Be encouraging, practical, and mention estimated CO₂ savings.
    Format with emojis. Keep each tip concise (1-2 sentences). End with an encouraging closing line."""
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 600,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_data_summary}]
    }
    try:
        r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=20)
        data = r.json()
        return data["content"][0]["text"]
    except Exception as e:
        return f"⚠️ AI suggestions unavailable right now. Please check your API key. Error: {e}"

def get_ai_chat(question: str, context: str) -> str:
    """Chat with EcoAdvisor AI."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    system_prompt = """You are EcoAdvisor, a friendly and knowledgeable carbon footprint assistant.
    Help users understand their environmental impact and give practical advice.
    Be conversational, supportive, and always relate answers to carbon emissions where relevant.
    Keep responses concise (3-4 sentences max)."""
    
    messages = st.session_state.chat_history.copy()
    messages.append({"role": "user", "content": f"User context: {context}\n\nQuestion: {question}"})
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 400,
        "system": system_prompt,
        "messages": messages
    }
    try:
        r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=20)
        data = r.json()
        reply = data["content"][0]["text"]
        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"⚠️ AI chat unavailable. Error: {e}"



def co2_gauge(value, max_val=30):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        delta={"reference": GLOBAL_AVG_KG_PER_DAY, "suffix": " kg"},
        number={"suffix": " kg CO₂"},
        title={"text": "Today's Footprint vs Global Avg"},
        gauge={
            "axis": {"range": [0, max_val]},
            "bar": {"color": "#2e7d32"},
            "steps": [
                {"range": [0, 7],  "color": "#c8e6c9"},
                {"range": [7, 13], "color": "#fff9c4"},
                {"range": [13, 30],"color": "#ffcdd2"},
            ],
            "threshold": {
                "line": {"color": "#e53935", "width": 3},
                "thickness": 0.75,
                "value": GLOBAL_AVG_KG_PER_DAY
            }
        }
    ))
    fig.update_layout(height=280, margin=dict(t=30, b=0, l=20, r=20),
                      paper_bgcolor="#0d1117", font_color="#e6edf3",
                      font=dict(color="#e6edf3"))
    return fig


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/leaf.png", width=60)
    st.title("🌿 EcoTrack")
    st.caption("Carbon Footprint Awareness Platform")
    st.divider()
    
    st.session_state.user_name = st.text_input("👤 Your Name", value=st.session_state.user_name)
    
    st.divider()
    page = st.radio("📌 Navigate", [
        "🏠 Dashboard",
        "📊 Carbon Calculator",
        "📅 Activity Tracker",
        "💡 Tips & Insights",
        "🤖 AI EcoAdvisor",
        "💬 Chat with EcoAI"
    ])
    
    st.divider()
    api_key_input = st.text_input("🔑 Anthropic API Key (for AI features)", type="password",
                                   help="Enter your Anthropic API key to enable AI suggestions")
    if api_key_input:
        os.environ["ANTHROPIC_API_KEY"] = api_key_input
        st.success("✅ API Key set!")
    
    st.divider()
    st.markdown("**🌍 Global Stats**")
    st.metric("Avg CO₂/person/day", "13 kg")
    st.metric("Safe limit/day", "< 7 kg")


# ── Compute totals ─────────────────────────────────────────────────────────────
total_today = sum(a["emissions"] for a in st.session_state.activities
                  if a.get("date") == datetime.now().strftime("%Y-%m-%d"))
total_all = sum(a["emissions"] for a in st.session_state.activities)
badge, badge_color = get_badge(total_today)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.title(f"🌿 Welcome back, {st.session_state.user_name}!")
    st.markdown("##### Your personal carbon footprint dashboard — track, learn, and reduce.")
    st.divider()

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌡️ Today's Footprint", f"{total_today:.2f} kg CO₂",
                  delta=f"{total_today - GLOBAL_AVG_KG_PER_DAY:.2f} vs global avg",
                  delta_color="inverse")
    with col2:
        st.metric("📅 Total Logged", f"{total_all:.2f} kg CO₂",
                  f"{len(st.session_state.activities)} activities")
    with col3:
        saved = max(0, GLOBAL_AVG_KG_PER_DAY - total_today)
        st.metric("💚 CO₂ Saved Today", f"{saved:.2f} kg",
                  "vs global average" if saved > 0 else "Above average")
    with col4:
        equiv_trees = round(total_all / 21.77, 1)
        st.metric("🌳 Trees Needed", f"{equiv_trees}",
                  "to offset your emissions")

    st.divider()
    col_g, col_b = st.columns([2, 1])
    with col_g:
        st.plotly_chart(co2_gauge(total_today), use_container_width=True)
    with col_b:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style="color:{badge_color}; font-size:2em;">{badge}</h2>
            <p style="color:#8b949e;">Based on today's activities</p>
            <hr style="border-color:#30363d;">
            <p style="color:#e6edf3;">🌍 Global avg: <b>13 kg/day</b></p>
            <p style="color:#e6edf3;">🎯 Your target: <b>&lt; 7 kg/day</b></p>
            <p style="color:#e6edf3;">📈 Your today: <b>{total_today:.2f} kg</b></p>
        </div>
        """, unsafe_allow_html=True)

    # Recent Activities
    if st.session_state.activities:
        st.subheader("📋 Recent Activities")
        df = pd.DataFrame(st.session_state.activities[-5:][::-1])
        df = df[["date", "category", "activity", "quantity", "unit", "emissions"]]
        df.columns = ["Date", "Category", "Activity", "Quantity", "Unit", "CO₂ (kg)"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("👆 Start by logging activities in the **Carbon Calculator** or **Activity Tracker** tab!")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CARBON CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Carbon Calculator":
    st.title("📊 Carbon Footprint Calculator")
    st.markdown("Calculate the CO₂ emissions from your daily activities.")
    st.divider()

    col1, col2 = st.columns([1, 1])
    with col1:
        category = st.selectbox("🗂️ Category", list(EMISSION_FACTORS.keys()))
        activity = st.selectbox("⚡ Activity", list(EMISSION_FACTORS[category].keys()))
        
        factor = EMISSION_FACTORS[category][activity]
        unit_map = {
            "Transport": "km", "Food": "meals/servings",
            "Home Energy": "units (kWh/kg)", "Shopping & Waste": "items/kg"
        }
        unit = unit_map.get(category, "units")
        quantity = st.number_input(f"📏 Quantity ({unit})", min_value=0.0, value=1.0, step=0.5)
        date_sel = st.date_input("📅 Date", value=datetime.now())
        
        emissions = calculate_emissions(category, activity, quantity)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌡️ Estimated Emissions</h3>
            <h2 style="color:#2e7d32; font-size:2.5em;">{emissions:.3f} <span style="font-size:0.5em;">kg CO₂e</span></h2>
            <p>📊 Emission factor: {factor} kg CO₂e per {unit}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➕ Log This Activity", use_container_width=True):
            st.session_state.activities.append({
                "date": date_sel.strftime("%Y-%m-%d"),
                "category": category,
                "activity": activity,
                "quantity": quantity,
                "unit": unit,
                "emissions": emissions
            })
            st.success(f"✅ Logged {emissions:.3f} kg CO₂ for {activity}!")
            st.balloons()

    with col2:
        st.subheader("⚖️ Compare Activities")
        if category in EMISSION_FACTORS:
            acts = list(EMISSION_FACTORS[category].keys())
            factors = [EMISSION_FACTORS[category][a] for a in acts]
            df_compare = pd.DataFrame({"Activity": acts, "kg CO₂e per unit": factors})
            df_compare = df_compare.sort_values("kg CO₂e per unit", ascending=True)
            
            fig = px.bar(df_compare, x="kg CO₂e per unit", y="Activity",
                        orientation='h', color="kg CO₂e per unit",
                        color_continuous_scale=["#c8e6c9", "#ff8f00", "#b71c1c"],
                        title=f"CO₂ Comparison: {category}")
            fig.update_layout(height=400, paper_bgcolor="#0d1117",
                             plot_bgcolor="rgba(0,0,0,0)",
                             coloraxis_showscale=False)
            fig.update_xaxes(showgrid=True, gridcolor="#e8f5e9")
            st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ACTIVITY TRACKER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📅 Activity Tracker":
    st.title("📅 Daily Activity Tracker")
    st.markdown("Track your carbon footprint over time and spot trends.")
    st.divider()

    if not st.session_state.activities:
        st.info("No activities logged yet. Use the **Carbon Calculator** to add activities!")
    else:
        df = pd.DataFrame(st.session_state.activities)
        df["date"] = pd.to_datetime(df["date"])

        # Daily trend chart
        daily = df.groupby("date")["emissions"].sum().reset_index()
        daily.columns = ["Date", "Total CO₂ (kg)"]
        
        fig_trend = px.line(daily, x="Date", y="Total CO₂ (kg)",
                           title="📈 Daily Carbon Footprint Trend",
                           markers=True, line_shape="spline",
                           color_discrete_sequence=["#2e7d32"])
        fig_trend.add_hline(y=GLOBAL_AVG_KG_PER_DAY, line_dash="dash",
                           line_color="red", annotation_text="Global Avg (13 kg)")
        fig_trend.add_hline(y=7, line_dash="dot",
                           line_color="green", annotation_text="Target (7 kg)")
        fig_trend.update_layout(paper_bgcolor="#0d1117",
                               plot_bgcolor="rgba(245,255,245,0.5)")
        st.plotly_chart(fig_trend, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            # Category breakdown pie
            cat_data = df.groupby("category")["emissions"].sum().reset_index()
            fig_pie = px.pie(cat_data, values="emissions", names="category",
                            title="🥧 Emissions by Category",
                            color_discrete_sequence=px.colors.sequential.Greens_r)
            fig_pie.update_layout(paper_bgcolor="#0d1117")
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Top emitting activities
            top_acts = df.groupby("activity")["emissions"].sum().nlargest(8).reset_index()
            fig_top = px.bar(top_acts, x="emissions", y="activity", orientation='h',
                            title="🏆 Top Emitting Activities",
                            color="emissions",
                            color_continuous_scale=["#c8e6c9", "#ff8f00", "#b71c1c"])
            fig_top.update_layout(paper_bgcolor="#0d1117",
                                 plot_bgcolor="rgba(0,0,0,0)",
                                 coloraxis_showscale=False)
            st.plotly_chart(fig_top, use_container_width=True)

        # Full log table
        st.subheader("📋 Activity Log")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            cats = ["All"] + list(df["category"].unique())
            filter_cat = st.selectbox("Filter by Category", cats)
        with col_b:
            date_from = st.date_input("From", value=df["date"].min())
        with col_c:
            date_to = st.date_input("To", value=df["date"].max())

        filtered = df.copy()
        if filter_cat != "All":
            filtered = filtered[filtered["category"] == filter_cat]
        filtered = filtered[(filtered["date"] >= pd.Timestamp(date_from)) &
                           (filtered["date"] <= pd.Timestamp(date_to))]

        display_df = filtered[["date","category","activity","quantity","unit","emissions"]].copy()
        display_df.columns = ["Date","Category","Activity","Quantity","Unit","CO₂ (kg)"]
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        if st.button("🗑️ Clear All Activities", type="secondary"):
            st.session_state.activities = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TIPS & INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💡 Tips & Insights":
    st.title("💡 Eco Tips & Personalized Insights")
    st.markdown("Practical actions to reduce your carbon footprint.")
    st.divider()

    # Personalized insights from logged data
    if st.session_state.activities:
        df = pd.DataFrame(st.session_state.activities)
        top_cat = df.groupby("category")["emissions"].sum().idxmax()
        top_val = df.groupby("category")["emissions"].sum().max()
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Personalized Insight</h3>
            <p>Your highest emission category is <b>{top_cat}</b> at <b>{top_val:.2f} kg CO₂</b>.</p>
            <p>Focus on the <b>{top_cat}</b> tips below to make the biggest impact! 🌍</p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

    # Tips by category
    for cat, tips in TIPS_DB.items():
        with st.expander(f"{'🚗' if cat=='Transport' else '🍽️' if cat=='Food' else '🏠' if cat=='Home Energy' else '🛍️'} {cat} Tips", expanded=(cat=="Transport")):
            for tip in tips:
                st.markdown(f"""
                <div class="tip-card">
                    <p style="margin:0; font-size:0.95em;">{tip}</p>
                </div>
                """, unsafe_allow_html=True)

    st.divider()
    st.subheader("📊 Impact Comparison")
    
    comparisons = {
        "Action": ["Go vegan for 1 month", "Drive 50% less", "Switch to LED bulbs",
                   "Take train vs flight", "Buy nothing new for 1 month", "Recycle consistently"],
        "CO₂ Saved (kg/month)": [75, 60, 10, 120, 40, 15],
        "Difficulty": ["Medium", "Hard", "Easy", "Medium", "Hard", "Easy"]
    }
    df_comp = pd.DataFrame(comparisons)
    fig = px.bar(df_comp, x="CO₂ Saved (kg/month)", y="Action", orientation='h',
                color="Difficulty",
                color_discrete_map={"Easy": "#4caf50", "Medium": "#ff9800", "Hard": "#f44336"},
                title="🌱 Monthly CO₂ Savings by Action")
    fig.update_layout(paper_bgcolor="#0d1117", plot_bgcolor="#161b22")
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AI ECOADVISOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 AI EcoAdvisor":
    st.title("🤖 AI EcoAdvisor")
    st.markdown("Get personalized AI-powered suggestions based on your carbon footprint data.")
    st.divider()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        st.warning("⚠️ Please enter your Anthropic API Key in the sidebar to use AI features.")
    
    if st.session_state.activities:
        df = pd.DataFrame(st.session_state.activities)
        summary_stats = df.groupby("category")["emissions"].sum().to_dict()
        top_activities = df.nlargest(5, "emissions")[["category","activity","emissions"]].to_string(index=False)
        
        user_summary = f"""
        User: {st.session_state.user_name}
        Total logged emissions: {total_all:.2f} kg CO₂
        Today's emissions: {total_today:.2f} kg CO₂ (global avg: 13 kg)
        Emissions by category: {summary_stats}
        Top 5 emitting activities:
        {top_activities}
        Number of activities logged: {len(st.session_state.activities)}
        """
        
        st.subheader(f"📊 Your Emission Summary")
        cols = st.columns(len(summary_stats))
        for i, (cat, val) in enumerate(summary_stats.items()):
            with cols[i]:
                st.metric(cat, f"{val:.1f} kg")
        
        st.divider()
        if st.button("🤖 Generate AI Suggestions", use_container_width=True, type="primary"):
            with st.spinner("🌿 EcoAdvisor is analyzing your data..."):
                suggestions = get_ai_suggestions(user_summary)
            st.markdown(f"""
            <div class="ai-response">
                <h3>🌟 Personalized Recommendations for {st.session_state.user_name}</h3>
                <p>{suggestions.replace(chr(10), '<br>')}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📝 Log some activities first to get personalized AI suggestions!")
        st.markdown("""
        **What EcoAdvisor can do:**
        - 🎯 Analyze your biggest emission sources
        - 💡 Give specific, actionable reduction tips
        - 📊 Estimate CO₂ savings from each action
        - 🏆 Help you reach your carbon goals
        """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AI CHAT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💬 Chat with EcoAI":
    st.title("💬 Chat with EcoAdvisor")
    st.markdown("Ask anything about carbon footprint, sustainability, and eco-living!")
    st.divider()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        st.warning("⚠️ Please enter your Anthropic API Key in the sidebar to use AI chat.")

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🌿"):
                st.write(msg["content"])

    # Quick question buttons
    if not st.session_state.chat_history:
        st.markdown("**💡 Quick Questions:**")
        q_cols = st.columns(2)
        quick_qs = [
            "What is carbon footprint?",
            "How can I reduce food emissions?",
            "Is electric car really greener?",
            "What's the easiest eco change I can make?"
        ]
        for i, q in enumerate(quick_qs):
            with q_cols[i % 2]:
                if st.button(q, use_container_width=True):
                    context = f"User has logged {len(st.session_state.activities)} activities, total {total_all:.1f} kg CO₂"
                    with st.spinner("🌿 EcoAdvisor is thinking..."):
                        reply = get_ai_chat(q, context)
                    st.rerun()

    # Chat input
    user_input = st.chat_input("Ask EcoAdvisor anything about sustainability...")
    if user_input:
        context = f"User '{st.session_state.user_name}' has logged {len(st.session_state.activities)} activities, total emissions: {total_all:.1f} kg CO₂, today: {total_today:.1f} kg CO₂"
        with st.spinner("🌿 EcoAdvisor is thinking..."):
            reply = get_ai_chat(user_input, context)
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center; color:#558b2f; font-size:0.85em;">
    🌿 EcoTrack – Carbon Footprint Awareness Platform | Built for Hack2Skill Challenge 3<br>
    🌍 Together we can reduce global emissions, one action at a time.
</div>
""", unsafe_allow_html=True)
