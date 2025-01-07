import pandas    as pd
import pymongo   as db
import streamlit as st
import config

class dbConfig (object):

    def __init__(self):
        self.conn_string = st.secrets.database.MONGO_URI
        self.database = st.secrets.database.DATABASE        
        pass

    def validar_query(self, dicionario:dict, chaves_obrigatorias:list) -> bool:
        # Validar se kwargs está vazio
        if not dicionario:
            raise ValueError("O dicionário não pode estar vazio.")
        
        # Validar se todas as chaves obrigatórias estão presentes
        for chave in chaves_obrigatorias:
            if chave not in dicionario:
                raise KeyError(f"A chave '{chave}' está ausente.")
        
        # Validar se os valores das chaves obrigatórias não são nulos
        for chave in chaves_obrigatorias:
            if dicionario[chave] is None:
                raise ValueError(f"O valor da chave '{chave}' não pode ser nulo.")
            
        # Retornar True se tudo estiver válido
        return True

    def get_metrics(self, collection_name:str, query:dict) -> dict:
        chaves_obrigatorias = [
            "organization_cnes",
            "year",
            "month"
        ]
        # Validar existência dos parâmetros
        if not collection_name or not query:
            raise ValueError("Os parametros não podem estar vazios.")
        
        if(self.validar_query(query,chaves_obrigatorias)):
            # Validar se os valores das chaves obrigatórias não são nulos
            if type(query["organization_cnes"]) is not int:
                raise ValueError(f"Tipo da chave 'organization_cnes' incorreto. Esperado int.")
            if type(query["year"]) is not int:
                raise ValueError(f"Tipo da chave 'year' incorreto. Esperado int.")
            if type(query["month"]) is not int:
                raise ValueError(f"Tipo da chave 'month' incorreto. Esperado int.")
            try:
                client = db.MongoClient(self.conn_string)
                database = client.get_database(self.database)
                collection = database.get_collection(collection_name)
                metrics = collection.find_one(query)
                client.close()
            except Exception as e:
                raise Exception("Unable to retrieve the document due to the following error: ", e)
            if (not metrics):
                raise Exception("Collection not found.")
            else:
                return metrics
        else:
            None

    @st.cache_data(show_spinner=False)
    def get_organizations(_self, collection_name:str) -> dict:           
        query = {"status":"Active"}
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
    def get_last_consolidation(_self, collection_name:str, cnes:int) -> list:           
        query = {"organization_cnes": int(cnes)}
        fields = {"year":1,"month":1,"_id":0}
        sorting = [("year",db.DESCENDING),("month",db.DESCENDING)]
        try:
            client = db.MongoClient(_self.conn_string)
            database = client.get_database(_self.database)
            collection = database.get_collection(collection_name)
            last_consolidation = collection.find(query,fields).sort(sorting)
            year_month = last_consolidation.to_list()[0]
            client.close()
        except IndexError:
            return None
        except Exception as e:
            raise Exception("Unable to retrieve the document due to the following error: ", e) 
        return year_month        

    def load_data(self, collection_name:str, query:dict) -> bool:
        chaves_obrigatorias = [
            'organization_cnes', 'year', 'month',
            'rkpi_1', 'rkpi_2', 'rkpi_3', 'rkpi_4', 'rkpi_5',
            'rkpi_6', 'rkpi_7', 'rkpi_8', 'rkpi_9', 'rkpi_10',
            'rkpi_11', 'rkpi_12', 'rkpi_13', 'rkpi_14'
        ]
        # Validar existência dos parâmetros
        if not collection_name or not query:
            raise ValueError("Os parametros não podem estar vazios.")
        if(self.validar_query(query,chaves_obrigatorias)):
            # Validar se os valores das chaves obrigatórias não são nulos
            if type(query["organization_cnes"]) is not int:
                raise ValueError(f"Tipo da chave 'organization_cnes' incorreto. Esperado int.")
        try:
            client = db.MongoClient(self.conn_string)
            database = client.get_database(self.database)
            collection = database.get_collection(collection_name)
            result = collection.insert_one(query)
            client.close()
        except Exception as e:
            raise Exception("Unable to retrieve the document due to the following error: ", e)
        if (not result.acknowledged):
            raise Exception("DB return missing.") 
        else:
            return result.acknowledged
        
    def upload_arquivo(self, dataframe:pd.DataFrame, collection_name:str) -> tuple[bool, str]:
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

        query = { "organization_cnes": organization_cnes,
                  "year": year }
        fields = {"year":1, "month":1, "_id":0}
        try:
            client = db.MongoClient(_self.conn_string)
            database = client.get_database(_self.database)
            col_results = database.get_collection("kpi_results")    
            find_results = col_results.find(query,fields)
            results = find_results.to_list()

            col_metrics = database.get_collection("metrics")    
            find_metrics = col_metrics.find(query,fields)
            metrics = find_metrics.to_list()
            
            client.close()
        except Exception as e:
            raise Exception("Unable to retrieve the document due to the following error: ", e)

        return metrics, results