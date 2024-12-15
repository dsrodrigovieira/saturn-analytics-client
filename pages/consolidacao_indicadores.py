import re
import config
import streamlit as st
from src.App      import App
from src.dbConfig import dbConfig

db = dbConfig()
app = App()

with st.container():    
    st.title("Consolidação de Indicadores")
    #st.write(":ringed_planet: Saturn Analytics")

with st.container():
    #st.subheader("Configuração")   
    box_organization = st.selectbox( placeholder="Selecione a empresa",
                                     label="Empresa:",
                                     options=db.get_organizations("organizations"),
                                     index=None
                                    )
    if box_organization:
        organization_cnes = re.search(r"\d+",box_organization).group()
        with st.empty():
            with st.container():          
                with st.spinner(text="Carregando..."):
                    last_consolidation = db.get_last_consolidation( collection_name="kpi_results",
                                                                    cnes=organization_cnes )
                    if last_consolidation:
                        info = f"Último mês consolidado: {config.MONTH_MASK[last_consolidation['month']]} de {last_consolidation['year']}"
                        st.info(info,icon="ℹ️")
                    else:
                        info = "Nenhuma consolidação foi encontrada para esta empresa."
                        st.warning(info,icon="❕")
    
    col1, col2 = st.columns(2)
    with col1:
        var_year = st.selectbox( placeholder="Selecione o ano",
                                 label="Ano:",
                                 options=config.YEARS,
                                 index=None
                                )
    with col2:
        var_month = st.selectbox( placeholder="Selecione o mês",
                                  label="Mês:",
                                  options=config.MONTH_MASK.values(),
                                  index=None
                                )        

    if st.button(label="Consolidar", use_container_width=True):            
        st.toast("Consolidando...",icon="⌛")
        metricas = db.get_metrics( collection_name="metrics",
                                    query= { "organization_cnes": int(organization_cnes),
                                             "year": int(var_year),
                                             "month": app.get_key_from_value(config.MONTH_MASK,var_month) } )    
        df = app.make_dataframe( data=metricas )
        result_query = app.calculate( df=df )
        status = db.load_data( collection_name="kpi_results",
                               query=result_query )              
        if status:
            st.toast(f'Concluído!',icon="✅")
            db.get_last_consolidation.clear()
        else:
            st.toast('Ocorreu um erro!',icon="☠️")