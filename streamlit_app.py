import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.database import save_to_db, get_top_companies, get_average_score

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="ESG Dashboard", layout="wide")

st.title("ESG Portfolio Analytics Dashboard")

# -----------------------------------
# ABOUT SECTION
# -----------------------------------
with st.expander("About this project"):
    st.write("""
    This dashboard evaluates companies based on Environmental, Social, and Governance (ESG) metrics.

    - Environmental: Emissions, energy usage  
    - Social: Employee satisfaction, diversity  
    - Governance: Board structure, ethics  

    It computes ESG scores, ranks companies, classifies risk levels, and provides insights
    using both analytics and SQL queries.
    """)

# -----------------------------------
# SIDEBAR SETTINGS
# -----------------------------------
st.sidebar.header("Settings")

mode = st.sidebar.selectbox(
    "Data Source",
    ["Default Dataset", "Upload CSV"]
)

if mode == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload Dataset", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a dataset")
        st.stop()
else:
    df = pd.read_csv("data/esg_data.csv")

# -----------------------------------
# ESG PROCESSING
# -----------------------------------
scaler = MinMaxScaler()

features = [
    'carbon_emissions',
    'energy_usage',
    'employee_satisfaction',
    'diversity_score',
    'board_independence',
    'ethics_score'
]

df[features] = scaler.fit_transform(df[features]) * 100

# Scores
df['E_score'] = (100 - df['carbon_emissions']) * 0.6 + (100 - df['energy_usage']) * 0.4
df['S_score'] = df['employee_satisfaction'] * 0.6 + df['diversity_score'] * 0.4
df['G_score'] = df['board_independence'] * 0.5 + df['ethics_score'] * 0.5

df['ESG_score'] = (df['E_score'] + df['S_score'] + df['G_score']) / 3
df['ESG_score'] = df['ESG_score'].clip(lower=0).round(2)

# -----------------------------------
# RISK CLASSIFICATION
# -----------------------------------
def classify_risk(score):
    if score >= 75:
        return "Low Risk"
    elif score >= 50:
        return "Medium Risk"
    else:
        return "High Risk"

df['Risk_Level'] = df['ESG_score'].apply(classify_risk)

# -----------------------------------
# RANKING
# -----------------------------------
df = df.sort_values(by='ESG_score', ascending=False)
df['Rank'] = range(1, len(df) + 1)

# -----------------------------------
# SAVE TO DATABASE
# -----------------------------------
save_to_db(df)

# -----------------------------------
# FILTER
# -----------------------------------
min_score = st.sidebar.slider("Minimum ESG Score", 0, 100, 0)
df_filtered = df[df['ESG_score'] >= min_score]

# -----------------------------------
# MAIN LAYOUT
# -----------------------------------
col1, col2 = st.columns([2, 1])

# -------- TABLE --------
with col1:
    st.subheader("ESG Rankings")
    st.dataframe(
        df_filtered[['company', 'E_score', 'S_score', 'G_score', 'ESG_score', 'Risk_Level', 'Rank']],
        use_container_width=True
    )

# -------- INSIGHTS --------
with col2:
    st.subheader("Insights")

    if not df_filtered.empty:
        st.success(f"Best Company: {df_filtered.iloc[0]['company']}")
        st.error(f"Risky Company: {df_filtered.iloc[-1]['company']}")
        st.metric("Average ESG Score", round(df_filtered['ESG_score'].mean(), 2))
    else:
        st.warning("No data available")

# -----------------------------------
# VISUALIZATION
# -----------------------------------
st.subheader("ESG Score Visualization")
if not df_filtered.empty:
    st.bar_chart(df_filtered.set_index('company')['ESG_score'])

# -----------------------------------
# SQL SECTION
# -----------------------------------
st.subheader("SQL-Based Insights")

st.code("""
SELECT company, ESG_score, Risk_Level
FROM esg_data
ORDER BY ESG_score DESC
LIMIT 3;
""", language='sql')

top_companies = get_top_companies(3)
avg_score = get_average_score()

st.write("Top 3 Companies (from SQL)")
st.dataframe(top_companies, use_container_width=True)

st.write("Average ESG Score (from SQL):", avg_score)

# -----------------------------------
# DOWNLOAD BUTTON
# -----------------------------------
st.subheader("Export Results")

st.download_button(
    label="Download ESG Results as CSV",
    data=df.to_csv(index=False),
    file_name="esg_results.csv",
    mime="text/csv"
)