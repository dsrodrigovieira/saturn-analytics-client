import config
import streamlit as st
from src.App      import App
from src.dbConfig import dbConfig

app = App()
db = dbConfig()

st.title("Envio de métricas")
btn_dic_dados = st.button("Dicionário de dados")
uploaded_file = st.file_uploader( label="Selecione o arquivo",
                                  type='csv',
                                  help="Insira um arquivo no formato CSV para upload" )

if "download_csv_file" not in st.session_state:
    if btn_dic_dados:
        app.download_csv_file()

if uploaded_file:
    validacao, dados = app.valida_arquivo(arquivo=uploaded_file)
    if validacao:
        if st.button( label="Enviar dados",
                      icon=config.ICON_PAGE_ENVIO_METRICAS,
                      use_container_width=True ):
            st.toast( body="Fazendo upload do arquivo...",
                      icon="⌛" )            
            ack, var = db.upload_arquivo( dataframe=dados,
                                          collection_name="metrics" )
            if ack:
                st.toast( body=f'Upload concluído com sucesso! {var} registros incluídos',
                          icon="✅" )
            else:
                st.toast( body=f'Ocorreu um erro! {var}',
                          icon="☠️" )
    