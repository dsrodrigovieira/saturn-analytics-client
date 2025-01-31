import config
import streamlit as st

# Importa as classes App e dbConfig
from src.App      import App
from src.dbConfig import dbConfig

# Instancia os objetos principais do aplicativo e da configuração do banco de dados
app = App()
db = dbConfig()

# Define o título do aplicativo na interface
st.title("Envio de métricas")

# Cria um botão para download do dicionário de dados
btn_dicionario_dados = st.button("Dicionário de dados")

# Cria um componente para upload de arquivo CSV
arquivo_carregado = st.file_uploader( label="Selecione o arquivo",
                                      type='csv',
                                      help="Insira um arquivo no formato CSV para upload" )

# Verifica se a chave "download_arquivo_csv" está no estado da sessão para controle da exibição do dialog
if "download_arquivo_csv" not in st.session_state:
    if btn_dicionario_dados:
        # Realiza o download do arquivo modelo
        app.download_arquivo_csv()

# Verifica se um arquivo foi carregado
if arquivo_carregado:
    # Valida o arquivo enviado
    validacao, dados = app.valida_arquivo(arquivo=arquivo_carregado)
    if validacao:
        # Cria um botão para enviar os dados validados
        if st.button( label="Enviar dados",
                      icon=config.ICON_PAGE_ENVIO_METRICAS,
                      use_container_width=True ):
            # Exibe uma mensagem de upload em andamento
            st.toast( body="Fazendo upload do arquivo...",
                      icon="⌛" )            
            # Realiza o upload do arquivo no banco de dados
            confirmacao, num_registros = db.upload_arquivo( dataframe=dados,
                                                            nome_colecao="metricas" )
            # Verifica se o upload foi bem-sucedido e exibe mensagens de feedback
            if confirmacao:
                st.toast( body=f'Upload concluído com sucesso! {num_registros} registros incluídos',
                          icon="✅" )
            else:
                st.toast( body=f'Ocorreu um erro! {num_registros}',
                          icon="☠️" )
