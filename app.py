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

# 2. Carregamento dos dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("hospital_readmissions.csv")
        # Força todos os nomes de colunas a ficarem em letras minúsculas e sem espaços para evitar erros
        df.columns = df.columns.str.lower().str.strip()
        # Se o Power BI exportou com o nome da tabela junto (ex: "tabela[gender]"), limpamos aqui:
        df.columns = [c.split('[')[-1].replace(']', '') for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Identificar as colunas dinamicamente (mesmo se mudarem de nome)
    col_gender = next((c for c in df.columns if 'gender' in c or 'gênero' in c or 'genero' in c), None)
    col_race = next((c for c in df.columns if 'race' in c or 'etnia' in c or 'raça' in c or 'raca' in c), None)
    col_target = next((c for c in df.columns if 'target' in c or 'readmit' in c or 'readmissão' in c or 'readmissao' in c), None)
    col_risk = next((c for c in df.columns if 'risk' in c or 'risco' in c), None)
    col_time = next((c for c in df.columns if 'time' in c or 'tempo' in c or 'internação' in c or 'internacao' in c), None)
    col_age = next((c for c in df.columns if 'age' in c or 'idade' in c or 'faixa' in c), None)
    col_meds = next((c for c in df.columns if 'medication' in c or 'medicamento' in c or 'reédios' in c or 'num_' in c), None)

    # 3. Sidebar - Filtros Dinâmicos
    st.sidebar.header("Filtros de Análise")
    
    df_filtered = df.copy()
    
    if col_gender and col_gender in df.columns:
        all_genders = sorted(df[col_gender].dropna().unique())
        selected_genders = st.sidebar.multiselect("Gênero", options=all_genders, default=all_genders)
        df_filtered = df_filtered[df_filtered[col_gender].isin(selected_genders)]
        
    if col_race and col_race in df.columns:
        all_races = sorted(df[col_race].dropna().unique())
        selected_races = st.sidebar.multiselect("Etnia", options=all_races, default=all_races)
        df_filtered = df_filtered[df_filtered[col_race].isin(selected_races)]
    
    # 4. Título Principal
    st.title("🏥 Hospital Readmission Analytics")
    st.markdown("Dashboard executivo para monitoramento e predição de risco de readmissão clínica.")
    st.write("---")
    
    # 5. Cartões de Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Total Pacientes</div><div class="metric-value">{len(df_filtered):,}</div></div>', unsafe_allow_html=True)
    with col2:
        taxa = (df_filtered[col_target].mean() * 100) if col_target and len(df_filtered) > 0 else 0
        if taxa > 100: taxa = taxa / 100 # Correção se o dado já veio multiplicado
        st.markdown(f'<div class="metric-card"><div class="metric-title">Taxa de Readmissão</div><div class="metric-value">{taxa:.2f}%</div></div>', unsafe_allow_html=True)
    with col3:
        risco = (df_filtered[col_risk].mean() * 100) if col_risk and len(df_filtered) > 0 else 0
        if risco > 100: risco = risco / 100
        st.markdown(f'<div class="metric-card"><div class="metric-title">Risco Médio</div><div class="metric-value">{risco:.2f}%</div></div>', unsafe_allow_html=True)
    with col4:
        tempo = df_filtered[col_time].mean() if col_time and len(df_filtered) > 0 else 0
        st.markdown(f'<div class="metric-card"><div class="metric-title">Tempo de Internação</div><div class="metric-value">{tempo:.1f} dias</div></div>', unsafe_allow_html=True)

    # Tema dos gráficos
    def apply_theme(fig, title_text):
        fig.update_layout(
            title=dict(text=title_text, font=dict(color='#39FF14', size=16)),
            paper_bgcolor='#1a1a1a', plot_bgcolor='#1a1a1a', font=dict(color='#FFFFFF'),
            xaxis=dict(gridcolor='#2d2d2d', title_font=dict(color='#39FF14'), tickfont=dict(color='#FFFFFF')),
            yaxis=dict(gridcolor='#2d2d2d', title_font=dict(color='#39FF14'), tickfont=dict(color='#FFFFFF')),
            margin=dict(l=40, r=40, t=50, b=40), showlegend=False
        )
        return fig

    # 6. Grid de Gráficos
    g1, g2 = st.columns(2)
    g3, g4 = st.columns(2)
    
    if col_gender and col_target:
        with g1:
            df_g = df_filtered.groupby(col_gender)[col_target].mean().reset_index()
            fig1 = px.bar(df_g, x=col_gender, y=col_target, text_auto='.2%')
            fig1.update_traces(marker_color='#39FF14')
            st.plotly_chart(apply_theme(fig1, "Readmissão por Gênero"), use_container_width=True)
            
    if col_time and col_risk:
        with g2:
            df_t = df_filtered.groupby(col_time)[col_risk].mean().reset_index()
            fig2 = px.line(df_t, x=col_time, y=col_risk)
            fig2.update_traces(line=dict(color='#39FF14', width=3))
            st.plotly_chart(apply_theme(fig2, "Tempo de Internação X Risco"), use_container_width=True)
            
    if col_age and col_target:
        with g3:
            df_a = df_filtered.groupby(col_age)[col_target].mean().reset_index()
            fig3 = px.bar(df_a, x=col_age, y=col_target)
            fig3.update_traces(marker_color='#39FF14')
            st.plotly_chart(apply_theme(fig3, "Readmissão por Faixa Etária"), use_container_width=True)
            
    if col_meds and col_risk:
        with g4:
            df_m = df_filtered.groupby(col_meds)[col_risk].mean().reset_index()
            fig4 = px.area(df_m, x=col_meds, y=col_risk)
            fig4.update_traces(line=dict(color='#39FF14'), fillcolor='rgba(57, 255, 20, 0.2)')
            st.plotly_chart(apply_theme(fig4, "Medicamentos X Risco"), use_container_width=True)
else:
    st.info("Aguardando o upload correto do arquivo 'hospital_readmissions.csv' no GitHub.")
