import streamlit as st
import config

pages = {
    "App":[
        st.Page( page="pages/home.py",
                 title="Início",
                 icon=config.ICON_PAGE_HOME
                ),
        st.Page( page="pages/envioMetricas.py",
                 title="Envio de Métricas",
                 icon=config.ICON_PAGE_ENVIO_METRICAS
                ),                
        st.Page( page="pages/consolidacao.py",
                 title="Consolidação de Indicadores",
                 icon=config.ICON_PAGE_CONSOLIDACAO
                ),
    ]
}

st.logo(config.PATH_LOGO)
pg = st.navigation(pages)
pg.run()