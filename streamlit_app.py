import streamlit as st
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from src.scoring import calculate_esg_scores, cluster_companies
from src.database import save_to_db, get_top_companies, get_average_score

st.set_page_config(page_title="ESG Dashboard", layout="wide", page_icon="🌱")

@st.cache_data
def load_and_process_data(df):
    scaler = MinMaxScaler()
    features = ['carbon_emissions', 'energy_usage', 'employee_satisfaction', 
                'diversity_score', 'board_independence', 'ethics_score']
    
    df[features] = scaler.fit_transform(df[features]) * 100
    
    df['E_score'] = (100 - df['carbon_emissions']) * 0.6 + (100 - df['energy_usage']) * 0.4
    df['S_score'] = df['employee_satisfaction'] * 0.6 + df['diversity_score'] * 0.4
    df['G_score'] = df['board_independence'] * 0.5 + df['ethics_score'] * 0.5
    
    df['ESG_score'] = (df['E_score'] + df['S_score'] + df['G_score']) / 3
    df['ESG_score'] = df['ESG_score'].clip(lower=0).round(2)
    
    df['Risk_Level'] = df['ESG_score'].apply(
        lambda x: "Low Risk" if x >= 75 else ("Medium Risk" if x >= 50 else "High Risk")
    )
    
    df = df.sort_values(by='ESG_score', ascending=False)
    df['Rank'] = range(1, len(df) + 1)
    
    df = cluster_companies(df)
    
    return df

st.title("🌱 ESG Portfolio Analytics Dashboard")

with st.expander("ℹ️ About this project", expanded=False):
    st.markdown("""
    This dashboard evaluates companies based on **Environmental, Social, and Governance (ESG)** metrics.
    
    - **Environmental**: Carbon emissions, energy usage  
    - **Social**: Employee satisfaction, diversity  
    - **Governance**: Board structure, ethics  
    
    Features: ESG scoring, risk classification, K-Means clustering, and interactive visualizations.
    """)

st.sidebar.header("⚙️ Settings")

mode = st.sidebar.selectbox("Data Source", ["Default Dataset", "Upload CSV"])

if mode == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload Dataset", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a dataset")
        st.stop()
else:
    df = pd.read_csv("data/esg_data.csv")

df = load_and_process_data(df)

save_to_db(df)

min_score = st.sidebar.slider("Minimum ESG Score", 0, 100, 0)
risk_filter = st.sidebar.multiselect("Risk Level", ["Low Risk", "Medium Risk", "High Risk"], default=["Low Risk", "Medium Risk", "High Risk"])

