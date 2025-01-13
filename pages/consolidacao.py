import re
import config
import streamlit as st

# Importa as classes App e dbConfig
from src.App      import App
from src.dbConfig import dbConfig

# Instancia os objetos principais do banco de dados e do aplicativo
db = dbConfig()
app = App()

# Container principal para o título da aplicação
with st.container():    
    st.title("Consolidação de Indicadores")

# Container para seleção de empresa e exibição de consolidações
with st.container():
    # Cria um dropdown para selecionar a empresa
    box_organization = st.selectbox( placeholder="Selecione a empresa",
                                     label="Empresa:",
                                     options=db.get_organizations("organizations"),
                                     index=None
                                    )
    
    # Verifica se uma empresa foi selecionada
    if box_organization:
        # Extrai o código CNES da empresa usando regex
        organization_cnes = re.search(r"\d+", box_organization).group()
        
        with st.empty():
            with st.container():          
                with st.spinner(text="Carregando..."):
                    # Obtém a última consolidação da empresa selecionada
                    last_consolidation = db.get_last_consolidation( collection_name="kpi_results",
                                                                    cnes=organization_cnes )
                    
                    # Exibe informações sobre a última consolidação
                    if last_consolidation:
                        info = f"Último mês consolidado: {config.MONTH_MASK[last_consolidation['month']]} de {last_consolidation['year']}"
                        st.info(info, icon="ℹ️")
                    else:
                        # Exibe aviso caso nenhuma consolidação seja encontrada
                        info = "Nenhuma consolidação foi encontrada para esta empresa."
                        st.warning(info, icon="❕")

    # Cria duas colunas para selecionar ano e mês da consolidação
    col1, col2 = st.columns(2)
    
    # Dropdown para selecionar o ano
    with col1:
        var_year = st.selectbox( placeholder="Selecione o ano",
                                 label="Ano:",
                                 options=config.YEARS,
                                 index=None
                                )
    
    # Dropdown para selecionar o mês
    with col2:
        var_month = st.selectbox( placeholder="Selecione o mês",
                                  label="Mês:",
                                  options=config.MONTH_MASK.values(),
                                  index=None
                                )        

    # Botão para iniciar a consolidação
    if st.button(label="Consolidar", use_container_width=True):            
        # Exibe uma notificação de progresso
        st.toast("Consolidando...", icon="\u231B")
        
        # Obtém métricas da empresa para o ano e mês selecionados
        metricas = db.get_metrics( collection_name="metrics",
                                    query={ "organization_cnes": int(organization_cnes),
                                            "year": int(var_year),
                                            "month": app.get_key_from_value(config.MONTH_MASK, var_month) } )    
        
        # Cria um DataFrame a partir dos dados obtidos
        df = app.make_dataframe(data=metricas)
        
        # Realiza cálculos de consolidação com base no DataFrame
        result_query = app.calculate(df=df)
        
        # Salva os resultados no banco de dados
        status = db.load_data(collection_name="kpi_results", query=result_query)              
        
        # Exibe notificações de sucesso ou erro com base no status
        if status:
            st.toast(f'Concluído!', icon="✅")
            db.get_last_consolidation.clear()  # Limpa o cache da função para dados atualizados
        else:
            st.toast('Ocorreu um erro!', icon="☠️")
