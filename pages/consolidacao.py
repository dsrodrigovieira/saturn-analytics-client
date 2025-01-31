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
    box_empresa = st.selectbox( placeholder="Selecione a empresa",
                                label="Empresa:",
                                options=db.busca_empresas(nome_colecao="empresas"),
                                index=None
                               )
    
    # Verifica se uma empresa foi selecionada
    if box_empresa:
        # Extrai o código CNES da empresa usando regex
        cd_cnes = re.search(r"\d+", box_empresa).group()
        
        with st.empty():
            with st.container():          
                with st.spinner(text="Carregando..."):
                    # Obtém a última consolidação da empresa selecionada
                    ultima_consolidacao = db.busca_ultima_consolidacao( nome_colecao="resultados_kpis",
                                                                        cnes=cd_cnes )
                    
                    # Exibe informações sobre a última consolidação
                    if ultima_consolidacao:
                        info = f"Último mês consolidado: {config.MONTH_MASK[ultima_consolidacao['mes']]} de {ultima_consolidacao['ano']}"
                        st.info(info, icon="ℹ️")
                    else:
                        # Exibe aviso caso nenhuma consolidação seja encontrada
                        info = "Nenhuma consolidação foi encontrada para esta empresa."
                        st.warning(info, icon="❕")

    # Cria duas colunas para selecionar ano e mês da consolidação
    col1, col2 = st.columns(2)
    
    # Dropdown para selecionar o ano
    with col1:
        valor_ano = st.selectbox( placeholder="Selecione o ano",
                                  label="Ano:",
                                  options=config.YEARS,
                                  index=None
                                )
    
    # Dropdown para selecionar o mês
    with col2:
        valor_mes = st.selectbox( placeholder="Selecione o mês",
                                  label="Mês:",
                                  options=config.MONTH_MASK.values(),
                                  index=None
                                )        

    # Botão para iniciar a consolidação
    if st.button(label="Consolidar", use_container_width=True):            
        # Exibe uma notificação de progresso
        st.toast("Consolidando...", icon="\u231B")
        
        # Obtém métricas da empresa para o ano e mês selecionados
        metricas = db.busca_metricas( nome_colecao="metricas",
                                      query={ "cd_cnes": int(cd_cnes),
                                              "ano": int(valor_ano),
                                              "mes": app.busca_chave_pelo_valor(dicionario=config.MONTH_MASK, valor=valor_mes) } )    
        
        # Cria um DataFrame a partir dos dados obtidos
        dataframe = app.cria_dataframe(dados=metricas)
        
        # Realiza cálculos de consolidação com base no DataFrame
        query_resultados = app.calcular(dados=dataframe)
        
        # Salva os resultados no banco de dados
        status = db.carrega_dados(nome_colecao="resultados_kpis", query=query_resultados)  
        
        # Exibe notificações de sucesso ou erro com base no status
        if status:
            st.toast(f'Concluído!', icon="✅")
            db.busca_ultima_consolidacao.clear()  # Limpa o cache da função para dados atualizados
            st.rerun()
        else:
            st.toast('Ocorreu um erro!', icon="☠️")
