import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuração da página
st.set_page_config(
    page_title="Análise de Readmissão Hospitalar",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS para o tema escuro com verde neon
st.markdown("""
    <style>
        .stApp { background-color: #030321; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #0b0b3a; border-right: 1px solid #1f1f7a; }
        [data-testid="stSidebar"] .stMarkdown h2, [data-testid="stSidebar"] p { color: #39FF14 !important; }
        .metric-card {
            background-color: #1a1a1a; border: 1px solid #2d2d2d; border-radius: 12px;
            padding: 20px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); margin-bottom: 20px;
        }
        .metric-title { font-size: 14px; color: #39FF14; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; }
        .metric-value { font-size: 32px; color: #39FF14; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. Geração Inteligente Simulada dos 55 Mil Pacientes
@st.cache_data
def simular_dados():
    np.random.seed(42)
    n_samples = 55000
    
    # Proporções simuladas com base no dashboard original
    genders = np.random.choice(['Feminino', 'Masculino', 'Desconhecido'], size=n_samples, p=[0.52, 0.47, 0.01])
    races = np.random.choice(['Caucasiano', 'Afro-americano', 'Hispânico', 'Asiático', 'Outros'], size=n_samples, p=[0.75, 0.14, 0.04, 0.02, 0.05])
    
    age_bins = ['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)', '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)']
    age_probs = [0.01, 0.02, 0.05, 0.12, 0.18, 0.22, 0.20, 0.14, 0.05, 0.01]
    ages = np.random.choice(age_bins, size=n_samples, p=age_probs)
    
    time_in_hospital = np.random.geometric(p=0.25, size=n_samples) + 1
    time_in_hospital = np.clip(time_in_hospital, 1, 14)
    
    num_medications = np.random.normal(loc=16, scale=8, size=n_samples).astype(int)
    num_medications = np.clip(num_medications, 1, 81)
    
    # Alinhando a taxa de readmissão próxima a 11.25% e risco médio a 37%
    target = np.random.choice([1, 0], size=n_samples, p=[0.1125, 0.8875])
    
    base_risk = 0.25 + (time_in_hospital * 0.02) + (num_medications * 0.003)
    risk_score = np.clip(base_risk + np.random.normal(0, 0.05, n_samples), 0, 1)
    
    df = pd.DataFrame({
        'gênero': genders,
        'etnia': races,
        'faixa etária': ages,
        'tempo de internação': time_in_hospital,
        'medicamentos': num_medications,
        'readmissão': target,
        'risco': risk_score
    })
    return df

df_filtered = simular_dados()

# 3. Sidebar - Filtros Dinâmicos
st.sidebar.header("Filtros de Análise")

all_genders = sorted(df_filtered['gênero'].unique())
selected_genders = st.sidebar.multiselect("Gênero", options=all_genders, default=all_genders)
df_filtered = df_filtered[df_filtered['gênero'].isin(selected_genders)]
    
all_races = sorted(df_filtered['etnia'].unique())
selected_races = st.sidebar.multiselect("Etnia", options=all_races, default=all_races)
df_filtered = df_filtered[df_filtered['etnia'].isin(selected_races)]

# 4. Título Principal
st.title("Análise de Readmissão Hospitalar")
st.markdown("Dashboard executivo para monitoramento e predição de risco de readmissão clínica.")
st.write("---")

# 5. Cartões de Métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Total de Pacientes</div><div class="metric-value">{len(df_filtered):,}</div></div>', unsafe_allow_html=True)
with col2:
    taxa = (df_filtered['readmissão'].mean() * 100) if len(df_filtered) > 0 else 0
    st.markdown(f'<div class="metric-card"><div class="metric-title">Taxa de Readmissão</div><div class="metric-value">{taxa:.2f}%</div></div>', unsafe_allow_html=True)
with col3:
    risco = (df_filtered['risco'].mean() * 100) if len(df_filtered) > 0 else 0
    st.markdown(f'<div class="metric-card"><div class="metric-title">Risco Médio</div><div class="metric-value">{risco:.2f}%</div></div>', unsafe_allow_html=True)
with col4:
    tempo = df_filtered['tempo de internação'].mean() if len(df_filtered) > 0 else 0
    st.markdown(f'<div class="metric-card"><div class="metric-title">Tempo de Internação</div><div class="metric-value">{tempo:.1f} dias</div></div>', unsafe_allow_html=True)

# Tema dos gráficos
def apply_theme(fig, title_text, xaxis_title="", yaxis_title=""):
    fig.update_layout(
        title=dict(text=title_text, font=dict(color='#39FF14', size=16)),
        paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font=dict(color='#FFFFFF'),
        xaxis=dict(title=xaxis_title, gridcolor='#2d2d2d', title_font=dict(color='#39FF14'), tickfont=dict(color='#FFFFFF')),
        yaxis=dict(title=yaxis_title, gridcolor='#2d2d2d', title_font=dict(color='#39FF14'), tickfont=dict(color='#FFFFFF')),
        margin=dict(l=40, r=40, t=50, b=40), showlegend=False
    )
    return fig

# 6. Grid de Gráficos em Português
g1, g2 = st.columns(2)
g3, g4 = st.columns(2)

with g1:
    df_g = df_filtered.groupby('gênero')['readmissão'].mean().reset_index()
    fig1 = px.bar(df_g, x='gênero', y='readmissão', text_auto='.2%')
    fig1.update_traces(marker_color='#39FF14')
    st.plotly_chart(apply_theme(fig1, "Readmissão por Gênero", "Gênero", "Taxa Média"), use_container_width=True)
        
with g2:
    df_t = df_filtered.groupby('tempo de internação')['risco'].mean().reset_index()
    fig2 = px.line(df_t, x='tempo de internação', y='risco')
    fig2.update_traces(line=dict(color='#39FF14', width=3))
    st.plotly_chart(apply_theme(fig2, "Tempo de Internação X Risco", "Tempo de Internação (Dias)", "Média de Risco"), use_container_width=True)
        
with g3:
    age_order = ['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)', '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)']
    df_a = df_filtered.groupby('faixa etária')['readmissão'].mean().reset_index()
    df_a['faixa etária'] = pd.Categorical(df_a['faixa etária'], categories=age_order, ordered=True)
    df_a = df_a.sort_values('faixa etária')
    fig3 = px.bar(df_a, x='faixa etária', y='readmissão')
    fig3.update_traces(marker_color='#39FF14')
    st.plotly_chart(apply_theme(fig3, "Readmissão por Faixa Etária", "Faixa Etária", "Taxa Média"), use_container_width=True)
        
with g4:
    df_m = df_filtered.groupby('medicamentos')['risco'].mean().reset_index()
    fig4 = px.area(df_m, x='medicamentos', y='risco')
    fig4.update_traces(line=dict(color='#39FF14'), fillcolor='rgba(57, 255, 20, 0.2)')
    st.plotly_chart(apply_theme(fig4, "Medicamentos X Risco", "Número de Medicamentos", "Média de Risco"), use_container_width=True)
