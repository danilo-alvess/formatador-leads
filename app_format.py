import streamlit as st
import hydralit_components as hc
import pandas as pd
import time

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
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    footer { visibility: hidden; }
    .adm-footer { text-align:center; color:#999; font-size:0.8rem; margin-top:2rem; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# NAVBAR SUPERIOR
# ---------------------------
tabs = [
    {"icon": "📁", "label": "Formatação"},
    {"icon": "✅", "label": "Validação"},
    {"icon": "📊", "label": "Dashboard"},
]

chosen_tab = hc.option_bar(
    option_definition=tabs,
    title="",
    key="MainNav",
    override_theme={
        'txc_inactive': 'black',
        'menu_background': '#F4F7FC',
        'txc_active': 'white',
        'option_active': '#025E73'
    },
    horizontal_orientation=True
)

# ---------------------------
# ABA 1 - FORMATAÇÃO DE LEADS
# ---------------------------
if chosen_tab == "Formatação":
    st.title("📁 Formatador de Planilhas - ADM Soluções")
    st.markdown("Envie a planilha bruta exportada do site **Casa dos Dados** e gere automaticamente o formato padrão para validação.")
    
    uploaded_file = st.file_uploader("📎 Enviar planilha bruta (.xlsx)", type=["xlsx"])
    
    if uploaded_file:
        st.success("✅ Planilha carregada com sucesso!")
        # Simulação de processamento
        with st.spinner("Formatando planilha..."):
            time.sleep(2)
        st.download_button("📥 Baixar planilha formatada", data=b"fake", file_name="Formatado.xlsx")

# ---------------------------
# ABA 2 - VALIDAÇÃO
# ---------------------------
elif chosen_tab == "Validação":
    st.title("✅ Validação de Leads")
    st.markdown("Carregue a planilha formatada e gere uma nova com **apenas os leads validados**.")
    
    uploaded_file = st.file_uploader("📎 Enviar planilha validada (.xlsx)", type=["xlsx"])
    
    if uploaded_file:
        # Exemplo de contagem
        total = 100
        validados = 37
        st.metric("Total de Leads", total)
        st.metric("Validados", validados)
        st.progress(validados / total)
        st.download_button("📥 Baixar apenas validados", data=b"fake", file_name="Validados.xlsx")

# ---------------------------
# ABA 3 - DASHBOARD
# ---------------------------
elif chosen_tab == "Dashboard":
    st.title("📊 Painel de Acompanhamento")
    st.markdown("Visualize o progresso geral das validações de leads.")
    chart_data = pd.DataFrame({
        "Status": ["Validados", "Não Validados"],
        "Quantidade": [37, 63]
    })
    st.bar_chart(chart_data.set_index("Status"))

# ---------------------------
# RODAPÉ
# ---------------------------
st.markdown(
    '<div class="adm-footer">© 2025 ADM Soluções • Desenvolvido por Danilo Alves</div>',
    unsafe_allow_html=True
)