df_filtered = df[(df['ESG_score'] >= min_score) & (df['Risk_Level'].isin(risk_filter))]

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏆 Rankings", "📈 Analytics", "💾 Export"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Companies", len(df_filtered), delta=f"{len(df_filtered) - len(df)} filtered")
    with col2:
        st.metric("Average ESG Score", round(df_filtered['ESG_score'].mean(), 2), 
                  delta=f"{round(df_filtered['ESG_score'].mean() - df['ESG_score'].mean(), 2)} vs all")
    with col3:
        low_risk_pct = len(df_filtered[df_filtered['Risk_Level'] == 'Low Risk']) / len(df_filtered) * 100 if len(df_filtered) > 0 else 0
        st.metric("Low Risk %", f"{low_risk_pct:.1f}%")
    with col4:
        best_company = df_filtered.iloc[0]['company'] if len(df_filtered) > 0 else "N/A"
        st.metric("Best Performer", best_company)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("ESG Score Distribution")
        fig_hist = px.bar(df_filtered, x='company', y='ESG_score',
                         color='Risk_Level',
                         color_discrete_map={'Low Risk': '#2ecc71', 'Medium Risk': '#f39c12', 'High Risk': '#e74c3c'},
                         template='plotly_white',
                         title="ESG Scores by Company")
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col_chart2:
        st.subheader("Risk Level Distribution")
        risk_counts = df_filtered['Risk_Level'].value_counts()
        fig_pie = px.pie(values=risk_counts.values, names=risk_counts.index,
                        color=risk_counts.index,
                        color_discrete_map={'Low Risk': '#2ecc71', 'Medium Risk': '#f39c12', 'High Risk': '#e74c3c'},
                        template='plotly_white')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    if not df_filtered.empty and len(df_filtered) > 2:
        st.subheader("🏢 Company Clusters")
        fig_scatter = px.scatter(df_filtered, x='ESG_score', y='company', 
                                color='Cluster_Label',
                                size='ESG_score',
                                hover_data=['E_score', 'S_score', 'G_score'],
                                template='plotly_white',
                                title="Company Clustering by ESG Performance")
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.subheader("🏆 ESG Company Rankings")
    
    if not df_filtered.empty:
        display_cols = ['Rank', 'company', 'E_score', 'S_score', 'G_score', 'ESG_score', 'Risk_Level', 'Cluster_Label']
        st.dataframe(df_filtered[display_cols], use_container_width=True, hide_index=True)
    else:
        st.warning("No companies match the selected filters")

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 E/S/G Score Breakdown")
        if not df_filtered.empty:
            avg_scores = df_filtered[['E_score', 'S_score', 'G_score']].mean()
            fig_bar = px.bar(x=avg_scores.index, y=avg_scores.values,
                           color=avg_scores.index,
                           color_discrete_sequence=['#27ae60', '#3498db', '#9b59b6'],
                           template='plotly_white',
                           title="Average E/S/G Scores")
            fig_bar.update_yaxes(range=[0, 100])
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Top 5 Companies Comparison")
        top5 = df_filtered.head(5)
        fig_radar = go.Figure()
        
        categories = ['E_score', 'S_score', 'G_score']
        for i, row in top5.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row['E_score'], row['S_score'], row['G_score'], row['E_score']],
                theta=['Environmental', 'Social', 'Governance', 'Environmental'],
                fill='toself',
                name=row['company']
            ))
        
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                              showlegend=True, template='plotly_white')
        st.plotly_chart(fig_radar, use_container_width=True)
    
    st.subheader("🏭 Industry Comparison")
    
    if 'industry' not in df.columns:
        df['industry'] = (df.index % 5).map({0: 'Technology', 1: 'Energy', 2: 'Finance', 3: 'Healthcare', 4: 'Retail'})
    
    industry_avg = df.groupby('industry')[['E_score', 'S_score', 'G_score', 'ESG_score']].mean().reset_index()
    
    fig_industry = px.bar(industry_avg, x='industry', y='ESG_score',
                         color='ESG_score', color_continuous_scale='Viridis',
                         template='plotly_white', title="Average ESG Score by Industry")
    st.plotly_chart(fig_industry, use_container_width=True)
    
    with st.expander("View Industry Breakdown"):
        st.dataframe(industry_avg, use_container_width=True, hide_index=True)
    
    st.subheader("📈 Score Correlation Heatmap")
    score_cols = ['E_score', 'S_score', 'G_score', 'ESG_score']
    corr_matrix = df_filtered[score_cols].corr()
    fig_heatmap = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdYlGn',
                           template='plotly_white', title="Correlation between ESG Components")
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab4:
    st.subheader("💾 Export Results")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        st.download_button(
            label="📥 Download Full Results (CSV)",
            data=df.to_csv(index=False),
            file_name="esg_results_full.csv",
            mime="text/csv"
        )
    
    with col_exp2:
        st.download_button(
            label="📥 Download Filtered Results (CSV)",
            data=df_filtered.to_csv(index=False),
            file_name="esg_results_filtered.csv",
            mime="text/csv"
        )
    
    st.subheader("🔍 SQL-Based Insights")
    st.code("""
SELECT company, ESG_score, Risk_Level
FROM esg_data
ORDER BY ESG_score DESC
LIMIT 5;
""", language='sql')
    
    top_companies = get_top_companies(5)
    avg_score = get_average_score()
    
    col_sql1, col_sql2 = st.columns(2)
    
    with col_sql1:
        st.write("**Top 5 Companies (from SQL)**")
        st.dataframe(top_companies, use_container_width=True, hide_index=True)
    
    with col_sql2:
        st.metric("Average ESG Score (from DB)", round(avg_score, 2))

st.sidebar.markdown("---")
st.sidebar.markdown("**📌 Filters Applied:**")
st.sidebar.write(f"- Min Score: {min_score}")
st.sidebar.write(f"- Risk Levels: {', '.join(risk_filter)}")
