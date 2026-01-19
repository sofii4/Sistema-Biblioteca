import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from fpdf import FPDF
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Configuração da página (Wide mode para caber as tabelas)
st.set_page_config(page_title="Relatório do Acervo", layout="wide")

# Conexão com o banco
engine = create_engine(os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://"))

st.title("📊 Painel de Controle de Acervos")

# Busca os dados uma única vez
df = pd.read_sql("SELECT * FROM obras", engine)

# --- CRIAÇÃO DAS ABAS DE NAVEGAÇÃO ---
tab_geral, tab_disp, tab_emp, tab_res, tab_ext = st.tabs([
    "📈 Visão Geral", 
    "✅ Disponíveis", 
    "📕 Emprestados", 
    "📦 Reserva Técnica", 
    "⚠️ Extraviados"
])

# ===================================================
# ABA 1: VISÃO GERAL (Gráficos e PDF)
# ===================================================
with tab_geral:
    st.markdown("### Resumo dos Indicadores")
    
    # Cálculos
    total_obras = len(df)
    disponiveis = len(df[df['situacao'] == 'disponivel'])
    emprestados = len(df[df['situacao'] == 'emprestado'])
    reserva = len(df[df['situacao'] == 'reserva'])
    extraviados = len(df[df['situacao'] == 'extraviado'])

    # Cards de Métricas
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Total Geral", total_obras)
    with col2: st.metric("Disponíveis", disponiveis)
    with col3: st.metric("Emprestados", emprestados)
    with col4: st.metric("Reserva", reserva)
    with col5: st.metric("Extraviados", extraviados)

    st.markdown("---")
    
    # Gráficos
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Acervo por Tipo**")
        st.bar_chart(df['tipo'].value_counts())
    with c2:
        st.write("**Status do Acervo**")
        st.bar_chart(df['situacao'].value_counts(), color="#ffaa00")

    # --- FUNÇÃO DO PDF (Mantida a versão resumida e bonita) ---
    def gerar_pdf_resumo(dataframe):
        pdf = FPDF()
        pdf.add_page()
        
        # Cabeçalho
        pdf.set_fill_color(52, 152, 219)
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 24)
        pdf.cell(190, 20, "RELATÓRIO GERENCIAL", ln=True, align="C")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(190, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
        
        pdf.set_text_color(0, 0, 0)
        pdf.ln(20)
        
        # Dados
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(190, 10, " Resumo Estatístico", ln=True, fill=False)
        pdf.ln(5)
        
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(95, 10, f"Total de Obras: {total_obras}", border="B")
        pdf.cell(95, 10, f"Disponíveis: {disponiveis}", border="B", ln=True)
        pdf.cell(95, 10, f"Emprestados: {emprestados}", border="B")
        pdf.cell(95, 10, f"Reserva Técnica: {reserva}", border="B", ln=True)
        pdf.cell(95, 10, f"Extraviados: {extraviados}", border="B", ln=True)

        pdf.set_y(-30)
        pdf.set_font("Helvetica", "I", 8)
        pdf.cell(190, 10, "Relatório gerado via Streamlit Dashboard", align="C")
        
        return bytes(pdf.output())

    st.markdown("### Exportar Relatório")
    try:
        pdf_bytes = gerar_pdf_resumo(df)
        st.download_button(
            label="📄 Baixar Resumo em PDF",
            data=pdf_bytes,
            file_name=f"resumo_biblioteca_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {e}")

# ===================================================
# CONFIGURAÇÃO COMUM DAS TABELAS
# ===================================================
# Colunas que queremos mostrar nas listas (para não ficar poluído)
colunas_visiveis = ['titulo', 'autor', 'cod_chamada', 'tipo', 'estante', 'cdd']

# ===================================================
# ABA 2: DISPONÍVEIS
# ===================================================
with tab_disp:
    st.header(f"Livros Disponíveis ({disponiveis})")
    df_disp = df[df['situacao'] == 'disponivel'][colunas_visiveis]
    st.dataframe(df_disp, use_container_width=True, hide_index=True)

# ===================================================
# ABA 3: EMPRESTADOS
# ===================================================
with tab_emp:
    st.header(f"Livros Emprestados ({emprestados})")
    df_emp = df[df['situacao'] == 'emprestado'][colunas_visiveis]
    st.dataframe(df_emp, use_container_width=True, hide_index=True)

# ===================================================
# ABA 4: RESERVA TÉCNICA
# ===================================================
with tab_res:
    st.header(f"Reserva Técnica ({reserva})")
    df_res = df[df['situacao'] == 'reserva'][colunas_visiveis]
    st.dataframe(df_res, use_container_width=True, hide_index=True)

# ===================================================
# ABA 5: EXTRAVIADOS
# ===================================================
with tab_ext:
    st.header(f"Livros Extraviados ({extraviados})")
    if extraviados > 0:
        df_ext = df[df['situacao'] == 'extraviado'][colunas_visiveis]
        st.dataframe(df_ext, use_container_width=True, hide_index=True)
    else:
        st.success("Nenhum livro registrado como extraviado no momento! 🎉")