import re
import time
import config
import streamlit as st

# Importa as classes App, KPI e dbConfig
from src.App      import App
from src.KPI      import KPI
from src.dbConfig import dbConfig

# Instancia os objetos principais do banco de dados e do aplicativo
db = dbConfig()
app = App()
kpi = KPI()

if 'btn_consolidacao' in st.session_state and st.session_state.btn_consolidacao == True:
    st.session_state.running = True
else:
    st.session_state.running = False

lista_empresas = db.busca_empresas("empresas")
if 'cnes' not in st.session_state:
    st.session_state['cnes'] = st.query_params.cnes if 'cnes' in st.query_params else None
empresa_selecionada = [lista_empresas.index(l) for l in lista_empresas if re.search(r"\d+", l).group() == st.session_state['cnes']]

# Container principal para o título da aplicação
with st.container():    
    st.title("Consolidação de Indicadores")

# Container para seleção de empresa e exibição de consolidações
with st.container():
    # Cria um dropdown para selecionar a empresa
    box_empresa = st.selectbox( placeholder="Selecione a empresa",
                                label="Empresa:",
                                options=lista_empresas,
                                index=empresa_selecionada[0] if empresa_selecionada else None )
    
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
        with st.empty():
            with st.container():
                    lista_anos, lista_meses = db.busca_consolidacoes_disponiveis( nome_colecao="metricas",
                                                                                  cnes=cd_cnes )
                    if not lista_anos:
                        info = "Nenhum dado encontrado para esta empresa. Acesse Envio de Métricas para enviar dados."
                        st.warning(info, icon="ℹ️")
                    else:
                        # Cria duas colunas para selecionar ano e mês da consolidação
                        col1, col2 = st.columns(2)
                        
                        # Dropdown para selecionar o ano
                        with col1:
                            valor_ano = st.selectbox( placeholder="Selecione o ano",
                                                      label="Ano:",
                                                      options=lista_anos,
                                                      key='valor_ano',
                                                      index=None )
                        
                        # Dropdown para selecionar o mês
                        with col2:
                            valor_mes = st.selectbox( placeholder="Selecione o mês",
                                                      label="Mês:",
                                                      options=[config.MONTH_MASK[lista_meses[i]] for i in range(len(lista_meses))],
                                                      key='valor_mes',
                                                      index=None )     
                            
                        # Botão para iniciar a consolidação
                        if st.button(label="Consolidar", disabled=st.session_state.running, key='btn_consolidacao', use_container_width=True ): 
                            with st.empty():
                                with st.container():          
                                    with st.spinner(text="Consolidando..."):                                        
                                        # Obtém métricas da empresa para o ano e mês selecionados
                                        metricas = db.busca_metricas( nome_colecao="metricas",
                                                                    query={ "cd_cnes": int(cd_cnes),
                                                                            "ano": int(valor_ano),
                                                                            "mes": app.busca_chave_pelo_valor(dicionario=config.MONTH_MASK, valor=valor_mes) } )    
                                        
                                        # Cria um DataFrame a partir dos dados obtidos
                                        dataframe = app.cria_dataframe( dados=metricas )
                                        
                                        # Realiza cálculos de consolidação com base no DataFrame
                                        query_resultados = app.calcular( dados=dataframe )
                                        
                                        # Salva os resultados no banco de dados
                                        status_registro = db.carrega_dados( nome_colecao="resultados_kpis",
                                                                query=query_resultados )                              
                                        if status_registro:
                                            ultimos_resultados = db.busca_ultimos_resultados( nome_colecao="resultados_kpis", 
                                                                                            cnes=int(cd_cnes),
                                                                                            ano_atual=int(valor_ano),
                                                                                            mes_atual=app.busca_chave_pelo_valor(dicionario=config.MONTH_MASK, valor=valor_mes) )
                                            
                                            variacao_mensal = kpi.calcula_variacao_mensal( dados_resultado=ultimos_resultados )
                                            status_variacao = db.atualiza_variacao_mensal( nome_colecao="resultados_kpis", 
                                                                                        cnes=int(cd_cnes),
                                                                                        ano=int(valor_ano),
                                                                                        mes=app.busca_chave_pelo_valor(dicionario=config.MONTH_MASK, valor=valor_mes),
                                                                                        dados=variacao_mensal )
                                        
                                    # Exibe notificações de sucesso ou erro com base no status
                                    if all(i == True for i in status_variacao):
                                        st.info(f'Concluído!', icon="✅")
                                        db.busca_ultima_consolidacao.clear()  # Limpa o cache da função para dados atualizados
                                        time.sleep(2)
                                        st.rerun()
                                    elif any(i == True for i in status_variacao):
                                        st.info(f'Concluída primeira consolidação!', icon="✅")
                                        db.busca_ultima_consolidacao.clear()  # Limpa o cache da função para dados atualizados
                                        time.sleep(2)
                                        st.rerun()
                                    else:
                                        st.error('Ocorreu um erro!', icon="☠️")
                                        db.busca_ultima_consolidacao.clear()  # Limpa o cache da função para dados atualizados                                        
