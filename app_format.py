import streamlit as st
import hydralit_components as hc
import pandas as pd
import time
from io import BytesIO
import re
from datetime import datetime
from zoneinfo import ZoneInfo

# ---------------------------
# CONFIGURAÇÕES GERAIS
# ---------------------------
st.set_page_config(
    page_title="ADM Soluções - Leads",
    page_icon="https://raw.githubusercontent.com/danilo-alvess/formatador-leads/main/logo_adm.png",
    layout="wide"
)

# CSS customizado
st.markdown("""
    <style>
    

    /* Fundo da barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #11003a; /* Cor da sidebar */
    }

    /* Cor dos textos na sidebar */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Ajustes gerais */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    footer { visibility: hidden; }
    .adm-footer { text-align:center; color:#999; font-size:0.8rem; margin-top:2rem; }
    </style>
""", unsafe_allow_html=True)


# ---------------------------
# NAVBAR SUPERIOR
# ---------------------------
tabs = [
    {"icon": "🧾", "label": "FORMATAÇÃO"},
    {"icon": "🧹", "label": "LIMPEZA"},
    {"icon": "📊", "label": "Dashboard"},
]

chosen_tab = hc.option_bar(
    option_definition=tabs,
    title="",
    key="MainNav",
    override_theme={
        'txc_inactive': 'white',
        'menu_background': '#11003a',
        'txc_active': 'white',
        'option_active': '#d72929'
    },
    horizontal_orientation=True
)

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



# Dicionário de quem será alocado para cada responsável
consultores_alocados = {
    "Gisele Marcelino": "brendo@admsolucoes.com.br",
    "Guilherme Andrade": "brendo@admsolucoes.com.br",
    "Vinícius Néo": "pedro.paiva@admsolucoes.com.br",
    "Arthur Helber": "eduardo@admsolucoes.com.br",
    "Daina Lisboa": "eduardo@admsolucoes.com.br",
    "Grazy Marcelino": "eduardo@admsolucoes.com.br"
}


# ---------------------------
# ABA 1 - FORMATAÇÃO DE LEADS
# ---------------------------
if chosen_tab == "FORMATAÇÃO":
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
            agora = datetime.now(ZoneInfo("America/Fortaleza"))
            hora_formatada = agora.strftime("%H.%M")
            data_formatada = agora.strftime("%d.%m")

            # Monta o nome do arquivo
            primeiro_nome = responsavel.split()[0]  # pega só o primeiro nome
            nome_arquivo = f"Formatada - {primeiro_nome} ({hora_formatada}-{data_formatada}).xlsx"


            st.success("✅ Arquivo formatado com sucesso!")
            st.download_button(
            label="Download",
            data=buffer,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")

    elif uploaded_file and not email_responsavel:
        st.warning("⚠️ Por favor, selecione quem está validando os leads.")


# ---------------------------
# ABA 2 - LIMPEZA
# ---------------------------
elif chosen_tab == "LIMPEZA":
    st.markdown("")
    st.markdown("Carregue a planilha formatada e para poder gerar uma nova com **apenas os leads validados**.")

    @st.cache_data
    def limpar_planilha(uploaded_file_l):
        # Lê a planilha enviada
        df = pd.read_excel(uploaded_file_l)

        # ---- Ajuste aqui conforme o nome da coluna usada para validação ----
        colunas_validacao = [col.lower() for col in df.columns]
        if "status" in colunas_validacao:
            col_val = df.columns[colunas_validacao.index("status")]
            df_validados = df[df[col_val].str.lower() == "validado"]
        elif "validação" in colunas_validacao:
            col_val = df.columns[colunas_validacao.index("validação")]
            df_validados = df[df[col_val].str.lower() == "sim"]
        else:
            st.error("❌ Não foi encontrada nenhuma coluna de status de validação na planilha.")
            return None

        return df_validados

    # Upload dentro da aba correta
    uploaded_file_l = st.file_uploader("📎 Enviar planilha formatada (.xlsx)", type=["xlsx"])

    if uploaded_file_l:
        df_validados = limpar_planilha(uploaded_file_l)
        if df_validados is not None:
            st.success(f"✅ {len(df_validados)} leads validados encontrados!")

            if df_validados is not None and not df_validados.empty:
            # Dicionário invertido
                emails_para_nomes = {email: nome for nome, email in responsaveis.items()}

            # Pega o e-mail do primeiro lead validado
            email_dono = df_validados["Proprietário do negócio"].iloc[0]

            # Busca nome e primeiro nome
            nome_completo = emails_para_nomes.get(email_dono, "Responsável")
            primeiro_nome = nome_completo.split()[0]

            # Gera nome do arquivo com data e hora
            agora = datetime.now(ZoneInfo("America/Fortaleza"))
            hora_formatada = agora.strftime("%H.%M")
            data_formatada = agora.strftime("%d.%m")

            nome_arquivo = f"Validados - {primeiro_nome} ({hora_formatada}-{data_formatada}).xlsx"

            # Converte para bytes (para download)
            output = BytesIO()
            df_validados.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            # Gera arquivo e botão de download
            output = BytesIO()
            df_validados.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="Download",
                data=output,
                file_name=nome_arquivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# ---------------------------
# ABA 3 - DASHBOARD
# ---------------------------
elif chosen_tab == "Dashboard":
    st.markdown("### 📊 Dashboard")
    st.info("Área de visualização em desenvolvimento.")

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.image("Logos.png")
st.sidebar.title("Captação de Leads")
st.sidebar.button("Configurações")

# ---------------------------
# RODAPÉ
# ---------------------------
st.markdown(
    '<div class="adm-footer">© 2025 ADM Soluções • Desenvolvido por Danilenda</div>',
    unsafe_allow_html=True
)

