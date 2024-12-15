import re
import streamlit as st
from src.App      import App
from src.dbConfig import dbConfig

app = App()
db = dbConfig()

st.title("Início")

with st.container():
    col1, col2 = st.columns([3,2], vertical_alignment='bottom')
    with col1:
        st.header("Resumo")
    with col2:
        col11, col12 = st.columns(2, vertical_alignment='center')
        filter_organization = col11.selectbox( placeholder="Selecione a empresa",
                                            label="Empresa:",
                                            options=db.get_organizations("organizations"),
                                            label_visibility="collapsed",
                                            index=None
                                        )
        filter_year = col12.segmented_control("Ano",options=[2023,2024],label_visibility="collapsed")

with st.empty():
    with st.container():
        if not filter_organization or not filter_year:
            st.info("Selecione a empresa e o ano", icon="ℹ️")
        else:
            organization_cnes = re.search(r"\d+",filter_organization).group()
            st.toast(f"{filter_year}, {organization_cnes}")
            with st.spinner(text="Carregando..."):
                raw_metrics, raw_results = db.get_summary(organization_cnes=int(organization_cnes),year=int(filter_year))
                historico = app.monta_historico(raw_metrics,raw_results)
                st.data_editor(
                    historico,
                    use_container_width=True,
                    disabled=True,
                    hide_index=True
                )
