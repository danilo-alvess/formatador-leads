import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.set_page_config(
    page_title="Formatador de Leads - ADM Soluções",
    page_icon="https://raw.githubusercontent.com/danilo-alvess/formatador-leads/main/logo_adm.png"
)


st.title("📊 Formatador de Planilha de Leads")
st.title("ADM Soluções")
st.write("Envie a planilha bruta (.xlsx) exportada do site **Casa dos Dados** para gerar a versão formatada.")

st.markdown("### ⚠️ Importante:")
st.warning("Se estiver no celular, baixe a planilha primeiro para o dispositivo. Upload direto do Google Drive pode não funcionar.")

# Lista de responsáveis
responsaveis = {
    "Selecione o responsável": "",
    "Amanda Prudente": "amanda.p@admsolucoes.com.br",
    "Brendo Félix": "brendo@admsolucoes.com.br",
    "Carlos Eduardo": "eduardo@admsolucoes.com.br",
    "Danilo Alves": "danilo.a@admsolucoes.com.br",
    "Grazy Marcelino": "grazy@admsolucoes.com.br",
    "Jamille Costa": "jamille@admsolucoes.com.br",
    "Pedro Paiva": "pedro.paiva@admsolucoes.com.br",
    "Ryan Caliel": "caliel@admsolucoes.com.br"
}

responsavel = st.selectbox("Quem está validando os leads?", list(responsaveis.keys()))
email_responsavel = responsaveis[responsavel]

uploaded_file = st.file_uploader("📁 Faça o upload da planilha bruta (.xlsx)", type=["xlsx"])

if uploaded_file and email_responsavel:
    try:
        df_empresas = pd.read_excel(uploaded_file, sheet_name="empresas")

        def limpar_nome(nome):
            return re.sub(r'[0-9.]', '', nome).strip()

        # Aplicar regras de formatação
        df_formatado = pd.DataFrame()
        df_formatado["Nome do negócio"] = df_empresas["Nome Fantasia"].fillna(df_empresas["Razao Social"]).apply(limpar_nome)
        df_formatado["Etapa do negócio"] = "prospect"
        df_formatado["Proprietário do negócio"] = email_responsavel
        df_formatado["CNPJ"] = df_empresas["CNPJ"]
        df_formatado["Proprietário (a)"] = df_empresas["Socios"].fillna(df_empresas["Razao Social"]).apply(limpar_nome)
        df_formatado["Celular"] = df_empresas["Telefones"]
        df_formatado["Email"] = df_empresas["E-mail"]
        df_formatado["Fonte"] = "Prospecção ativa"

        # Converter para .xlsx em memória
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df_formatado.to_excel(writer, index=False, sheet_name="Formatado")
        buffer.seek(0)

        st.success("✅ Arquivo formatado com sucesso!")
        st.download_button(
            label="📥 Baixar planilha formatada",
            data=buffer,
            file_name="Negocios_Formatado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

elif uploaded_file and not email_responsavel:
    st.warning("⚠️ Por favor, selecione quem está validando os leads.")

# Atualização forçada para carregar novo favicon
