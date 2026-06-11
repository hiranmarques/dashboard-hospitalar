import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da página
st.set_page_config(
    page_title="Hospital Readmission Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS para o tema escuro com verde neon
st.markdown("""
    <style>
        .stApp {
            background-color: #030321;
            color: #FFFFFF;
        }
        [data-testid="stSidebar"] {
            background-color: #0b0b3a;
            border-right: 1px solid #1f1f7a;
        }
        [data-testid="stSidebar"] .stMarkdown h2, [data-testid="stSidebar"] p {
            color: #39FF14 !important;
        }
        .metric-card {
            background-color: #1a1a1a;
            border: 1px solid #2d2d2d;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }
        .metric-title {
            font-size: 14px;
            color: #39FF14;
            font-weight: bold;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .metric-value {
            font-size: 32px;
            color: #39FF14;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# 2. Carregamento dos dados
@st.cache_data
def load_data():
    try:
        return pd.read_csv("hospital_readmissions.csv")
    except:
        st.error("Arquivo 'hospital_readmissions.csv' não encontrado.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # 3. Sidebar - Filtros Dinâmicos
    st.sidebar.header("Filtros de Análise")
    
    all_genders = sorted(df['gender'].dropna().unique()) if 'gender' in df.columns else []
    selected_genders = st.sidebar.multiselect("Gênero", options=all_genders, default=all_genders)
    
    all_races = sorted(df['race'].dropna().unique()) if 'race' in df.columns else []
    selected_races = st.sidebar.multiselect("Etnia", options=all_races, default=all_races)
    
    # Filtragem
    df_filtered = df.copy()
    if 'gender' in df.columns and selected_genders:
        df_filtered = df_filtered[df_filtered['gender'].isin(selected_genders)]
    if 'race' in df.columns and selected_races:
        df_filtered = df_filtered[df_filtered['race'].isin(selected_races)]
    
    # 4. Título
    st.title("🏥 Hospital Readmission Analytics")
    st.markdown("Dashboard executivo para monitoramento e predição de risco de readmissão clínica.")
    st.write("---")
    
    # 5. Cartões de Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_p = len(df_filtered)
        st.markdown(f'<div class="metric-card"><div class="metric-title">Total Pacientes</div><div class="metric-value">{total_p:,}</div></div>', unsafe_allow_html=True)
    with col2:
        taxa = (df_filtered['target'].mean() * 100) if 'target' in df_filtered.columns and len(df_filtered) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-title">Taxa de Readmissão</div><div class="metric-value">{taxa:.2f}%</div></div>', unsafe_allow_html=True)
    with col3:
        risco = (df_filtered['risk_score'].mean() * 100) if 'risk_score' in df_filtered.columns and len(df_filtered) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-title">Risco Médio</div><div class="metric-value">{risco:.2f}%</div></div>', unsafe_allow_html=True)
    with col4:
        tempo = df_filtered['time_in_hospital'].mean() if 'time_in_hospital' in df_filtered.columns and len(df_filtered) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-title">Tempo de Internação</div><div class="metric-value">{tempo:.1f} dias</div></div>', unsafe_allow_html=True)

    # Tema dos gráficos Plotly
    def apply_theme(fig, title_text):
        fig.update_layout(
            title=dict(text=title_text, font=dict(color='#39FF14', size=16)),
            paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#2d2d2d', title_font=dict(color='#39FF14')),
            yaxis=dict(gridcolor='#2d2d2d', title_font=dict(color='#39FF14')),
            margin=dict(l=40, r=40, t=50, b=40), showlegend=False
        )
        return fig

    # 6. Grid de Gráficos
    g1, g2 = st.columns(2)
    g3, g4 = st.columns(2)
    
    if 'gender' in df_filtered.columns and 'target' in df_filtered.columns:
        with g1:
            df_g = df_filtered.groupby('gender')['target'].mean().reset_index()
            fig1 = px.bar(df_g, x='gender', y='target', text_auto='.2%')
            fig1.update_traces(marker_color='#39FF14')
            st.plotly_chart(apply_theme(fig1, "Readmissão por Gênero (Proporcional)"), use_container_width=True)
            
    if 'time_in_hospital' in df_filtered.columns and 'risk_score' in df_filtered.columns:
        with g2:
            df_t = df_filtered.groupby('time_in_hospital')['risk_score'].mean().reset_index()
            fig2 = px.line(df_t, x='time_in_hospital', y='risk_score')
            fig2.update_traces(line=dict(color='#39FF14', width=3))
            st.plotly_chart(apply_theme(fig2, "Tempo de Internação X Risco"), use_container_width=True)
            
    if 'age' in df_filtered.columns and 'target' in df_filtered.columns:
        with g3:
            age_order = ['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)', '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)']
            df_a = df_filtered.groupby('age')['target'].mean().reset_index()
            df_a['age'] = pd.Categorical(df_a['age'], categories=age_order, ordered=True)
            df_a = df_a.sort_values('age')
            fig3 = px.bar(df_a, x='age', y='target')
            fig3.update_traces(marker_color='#39FF14')
            st.plotly_chart(apply_theme(fig3, "Readmissão por Faixa Etária"), use_container_width=True)
            
    if 'num_medications' in df_filtered.columns and 'risk_score' in df_filtered.columns:
        with g4:
            df_m = df_filtered.groupby('num_medications')['risk_score'].mean().reset_index()
            fig4 = px.area(df_m, x='num_medications', y='risk_score')
            fig4.update_traces(line=dict(color='#39FF14'), fillcolor='rgba(57, 255, 20, 0.2)')
            st.plotly_chart(apply_theme(fig4, "Medicamentos X Risco"), use_container_width=True)
