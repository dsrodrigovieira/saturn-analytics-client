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
        self.string_conexao = st.secrets.database.MONGO_URI
        self.banco = st.secrets.database.DATABASE

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

    def busca_metricas(self, nome_colecao: str, query: dict) -> dict:
        """
        Recupera métricas do banco de dados com base em uma consulta.

        Args:
            nome_colecao (str): Nome da coleção MongoDB.
            query (dict): Filtros da consulta.

        Returns:
            dict: Documento retornado pela consulta.

        Raises:
            ValueError: Se parâmetros forem inválidos.
            Exception: Se ocorrer erro ao recuperar o documento.
        """
        chaves_obrigatorias = ["cd_cnes", "ano", "mes"]
        if not nome_colecao or not query:
            raise ValueError("Os parâmetros não podem estar vazios.")
        
        if self.validar_query(query, chaves_obrigatorias):
            if type(query["cd_cnes"]) is not int:
                raise ValueError("Tipo da chave 'cd_cnes' incorreto. Esperado int.")
            if type(query["ano"]) is not int:
                raise ValueError("Tipo da chave 'ano' incorreto. Esperado int.")
            if type(query["mes"]) is not int:
                raise ValueError("Tipo da chave 'mes' incorreto. Esperado int.")
            try:
                cursor = db.MongoClient(self.string_conexao)
                banco = cursor.get_database(self.banco)
                colecao = banco.get_collection(nome_colecao)
                metricas = colecao.find_one(query)
                cursor.close()
            except Exception as e:
                raise Exception("Não foi possível recuperar o documento devido ao seguinte erro: ", e)
            if not metricas:
                raise Exception("Coleção não encontrada.")
            else:
                return metricas

    @st.cache_data(show_spinner=False)
    def busca_empresas(_self, nome_colecao: str) -> list:
        """
        Recupera organizações ativas do banco de dados.

        Args:
            nome_colecao (str): Nome da coleção MongoDB.

        Returns:
            list: Lista de organizações ativas formatadas.

        Raises:
            Exception: Se ocorrer erro ao recuperar os documentos.
        """
        query = {"status": "Ativo"}
        try:
            cursor = db.MongoClient(_self.string_conexao)
            banco = cursor.get_database(_self.banco)
            colecao = banco.get_collection(nome_colecao)
            empresas = colecao.find(query)
            lista_empresas = [f"{empresa['nome']} ({empresa['cd_cnes']})" for empresa in empresas]
            cursor.close()
        except Exception as e:
            raise Exception("Não foi possível recuperar o documento devido ao seguinte erro: ", e)
        return lista_empresas


    @st.cache_data(show_spinner=False)
    def busca_consolidacoes_disponiveis(_self, nome_colecao: str, cnes: int) -> tuple[list, list]:
        """
        Recupera anos e meses disponíveis para consolidar.

        Args:
            nome_colecao (str): Nome da coleção MongoDB.
            cnes (int): CNES da organização.

        Returns:
            tuple: Lista de anos e lista de meses.

        Raises:
            Exception: Se ocorrer erro ao recuperar os documentos.
        """
        query = {"cd_cnes": int(cnes)}
        campos = {"ano": 1, "mes": 1, "_id": 0}
        try:
            cursor = db.MongoClient(_self.string_conexao)
            banco = cursor.get_database(_self.banco)
            colecao = banco.get_collection(nome_colecao)
            metricas = colecao.find(query, campos)
            lista_metricas = list(metricas)
            cursor.close()
        except Exception as e:
            raise Exception("Não foi possível recuperar o documento devido ao seguinte erro: ", e)
        return list(pd.array([metrica['ano'] for metrica in lista_metricas]).unique()), [metrica['mes'] for metrica in lista_metricas]

    @st.cache_data(show_spinner=False)
    def busca_ultima_consolidacao(_self, nome_colecao: str, cnes: int) -> list:
        """
        Recupera o último registro de consolidação de dados com base no CNES.

        Args:
            nome_colecao (str): Nome da coleção MongoDB.
            cnes (int): CNES da organização.

        Returns:
            list: Dados do último registro encontrado.

        Raises:
            IndexError: Se não houver resultados.
            Exception: Se ocorrer erro ao recuperar os documentos.
        """
        query = {"cd_cnes": int(cnes)}
        campos = {"ano": 1, "mes": 1, "_id": 0}
        ordem = [("ano", db.DESCENDING), ("mes", db.DESCENDING)]
        try:
            cursor = db.MongoClient(_self.string_conexao)
            banco = cursor.get_database(_self.banco)
            colecao = banco.get_collection(nome_colecao)
            ultima_consolidacao = colecao.find(query, campos).sort(ordem)
            consolidacao = list(ultima_consolidacao)[0]
            cursor.close()
        except IndexError:
            return None
        except Exception as e:
            raise Exception("Não foi possível recuperar o documento devido ao seguinte erro: ", e)
        return consolidacao

    def carrega_dados(self, nome_colecao: str, query: dict) -> bool:
        """
        Insere dados no banco de dados.

        Args:
            nome_colecao (str): Nome da coleção MongoDB.
            query (dict): Dados a serem inseridos.

        Returns:
            bool: Confirmação da operação.

        Raises:
            ValueError: Se parâmetros forem inválidos.
            Exception: Se ocorrer erro ao inserir os documentos.
        """
        chaves_obrigatorias = ['cd_cnes', 'ano', 'mes', 'dados']
        if not nome_colecao or not query:
            raise ValueError("Os parâmetros não podem estar vazios.")
        if self.validar_query(query, chaves_obrigatorias):
            if type(query["cd_cnes"]) is not int:
                raise ValueError("Tipo da chave 'cd_cnes' incorreto. Esperado int.")
        try:
            cursor = db.MongoClient(self.string_conexao)
            banco = cursor.get_database(self.banco)
            colecao = banco.get_collection(nome_colecao)
            retorno = colecao.insert_one(query)
            cursor.close()
        except Exception as e:
            raise Exception("Não foi possível recuperar o documento devido ao seguinte erro: ", e)
        if not retorno.acknowledged:
            raise Exception("Retorno do banco de dados não encontrado.")
        else:
            return retorno.acknowledged

    def upload_arquivo(self, dataframe: pd.DataFrame, nome_colecao: str) -> tuple[bool, str]:
        """
        Faz upload de um DataFrame para a coleção MongoDB.

        Args:
            dataframe (pd.DataFrame): DataFrame a ser inserido.
            nome_colecao (str): Nome da coleção MongoDB.

        Returns:
            tuple: Sucesso da operação e número de registros inseridos.

        Raises:
            Exception: Se ocorrer erro ao inserir os dados.
        """
        if not dataframe.empty:
            query = dataframe.to_dict(orient='records')
            try:
                cursor = db.MongoClient(self.string_conexao)
                banco = cursor.get_database(self.banco)
                colecao = banco.get_collection(nome_colecao)
                if len(query) == 1:
                    dados_inseridos = colecao.insert_one(query[0])
                    numero_registros = 1
                else:
                    dados_inseridos = colecao.insert_many(query)
                    numero_registros = len(dados_inseridos.inserted_ids)
                cursor.close()
                return dados_inseridos.acknowledged, str(numero_registros)
            except Exception as e:
                error = f"Não foi possível salvar os dados devido erro interno do servidor. {e}"
                return False, error
        else:
            return False, "Dados inválidos"

    @st.cache_data(show_spinner=False)
    def busca_resumo(_self, cd_cnes: int, ano: int):
        """
        Recupera resumo de métricas e resultados com base em CNES e ano.

        Args:
            cd_cnes (int): CNES da organização.
            ano (int): Ano da consulta.

        Returns:
            tuple: Métricas e resultados encontrados.

        Raises:
            Exception: Se ocorrer erro ao recuperar os documentos.
        """
        query = {"cd_cnes": cd_cnes, "ano": ano}
        campos = {"ano": 1, "mes": 1, "_id": 0}
        try:
            cursor = db.MongoClient(_self.string_conexao)
            banco = cursor.get_database(_self.banco)
            colecao_resultados = banco.get_collection("resultados_kpis")
            resultados = colecao_resultados.find(query, campos)
            lista_resultados = list(resultados)

            colecao_metricas = banco.get_collection("metricas")
            metricas = colecao_metricas.find(query, campos)
            lista_metricas = list(metricas)

            cursor.close()
        except Exception as e:
            raise Exception("Não foi possível recuperar o documento devido ao seguinte erro: ", e)

        return lista_metricas, lista_resultados

    def busca_ultimos_resultados(self, nome_colecao: str, cnes: int, ano_atual: int, mes_atual: int) -> list:
        """
        Recupera os resultados do mês que está sendo consolidado e do anterior.

        Args:
            nome_colecao (str): Nome da coleção MongoDB.
            cnes (int): CNES da organização.
            ano_atual (int): Ano da consulta.
            mes_atual (int): Mês da consulta.

        Returns:
            list: Objetos mongoDB dos resultados dos meses encontrado.

        Raises:
            IndexError: Se não houver resultados.
            Exception: Se ocorrer erro ao recuperar os documentos.
        """

        if mes_atual == 1:
            mes_anterior = 12
            ano_anterior = ano_atual-1
        else:
            mes_anterior = mes_atual-1
            ano_anterior = ano_atual
            
        query = {"cd_cnes": int(cnes),
                 "$or": [ {"ano": int(ano_atual), "mes": int(mes_atual)},
                          {"ano": int(ano_anterior), "mes": int(mes_anterior)} ]}
        try:
            cursor = db.MongoClient(self.string_conexao)
            banco = cursor.get_database(self.banco)
            colecao = banco.get_collection(nome_colecao)
            resultado_kpis = colecao.find(query)
            resultados = resultado_kpis.to_list()
            cursor.close()
            return resultados
        except Exception as e:
            raise Exception(f"Não foi possível recuperar o documento devido ao seguinte erro: {e}")
        
    def atualiza_variacao_mensal(self, nome_colecao: str, cnes: int, ano: int, mes: int, dados:list) -> tuple[bool, bool]:
        """
        Atualiza os resultados dos KPIs de determinado mês com o tipo de variação dos valores entre meses.

        Args:
            nome_colecao (str): Nome da coleção MongoDB.
            cnes (int): CNES da organização.
            ano (int): Ano da competência a ser atualizada.
            mes (int): Mês da competência a ser atualizada.
            dados (list): Dados a serem atualizados.

        Returns:
            list[bool,bool]: Confirmação da operação.

        Raises:
            IndexError: Se não houver resultados.
            Exception: Se ocorrer erro ao recuperar os documentos.
        """

        # validacao
        if len(dados) == 0:
            return True, False
        if len(dados) != 14:
            raise Exception("A quantidade de dados a serem atualizados é inválida.")
        aux_lista = []
        for item in dados:
            aux_lista.extend(list(item.keys()))
        if not all(chave in pd.Series(aux_lista).unique() for chave in ['index', 'variacao']):
            raise Exception("Os dados a serem atualizados são inválidos.")

        query = {"cd_cnes": int(cnes),
                "ano": int(ano),
                "mes": int(mes)}
        registros_encontrados = 0
        registros_atualizados = 0

        try:
            cursor = db.MongoClient(self.string_conexao)
            banco = cursor.get_database(self.banco)
            colecao = banco.get_collection(nome_colecao)
            for i,j in enumerate(dados):
                upd = {"$set": {f"dados.{j['index']}.variacao": int(j['variacao'])}}
                resultado_atualizacao = colecao.update_one(query,upd)
                registros_encontrados = registros_encontrados + resultado_atualizacao.matched_count
                registros_atualizados = registros_atualizados + resultado_atualizacao.modified_count
            cursor.close()
            return True, True
        except Exception as e:
            raise Exception(f"Não foi possível recuperar o documento devido ao seguinte erro: {e}")
        
