import streamlit as st
import anthropic
import pandas as pd
import plotly.express as px
import os

# ── Page configuration ───────────────────────────────────────────
st.set_page_config(
    page_title="AI BI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Custom CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        text-align: center;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E293B;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-delta {
        font-size: 0.9rem;
        color: #16A34A;
        font-weight: 600;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────
st.markdown("""
<div style="background:#1E293B; padding:1rem 2rem; margin:-1rem -1rem 2rem -1rem;">
    <h1 style="color:white; margin:0; font-size:1.5rem; font-weight:600;">
        📊 AI BI Dashboard
    </h1>
    <p style="color:#94A3B8; margin:0.25rem 0 0 0; font-size:0.85rem;">
        Powered by Claude AI — insights update automatically
    </p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  DATA LOADING
# ════════════════════════════════════════════════════════════════

@st.cache_data
def load_data(file_path):
    # @st.cache_data means pandas only reads the file once
    # If the file hasn't changed, Streamlit uses the cached version
    # This makes the dashboard much faster on reruns
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%b %Y')
    df['Week'] = df['Date'].dt.isocalendar().week
    return df

# ── File uploader ─────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload your sales CSV",
    type=["csv"],
    help="Upload a CSV with Date, Product, Region, Units_Sold, Revenue, Returns columns"
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%b %Y')
else:
    # Load default sample data if no file uploaded
    default_path = "sales_data.csv"
    if os.path.exists(default_path):
        df = load_data(default_path)
        st.info("Using sample sales data — upload your own CSV to analyse your data")
    else:
        st.error("No data found. Please upload a CSV file.")
        st.stop()

# ════════════════════════════════════════════════════════════════
#  KPI CALCULATIONS
# ════════════════════════════════════════════════════════════════

def calculate_kpis(df):
    total_revenue = df['Revenue'].sum()
    total_units = df['Units_Sold'].sum()
    total_returns = df['Returns'].sum()
    return_rate = (total_returns / total_units * 100).round(1)
    top_product = df.groupby('Product')['Revenue'].sum().idxmax()
    top_region = df.groupby('Region')['Revenue'].sum().idxmax()

    return {
        'total_revenue': total_revenue,
        'total_units': total_units,
        'total_returns': total_returns,
        'return_rate': return_rate,
        'top_product': top_product,
        'top_region': top_region
    }

kpis = calculate_kpis(df)

# ════════════════════════════════════════════════════════════════
#  KPI CARDS
# ════════════════════════════════════════════════════════════════

st.markdown("### Key Metrics")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">${kpis['total_revenue']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Units Sold</div>
        <div class="kpi-value">{kpis['total_units']:,}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Return Rate</div>
        <div class="kpi-value">{kpis['return_rate']}%</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Top Region</div>
        <div class="kpi-value">{kpis['top_region']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  CHARTS
# ════════════════════════════════════════════════════════════════

st.markdown("### Sales Analysis")
chart1, chart2 = st.columns(2)

with chart1:
    # Revenue by Product — bar chart
    product_revenue = df.groupby('Product')['Revenue'].sum().reset_index()
    product_revenue = product_revenue.sort_values('Revenue', ascending=False)

    fig1 = px.bar(
        product_revenue,
        x='Product',
        y='Revenue',
        title='Revenue by Product',
        color='Product',
        color_discrete_map={
            'Laptop': '#2563EB',
            'Phone': '#7C3AED',
            'Tablet': '#16A34A'
        }
    )
    fig1.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        title_font_size=14,
        title_font_color='#1E293B',
        xaxis_title='',
        yaxis_title='Revenue ($)',
        margin=dict(t=40, b=20, l=20, r=20),
        xaxis=dict(tickfont=dict(color='#1E293B', size=12)),
        yaxis=dict(tickfont=dict(color='#1E293B', size=12),title_font=dict(color='#1E293B', size=12))
    )
    st.plotly_chart(fig1, use_container_width=True)

with chart2:
    # Units sold by Region — bar chart
    region_units = df.groupby('Region')['Units_Sold'].sum().reset_index()
    region_units = region_units.sort_values('Units_Sold', ascending=False)

    fig2 = px.bar(
        region_units,
        x='Region',
        y='Units_Sold',
        title='Units Sold by Region',
        color='Region',
        color_discrete_sequence=['#2563EB', '#7C3AED', '#16A34A', '#F59E0B']
    )
    fig2.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        title_font_size=14,
        title_font_color='#1E293B',
        xaxis_title='',
        yaxis_title='Units Sold',
        margin=dict(t=40, b=20, l=20, r=20),
        xaxis=dict(tickfont=dict(color='#1E293B', size=12)),
        yaxis=dict(tickfont=dict(color='#1E293B', size=12),title_font=dict(color='#1E293B', size=12))
    )
    st.plotly_chart(fig2, use_container_width=True)

# Revenue over time — line chart
st.markdown("### Revenue Over Time")
df['DateOnly'] = df['Date'].dt.strftime('%b %d')
daily_revenue = df.groupby('DateOnly')['Revenue'].sum().reset_index()
daily_revenue.columns = ['Date', 'Revenue']

# Convert date to string so Plotly treats it as category not datetime
#daily_revenue['Date'] = daily_revenue['Date'].astype(str)

fig3 = px.line(
    daily_revenue,
    x='Date',
    y='Revenue',
    title='Daily Revenue Trend',
    markers=True
)
fig3.update_traces(
    line_color='#2563EB',
    marker_color='#2563EB',
    marker_size=8
)
fig3.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title_font_size=14,
    title_font_color='#1E293B',
    xaxis_title='',
    yaxis_title='Revenue ($)',
    margin=dict(t=40, b=20, l=20, r=20),
    xaxis=dict(tickfont=dict(color='#1E293B', size=12)),
    yaxis=dict(tickfont=dict(color='#1E293B', size=12),title_font=dict(color='#1E293B', size=12))
)
st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════
#  AI NARRATIVE + ANOMALY DETECTION
# ════════════════════════════════════════════════════════════════

st.markdown("### AI Analysis")
ai_left, ai_right = st.columns(2)

def build_data_summary(df, kpis):
    # Build a concise summary for Claude
    # Privacy first — aggregated stats only
    summary = f"""
Sales Dashboard Summary:
- Total Revenue: ${kpis['total_revenue']:,.0f}
- Total Units Sold: {kpis['total_units']:,}
- Return Rate: {kpis['return_rate']}%
- Top Product by Revenue: {kpis['top_product']}
- Top Region by Revenue: {kpis['top_region']}

Revenue by Product:
{df.groupby('Product')['Revenue'].sum().to_string()}

Units Sold by Region:
{df.groupby('Region')['Units_Sold'].sum().to_string()}

Daily Revenue:
{df.groupby('Date')['Revenue'].sum().to_string()}

Returns by Product:
{df.groupby('Product')['Returns'].sum().to_string()}
"""
    return summary

def generate_narrative(summary):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system="""You are a senior business analyst writing an executive dashboard narrative.
Write 3-4 sentences summarising the key story this data tells.
Be specific with numbers. Write for a business leader, not a data analyst.
Focus on what matters most and what action it implies.
Do not use bullet points — write in flowing prose.""",
        messages=[
            {"role": "user", "content": f"Write a narrative summary for this dashboard:\n\n{summary}"}
        ]
    )
    return message.content[0].text

def detect_anomalies(summary):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system="""You are a data quality and anomaly detection specialist.
Analyse the data summary and identify anything unusual, unexpected, or worth investigating.
Format each anomaly exactly like this:
[FLAG] <short title>: <one sentence explanation and recommended action>

If nothing unusual is found, say: No anomalies detected — data looks healthy.
Be specific with numbers. Maximum 4 flags.""",
        messages=[
            {"role": "user", "content": f"Detect anomalies in this data:\n\n{summary}"}
        ]
    )
    return message.content[0].text

summary = build_data_summary(df, kpis)

with ai_left:
    st.markdown("**Executive Summary**")
    if st.button("Generate Narrative", type="primary"):
        with st.spinner("Claude is writing your narrative..."):
            narrative = generate_narrative(summary)
        st.markdown(f"""
        <div style="background:white; padding:1.5rem; border-radius:12px;
        border:1px solid #E2E8F0; line-height:1.7; color:#1E293B;">
            {narrative}
        </div>
        """, unsafe_allow_html=True)

with ai_right:
    st.markdown("**Anomaly Detection**")
    if st.button("Scan for Anomalies", type="primary"):
        with st.spinner("Claude is scanning your data..."):
            anomalies = detect_anomalies(summary)
        st.markdown(f"""
        <div style="background:white; padding:1.5rem; border-radius:12px;
        border:1px solid #E2E8F0; line-height:1.7; color:#1E293B;">
            {anomalies}
        </div>
        """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#94A3B8; font-size:0.8rem; padding:1rem;">
    AI BI Dashboard — Built with Claude API + Streamlit + Plotly
</div>
""", unsafe_allow_html=True)