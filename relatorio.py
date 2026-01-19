import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração da página
st.set_page_config(page_title="Relatório do Acervo", layout="wide")

# Conexão com o banco
engine = create_engine(os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://"))

st.title("📊 Relatório Geral de Acervos")
st.markdown("---")

# Busca os dados
df = pd.read_sql("SELECT * FROM obras", engine)

# --- DASHBOARD (Métricas automáticas) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Obras", len(df))
with col2:
    disp = len(df[df['situacao'] == 'disponivel'])
    st.metric("Disponíveis", disp)
with col3:
    emp = len(df[df['situacao'] == 'emprestado'])
    st.metric("Emprestados", emp, delta=f"{(emp/len(df)*100):.1f}%", delta_color="inverse")
with col4:
    res = len(df[df['situacao'] == 'reserva'])
    st.metric("Reserva Técnica", res)

st.markdown("### Análise por Categoria")
c1, c2 = st.columns(2)

with c1:
    st.bar_chart(df['tipo'].value_counts())

with c2:
    # Tabela de dados inteligente (com busca e filtro nativo)
    st.dataframe(df[['titulo', 'autor', 'tipo', 'situacao']], use_container_width=True)

st.markdown("### Distribuição de Idiomas")
st.area_chart(df['idioma'].value_counts())