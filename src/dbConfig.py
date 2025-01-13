import pandas as pd
import pymongo as db
import streamlit as st
import config

class dbConfig(object):
    """
    Classe para gerenciar a configuração e operações do banco de dados MongoDB.
    """
    def __init__(self):
        """
        Inicializa a configuração do banco de dados usando as variáveis armazenadas em Streamlit secrets.
        """
        self.conn_string = st.secrets.database.MONGO_URI
        self.database = st.secrets.database.DATABASE

    def validar_query(self, dicionario: dict, chaves_obrigatorias: list) -> bool:
        """
        Valida se o dicionário contém todas as chaves obrigatórias e se os valores não são nulos.

        Args:
            dicionario (dict): Dicionário a ser validado.
            chaves_obrigatorias (list): Lista de chaves obrigatórias.

        Returns:
            bool: True se o dicionário for válido.

        Raises:
            ValueError: Se o dicionário estiver vazio ou se algum valor for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """
        if not dicionario:
            raise ValueError("O dicionário não pode estar vazio.")
        
        for chave in chaves_obrigatorias:
            if chave not in dicionario:
                raise KeyError(f"A chave '{chave}' está ausente.")
        
        for chave in chaves_obrigatorias:
            if dicionario[chave] is None:
                raise ValueError(f"O valor da chave '{chave}' não pode ser nulo.")
        
        return True

    def get_metrics(self, collection_name: str, query: dict) -> dict:
        """
        Recupera métricas do banco de dados com base em uma consulta.

        Args:
            collection_name (str): Nome da coleção MongoDB.
            query (dict): Filtros da consulta.

        Returns:
            dict: Documento retornado pela consulta.

        Raises:
            ValueError: Se parâmetros forem inválidos.
            Exception: Se ocorrer erro ao recuperar o documento.
        """
        chaves_obrigatorias = ["organization_cnes", "year", "month"]
        if not collection_name or not query:
            raise ValueError("Os parâmetros não podem estar vazios.")
        
        if self.validar_query(query, chaves_obrigatorias):
            if type(query["organization_cnes"]) is not int:
                raise ValueError("Tipo da chave 'organization_cnes' incorreto. Esperado int.")
            if type(query["year"]) is not int:
                raise ValueError("Tipo da chave 'year' incorreto. Esperado int.")
            if type(query["month"]) is not int:
                raise ValueError("Tipo da chave 'month' incorreto. Esperado int.")
            try:
                client = db.MongoClient(self.conn_string)
                database = client.get_database(self.database)
                collection = database.get_collection(collection_name)
                metrics = collection.find_one(query)
                client.close()
            except Exception as e:
                raise Exception("Unable to retrieve the document due to the following error: ", e)
            if not metrics:
                raise Exception("Collection not found.")
            else:
                return metrics

    @st.cache_data(show_spinner=False)
    def get_organizations(_self, collection_name: str) -> dict:
        """
        Recupera organizações ativas do banco de dados.

        Args:
            collection_name (str): Nome da coleção MongoDB.

        Returns:
            dict: Lista de organizações ativas formatadas.

        Raises:
            Exception: Se ocorrer erro ao recuperar os documentos.
        """
        query = {"status": "Active"}
        try:
            client = db.MongoClient(_self.conn_string)
            database = client.get_database(_self.database)
            collection = database.get_collection(collection_name)
            organizations = collection.find(query)
            names = [f"{i['name']} ({i['cnes']})" for i in organizations]
            client.close()
        except Exception as e:
            raise Exception("Unable to retrieve the document due to the following error: ", e)
        return names

    @st.cache_data(show_spinner=False)
    def get_last_consolidation(_self, collection_name: str, cnes: int) -> list:
        """
        Recupera o último registro de consolidação de dados com base no CNES.

        Args:
            collection_name (str): Nome da coleção MongoDB.
            cnes (int): CNES da organização.

        Returns:
            list: Dados do último registro encontrado.

        Raises:
            IndexError: Se não houver resultados.
            Exception: Se ocorrer erro ao recuperar os documentos.
        """
        query = {"organization_cnes": int(cnes)}
        fields = {"year": 1, "month": 1, "_id": 0}
        sorting = [("year", db.DESCENDING), ("month", db.DESCENDING)]
        try:
            client = db.MongoClient(_self.conn_string)
            database = client.get_database(_self.database)
            collection = database.get_collection(collection_name)
            last_consolidation = collection.find(query, fields).sort(sorting)
            year_month = last_consolidation.to_list()[0]
            client.close()
        except IndexError:
            return None
        except Exception as e:
            raise Exception("Unable to retrieve the document due to the following error: ", e)
        return year_month

    def load_data(self, collection_name: str, query: dict) -> bool:
        """
        Insere dados no banco de dados.

        Args:
            collection_name (str): Nome da coleção MongoDB.
            query (dict): Dados a serem inseridos.

        Returns:
            bool: Confirmação da operação.

        Raises:
            ValueError: Se parâmetros forem inválidos.
            Exception: Se ocorrer erro ao inserir os documentos.
        """
        chaves_obrigatorias = ['organization_cnes', 'year', 'month', 'data']
        if not collection_name or not query:
            raise ValueError("Os parâmetros não podem estar vazios.")
        if self.validar_query(query, chaves_obrigatorias):
            if type(query["organization_cnes"]) is not int:
                raise ValueError("Tipo da chave 'organization_cnes' incorreto. Esperado int.")
        try:
            client = db.MongoClient(self.conn_string)
            database = client.get_database(self.database)
            collection = database.get_collection(collection_name)
            result = collection.insert_one(query)
            client.close()
        except Exception as e:
            raise Exception("Unable to retrieve the document due to the following error: ", e)
        if not result.acknowledged:
            raise Exception("DB return missing.")
        else:
            return result.acknowledged

    def upload_arquivo(self, dataframe: pd.DataFrame, collection_name: str) -> tuple[bool, str]:
        """
        Faz upload de um DataFrame para a coleção MongoDB.

        Args:
            dataframe (pd.DataFrame): DataFrame a ser inserido.
            collection_name (str): Nome da coleção MongoDB.

        Returns:
            tuple: Sucesso da operação e número de registros inseridos.

        Raises:
            Exception: Se ocorrer erro ao inserir os dados.
        """
        if dataframe:
            query = dataframe.to_dict(orient='records')
            try:
                client = db.MongoClient(config.MONGO_URI)
                database = client.get_database(config.DATABASE)
                collection = database.get_collection(collection_name)
                if len(query) == 1:
                    inserted_data = collection.insert_one(query)
                    registers_num = len(inserted_data.inserted_id)
                else:
                    inserted_data = collection.insert_many(query)
                    registers_num = len(inserted_data.inserted_ids)
                client.close()
                return inserted_data.acknowledged, str(registers_num)
            except:
                error = "Unable to insert data due to a internal server error"
                return False, error
        else:
            return False, "Dados inválidos"

    @st.cache_data(show_spinner=False)
    def get_summary(_self, organization_cnes: int, year: int):
        """
        Recupera resumo de métricas e resultados com base em CNES e ano.

        Args:
            organization_cnes (int): CNES da organização.
            year (int): Ano da consulta.

        Returns:
            tuple: Métricas e resultados encontrados.

        Raises:
            Exception: Se ocorrer erro ao recuperar os documentos.
        """
        query = {"organization_cnes": organization_cnes, "year": year}
        fields = {"year": 1, "month": 1, "_id": 0}
        try:
            client = db.MongoClient(_self.conn_string)
            database = client.get_database(_self.database)
            col_results = database.get_collection("kpi_results")
            find_results = col_results.find(query, fields)
            results = find_results.to_list()

            col_metrics = database.get_collection("metrics")
            find_metrics = col_metrics.find(query, fields)
            metrics = find_metrics.to_list()

            client.close()
        except Exception as e:
            raise Exception("Unable to retrieve the document due to the following error: ", e)

        return metrics, results
