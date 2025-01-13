import streamlit as st
import config

# Dicionário que mapeia as páginas da aplicação
pages = {
    "App": [
        # Define a página inicial da aplicação
        st.Page(
            page="pages/home.py",
            title="Início",
            icon=config.ICON_PAGE_HOME
        ),
        # Define a página para envio de métricas
        st.Page(
            page="pages/envioMetricas.py",
            title="Envio de Métricas",
            icon=config.ICON_PAGE_ENVIO_METRICAS
        ),
        # Define a página para consolidação de indicadores
        st.Page(
            page="pages/consolidacao.py",
            title="Consolidação de Indicadores",
            icon=config.ICON_PAGE_CONSOLIDACAO
        ),
    ]
}

# Configura o logotipo da aplicação
st.logo(config.PATH_LOGO)

# Configura o sistema de navegação da aplicação com base no dicionário de páginas
pg = st.navigation(pages)

# Executa a página atualmente selecionada na navegação
pg.run()
