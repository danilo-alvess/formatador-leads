import streamlit as st
import pandas as pd
import re
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="Leads - ADM Soluções",
    page_icon="https://raw.githubusercontent.com/danilo-alvess/formatador-leads/main/logo_adm.png"
)

st.image(
    "https://raw.githubusercontent.com/danilo-alvess/formatador-leads/main/banner_captacao.png",
    use_container_width=True
)

st.title("Formatador de Planilha de Leads")
st.header("ADM Soluções")
st.write("Envie a planilha bruta (.xlsx) exportada do site **Casa dos Dados** para gerar a versão formatada.")

st.markdown("### ⚠️ Importante:")
st.warning("Se estiver no celular, baixe a planilha primeiro para o dispositivo. Upload direto do Google Drive pode não funcionar.")

# Lista de responsáveis
responsaveis = {
    "Selecione o responsável": "",
    "Amanda Prudente": "amanda.p@admsolucoes.com.br",
    "Isabelle Alves": "isabelle.alves@admsolucoes.com.br",
    "Andressa Passos": "andressa.passos@admsolucoes.com.br",
    "Arthur Helber": "arthur.helber@admsolucoes.com.br",
    "Caio Gadelha": "caio.gadelha@admsolucoes.com.br",
    "Carlos Eduardo": "eduardo@admsolucoes.com.br",
    "Daina Lisboa": "daina.lisboa@admsolucoes.com.br",
    "Danilo Alves": "danilo.a@admsolucoes.com.br",
    "Elis Lima": "elis.lima@admsolucoes.com.br",
    "Gabriel Gentil": "gabriel.gentil@admsolucoes.com.br",
    "Gisele Marcelino": "gisele.marcelino@admsolucoes.com.br",
    "Lívia Pordeus": "livia.pordeus@admsolucoes.com.br",
    "Miguel Cassimiro": "miguel.cassimiro@admsolucoes.com.br",
    "Izamor Morais": "izamor.morais@admsolucoes.com.br",
    "Marianne Bezerra": "marianne.bezerra@admsolucoes.com.br",
    "Nicolas Veras": "nicolas.veras@admsolucoes.com.br",
    "Ryan Caliel": "caliel@admsolucoes.com.br",
    "Suzanne Santos": "suzanne.santos@admsolucoes.com.br",
    "Tércio da Costa": "tercio.costa@admsolucoes.com.br",
}

responsavel_opcoes = ["Selecione o responsável"] + sorted(
    [nome for nome in responsaveis.keys() if nome != "Selecione o responsável"]
)
responsavel = st.selectbox("Quem está validando os leads?", responsavel_opcoes)
email_responsavel = responsaveis[responsavel]

# Dicionário de quem será alocado para cada responsável
consultores_alocados = {
    "Gisele Marcelino": "brendo@admsolucoes.com.br",
    "Guilherme Andrade": "brendo@admsolucoes.com.br",
    "Vinícius Néo": "pedro.paiva@admsolucoes.com.br",
    "Arthur Helber": "eduardo@admsolucoes.com.br",
    "Daina Lisboa": "eduardo@admsolucoes.com.br",
    "Grazy Marcelino": "eduardo@admsolucoes.com.br"
}

uploaded_file = st.file_uploader("📁 Faça o upload da planilha bruta (.xlsx)", type=["xlsx"])

if uploaded_file and email_responsavel:
    try:
        df_empresas = pd.read_excel(uploaded_file, sheet_name="empresas")

        def limpar_nome(nome):
            return re.sub(r'[0-9.]', '', str(nome)).strip()

        def limpar_socios(s):
            s = str(s)
            s = re.sub(
                r"(?i)(Sócio Pessoa Jurídica Domiciliado no Exterior|Sócio-Administrador|Sócio|Administrador)\s*-\s*",
                "",
                s
            )
            return s.strip()

        df_formatado = pd.DataFrame()
        df_formatado["Nome da empresa"] = df_empresas["Razao Social"].apply(limpar_nome)
        df_formatado["Nome"] = df_empresas["Socios"].apply(limpar_socios)
        df_formatado["Número de telefone"] = df_empresas["Telefones"]
        df_formatado["Status"] = "Não Validado"
        df_formatado["Nome do negócio"] = df_empresas["Nome Fantasia"].fillna(df_empresas["Razao Social"])
        df_formatado["Etapa do negócio"] = "leads"
        df_formatado["Proprietário do negócio"] = email_responsavel

        email_consultor_alocado = consultores_alocados.get(responsavel, "")
        df_formatado["Consultor alocado"] = email_consultor_alocado

        df_formatado["Fonte"] = "Prospecção ativa"
        df_formatado["CNPJ"] = df_empresas["CNPJ"]
        df_formatado["E-mail"] = df_empresas["E-mail"]
        df_formatado["Fase do ciclo de vida"] = "Lead"
        df_formatado["Pipeline"] = "Pipeline de vendas"

        colunas_prioritarias = ["Nome da empresa", "Nome", "Número de telefone", "Status"]
        outras_colunas = [col for col in df_formatado.columns if col not in colunas_prioritarias]
        df_formatado = df_formatado[colunas_prioritarias + outras_colunas]

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df_formatado.to_excel(writer, index=False, sheet_name="Formatado")
        buffer.seek(0)

        # Formatação do número do pedido com 3 dígitos e hora/data
        agora = datetime.now()
        hora_formatada = agora.strftime("%H:%M")
        data_formatada = agora.strftime("%d/%m")

        # Monta o nome do arquivo
        nome_arquivo = f"Negócios Formatado - {responsavel} ({hora_formatada}.{data_formatada}).xlsx"

        st.success("✅ Arquivo formatado com sucesso!")
        st.download_button(
            label="📥 Clique aqui para baixar planilha formatada",
            data=buffer,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

elif uploaded_file and not email_responsavel:
    st.warning("⚠️ Por favor, selecione quem está validando os leads.")



