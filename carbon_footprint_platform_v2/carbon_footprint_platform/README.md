# 🌿 EcoTrack – Carbon Footprint Awareness Platform

> **[Challenge 3] Hack2Skill – PromptWars**  
> Design a solution that helps individuals understand, track, and reduce their carbon footprint through simple actions and personalized insights.

---

## 🌍 What is EcoTrack?

EcoTrack is an AI-powered Carbon Footprint Awareness Platform built with Python and Streamlit. It helps individuals **understand**, **track**, and **reduce** their carbon emissions through:

- 📊 **Carbon Calculator** – Calculate CO₂ from transport, food, energy, and shopping
- 📅 **Activity Tracker** – Log daily activities and visualize trends over time
- 💡 **Tips & Insights** – Personalized eco tips based on your emission profile
- 🤖 **AI EcoAdvisor** – Claude-powered personalized reduction recommendations
- 💬 **EcoAI Chat** – Ask anything about sustainability and carbon footprint

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🔢 Carbon Calculator | 30+ activities across 4 categories with real emission factors |
| 📈 Dashboard | Real-time gauge, badges, KPIs vs global average |
| 📅 Activity Tracker | Daily trend charts, category breakdowns, filterable logs |
| 💡 Smart Tips | Category-specific eco tips with CO₂ savings estimates |
| 🤖 AI Suggestions | Personalized recommendations powered by Claude AI |
| 💬 AI Chat | Conversational eco-advice assistant |

---

## 🛠️ Tech Stack

- **Frontend & Backend**: Python + Streamlit
- **Data Visualization**: Plotly
- **Data Processing**: Pandas
- **AI Integration**: Anthropic Claude API (claude-sonnet-4-6)
- **Deployment**: Streamlit Community Cloud

---

## ⚙️ Setup & Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/carbon-footprint-platform.git
cd carbon-footprint-platform
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. (Optional) Add your Anthropic API Key
Enter your API key in the sidebar to enable AI-powered features.

---

## 📊 Emission Data Sources

Emission factors are based on:
- UK Government GHG Conversion Factors (DEFRA)
- IPCC Sixth Assessment Report
- Our World in Data – Carbon emissions per food type

---

## 🏗️ Project Structure

```
carbon-footprint-platform/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 📸 Screenshots

> Dashboard with real-time CO₂ gauge, badges, and KPI metrics  
> Carbon Calculator with activity comparison charts  
> AI EcoAdvisor with personalized recommendations  
> Interactive trend charts and category breakdowns

---

## 🌱 Impact

- Helps users identify their **top emission sources**
- Provides **actionable, quantified** reduction steps
- Compares individual footprint against **global averages**
- AI-powered **personalized coaching** for sustained behavior change

---

## 👩‍💻 Author

**Vaishnavi** – B.Tech CSE (AI & Data Science), Pragati Engineering College  
Built for Hack2Skill PromptWars – Challenge 3: Carbon Footprint Awareness Platform

---

## 📄 License

MIT License – feel free to use and adapt!
