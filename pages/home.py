import re
import streamlit as st

# Importa as classes App e dbConfig
from src.App import App
from src.dbConfig import dbConfig

# Instancia objetos para a aplicação principal e para a configuração do banco de dados
app = App()
db = dbConfig()

# Define o título principal da página
st.title("Início")

# Cria um contêiner para organizar os elementos da interface
with st.container():
    # Define duas colunas
    col1, col2 = st.columns([3, 4], vertical_alignment='bottom')
        
    with col1:
        st.header("Resumo")
    
    with col2:
        col11, col12 = st.columns([5,3], vertical_alignment='center')
        
        # Primeiro filtro: seleção de organização (empresa)
        filtro_empresa = col11.selectbox(
            placeholder="Selecione a empresa",
            label="Empresa:",
            options=db.busca_empresas("empresas"),
            label_visibility="collapsed",
            index=None
        )
        
        # Segundo filtro: controle segmentado para seleção do ano
        filtro_ano = col12.segmented_control(
            "Ano",
            options=[2023, 2024],
            label_visibility="collapsed"
        )

# Espaço reservado para exibir informações dinâmicas ou resultados
with st.empty():
    with st.container():
        # Verifica se os filtros de organização e ano foram selecionados
        if not filtro_empresa or not filtro_ano:
            # Exibe uma mensagem informativa caso os filtros não estejam preenchidos
            st.info("Selecione a empresa e o ano", icon="ℹ️")
        else:
            # Extrai o código CNES (identificador da organização) da seleção usando regex
            cd_cnes = re.search(r"\d+", filtro_empresa).group()

            # Exibe um spinner enquanto os dados são carregados
            with st.spinner(text="Carregando..."):
                # Recupera os dados de métricas e resultados do banco de dados
                metricas_bruto, resultados_bruto = db.busca_resumo(
                    cd_cnes=int(cd_cnes),
                    ano=int(filtro_ano)
                )
                
                # Monta o histórico dos dados utilizando um método da classe App
                historico = app.monta_historico(
                    dados_metricas=metricas_bruto,
                    dados_resultados=resultados_bruto
                )
                
                if (historico.empty):
                    info = f"Sem dados para exibir"
                    st.info(info, icon="ℹ️")
                else:
                    # Exibe os dados em uma tabela
                    st.data_editor(
                        data=historico,
                        use_container_width=True,
                        disabled=True,
                        hide_index=True
                    )
