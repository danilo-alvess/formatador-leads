import streamlit as st
import hydralit_components as hc

# Configuração inicial
st.set_page_config(
    page_title="Formatador de Leads - ADM Soluções",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importa as abas (não processa ainda)
from pages.formatacao import pagina_formatacao
from pages.limpeza import pagina_limpeza

# Barra superior com abas
tabs = [
    {"icon": "🧩", "label": "FORMATAÇÃO"},
    {"icon": "🧹", "label": "LIMPEZA"},
]

chosen_tab = hc.option_bar(
    option_definition=tabs,
    title='',
    key='MainOptionx',
    horizontal_orientation=True,
    override_theme={'txc_inactive': 'black', 'menu_background': '#E7F0FF', 'txc_active': 'white', 'option_active': '#1E40AF'}
)

# Exibe aba correspondente
if chosen_tab == "FORMATAÇÃO":
    pagina_formatacao()
elif chosen_tab == "LIMPEZA":
    pagina_limpeza()

# Rodapé simples
st.markdown("---")
st.caption("Desenvolvido pela ADM Soluções 🚀")
