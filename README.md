# 📊 AI-Powered BI Dashboard

> Upload any sales CSV and get instant AI-powered business intelligence.

An interactive BI dashboard that combines Plotly visualisations with Claude AI 
to automatically generate executive narratives and detect data anomalies.

---

## ✨ Features

- **KPI Cards** — Total revenue, units sold, return rate, top region
- **Interactive Charts** — Revenue by product, units by region, daily trend
- **AI Executive Narrative** — Claude writes a plain English business summary
- **Anomaly Detection** — Claude automatically flags unusual patterns with specific numbers and recommended actions
- **Upload Any CSV** — Works with any sales dataset matching the column format

---

## 🔍 Anomaly Detection Examples

Claude automatically identifies:
- Products with abnormally high return rates
- Revenue outlier days with exact dates and variance percentages
- Mismatches between volume and revenue that suggest pricing issues
- Data quality flags across multiple metrics

---

## 🔐 Privacy First

Only aggregated statistics are sent to the AI — never raw customer data.

---

## 🎨 Design

Designed in Figma before building.
[View Figma Designs →](https://www.figma.com/design/cWQ6g5FToUlVigY3PVLcz0/M1-Data-Assitant?node-id=47-44&t=yrViGimidBFDcryJ-1)


## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/RutvikBhamwari/AI_Powered_BI_Dashboard.git
cd AI_Powered_BI_Dashboard
```

2. Install dependencies:
```bash
pip3 install anthropic streamlit pandas plotly
```

3. Set your API key:
```bash
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

4. Run the dashboard:
```bash
streamlit run dashboard.py
```

5. Upload your CSV or use the included sample data

---

## 📁 Project Structure
```
AI_Powered_BI_Dashboard/
├── dashboard.py              # Main Streamlit dashboard
├── generate_data.py          # Sample data generator
├── sales_data.csv            # 10-row sample dataset
├── sales_data_6months.csv    # 740-row 6-month dataset
└── .gitignore
```

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Anthropic Claude API | Narrative generation + anomaly detection |
| Streamlit | Web interface |
| Plotly | Interactive charts |
| pandas | Data processing |

---

## 💡 How Anomaly Detection Works

1. Dashboard calculates aggregated statistics — no raw data sent to AI
2. Summary sent to Claude with anomaly detection system prompt
3. Claude analyses patterns across products, regions, and time
4. Flags returned with specific numbers, context, and recommended actions

---

## 👤 Author

**Rutvik Bhamwari**
BI Analyst building AI-powered data products
[GitHub](https://github.com/RutvikBhamwari)

---