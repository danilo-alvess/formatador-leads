import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.responsaveis import responsaveis

@st.cache_data
def carregar_planilha(uploaded_file):
    return pd.read_excel(uploaded_file)

def pagina_formatacao():
    st.title("🧩 Formatação de Leads")
    st.write("Envie a planilha original para gerar a versão formatada automaticamente.")

    uploaded_file = st.file_uploader("📎 Enviar planilha (.xlsx)", type=["xlsx"])
    responsavel = st.selectbox("👤 Selecione o responsável", list(responsaveis.keys()))

    if uploaded_file and responsavel != "Selecione o responsável":
        df = carregar_planilha(uploaded_file)

        # Exemplo simples de formatação
        df["Fonte"] = "Prospecção ativa"
        df["Etapa do negócio"] = "prospect"

        primeiro_nome = responsavel.split()[0]
        agora = datetime.now(ZoneInfo("America/Fortaleza"))
        hora_formatada = agora.strftime("%H.%M")
        data_formatada = agora.strftime("%d.%m")

        nome_arquivo = f"Lista Formatada - {primeiro_nome} ({hora_formatada}-{data_formatada}).xlsx"

        # Download
        output = BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)

        st.success("✅ Planilha formatada com sucesso!")
        st.download_button(
            label="📥 Baixar planilha formatada",
            data=output,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
