import streamlit as st
import pandas as pd
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

# Dicionários para tradução automática dos dados internos da base
traducao_genero = {'Female': 'Feminino', 'Male': 'Masculino', 'Unknown/Invalid': 'Desconhecido/Inválido'}
traducao_etnia = {
    'AfricanAmerican': 'Afro-americano',
    'Asian': 'Asiático',
    'Caucasian': 'Caucasiano',
    'Hispanic': 'Hispânico',
    'Other': 'Outros'
}

# 2. Carregamento e tratamento dos dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("hospital_readmissions.csv")
        # Padroniza os nomes das colunas
        df.columns = df.columns.str.lower().str.strip()
        df.columns = [c.split('[')[-1].replace(']', '') for c in df.columns]
        
        # Mapeia colunas encontradas para traduzir o conteúdo de inglês para português
        col_gender = next((c for c in df.columns if 'gender' in c or 'gênero' in c or 'genero' in c), None)
        col_race = next((c for c in df.columns if 'race' in c or 'etnia' in c or 'raça' in c or 'raca' in c), None)
        
        if col_gender:
            df[col_gender] = df[col_gender].replace(traducao_genero)
        if col_race:
            df[col_race] = df[col_race].replace(traducao_etnia)
            
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Identificar as colunas dinamicamente
    col_gender = next((c for c in df.columns if 'gender' in c or 'gênero' in c or 'genero' in c), None)
    col_race = next((c for c in df.columns if 'race' in c or 'etnia' in c or 'raça' in c or 'raca' in c), None)
    col_target = next((c for c in df.columns if 'target' in c or 'readmit' in c or 'readmissão' in c or 'readmissao' in c), None)
    col_risk = next((c for c in df.columns if 'risk' in c or 'risco' in c), None)
    col_time = next((c for c in df.columns if 'time' in c or 'tempo' in c or 'internação' in c or 'internacao' in c), None)
    col_age = next((c for c in df.columns if 'age' in c or 'idade' in c or 'faixa' in c), None)
    col_meds = next((c for c in df.columns if 'medication' in c or 'medicamento' in c or 'remédios' in c or 'remedios' in c or 'num_' in c), None)

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
        df_
