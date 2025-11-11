import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo
from utils.responsaveis import responsaveis

@st.cache_data
def carregar_planilha(uploaded_file):
    return pd.read_excel(uploaded_file)

def pagina_limpeza():
    st.title("🧹 Limpeza de Leads")
    st.write("Envie a planilha formatada para gerar uma nova apenas com os leads validados.")

    uploaded_file = st.file_uploader("📎 Enviar planilha formatada (.xlsx)", type=["xlsx"])

    if uploaded_file:
        df = carregar_planilha(uploaded_file)
        colunas = [c.lower() for c in df.columns]

        # Identifica coluna de status
        if "status" in colunas:
            col_val = df.columns[colunas.index("status")]
            df_validados = df[df[col_val].str.lower() == "validado"]
        else:
            st.error("❌ Coluna de status não encontrada.")
            return

        if df_validados.empty:
            st.warning("⚠ Nenhum lead validado encontrado.")
            return

        # Mapeia e-mail → nome
        emails_para_nomes = {email: nome for nome, email in responsaveis.items()}

        email_dono = df_validados["Proprietário do negócio"].iloc[0]
        nome_completo = emails_para_nomes.get(email_dono, "Responsável")
        primeiro_nome = nome_completo.split()[0]

        agora = datetime.now(ZoneInfo("America/Fortaleza"))
        hora_formatada = agora.strftime("%H.%M")
        data_formatada = agora.strftime("%d.%m")

        nome_arquivo = f"Leads Validados - {primeiro_nome} ({hora_formatada}-{data_formatada}).xlsx"

        # Download
        output = BytesIO()
        df_validados.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)

        st.success(f"✅ {len(df_validados)} leads validados encontrados!")
        st.download_button(
            label="📥 Baixar leads validados",
            data=output,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
