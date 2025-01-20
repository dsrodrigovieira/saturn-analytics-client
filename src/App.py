import pandas as pd
import streamlit as st
from src.KPI import KPI

class App(object):
    """
    Classe que gerencia o aplicativo de KPIs, incluindo carregamento de dados, validação, cálculos e exibição de resultados.
    """

    def __init__(self):
        """
        Inicializa o objeto da classe App com uma instância de KPI e variáveis de controle para os KPIs.
        """
        self.kpi = KPI()
        self._1_proporcao_partos_vaginais = None
        self._2_proporcao_reinternacoes_30_dias = None
        self._3_taxa_pcr = None
        self._4_taxa_mortalidade = None
        self._5_tempo_medio_internacao = None
        self._6_tempo_medio_emergencia = None
        self._7_tempo_medio_espera_emergencia = None
        self._8_taxa_atb_profilatico = None
        self._9_taxa_infeccao_cirurgia_limpa = None
        self._10_incidencia_ipcs_cvc = None
        self._11_incidencia_itu_cvd = None
        self._12_taxa_profilaxia_tromboembolismo = None
        self._13_incidencia_queda = None
        self._14_evento_sentinela = None
        pass

    # ENVIO
    @st.cache_data
    def load_model_csv(_self) -> tuple[pd.DataFrame, str]:
        """
        Carrega um arquivo CSV e cria um dicionário de dados com tipos de colunas.
        
        Returns:
            tuple: Contém o dicionário de dados e o modelo em formato CSV.
        """
        file = pd.read_csv("files/modelo.csv", encoding="utf-8")  # Carrega o arquivo CSV
        data_dict = pd.DataFrame(file.dtypes).reset_index()  # Cria o dicionário com tipos de colunas
        data_dict.columns = ["Coluna", "Tipo"]  # Renomeia as colunas
        return data_dict, file.to_csv(index=False)  # Retorna o dicionário e o modelo como CSV

    @st.dialog("Dicionário de dados")
    def download_csv_file(_self) -> None:
        """
        Exibe o dicionário de dados e permite o download do modelo CSV.
        """
        dicionario_dados, modelo = _self.load_model_csv()    
        st.dataframe(dicionario_dados, use_container_width=True, hide_index=True)  # Exibe o dicionário de dados
        st.download_button(
            label="Baixar modelo em CSV",
            data=modelo,
            file_name="modelo.csv",
            mime="text/csv",
        )

    # CONSOLIDAÇÃO
    def make_dataframe(self, data: dict) -> pd.DataFrame:
        """
        Converte um dicionário de dados em um DataFrame.

        Args:
            data (dict): Dados a serem convertidos em DataFrame.

        Returns:
            pd.DataFrame: DataFrame com os dados normalizados.

        Raises:
            Exception: Caso os dados estejam vazios ou inválidos.
        """
        if not data:
            raise Exception("Collection data not found.")
        else:
            try:
                return pd.json_normalize(data)  # Normaliza os dados para um formato tabular
            except ValueError as e:
                raise Exception("Unable to load data from the collection: ", e)

    def make_result_dict(self, organization_cnes: int, year: int, month: int) -> dict:
        """
        Cria um dicionário de resultados combinando as métricas calculadas.
        
        Args:
            organization_cnes (int): Código da organização.
            year (int): Ano dos dados.
            month (int): Mês dos dados.

        Returns:
            dict: Dicionário contendo as informações e métricas calculadas.
        """
        result_dict = {
            "organization_cnes": organization_cnes,
            "year": year,
            "month": month,
            "data": {
                **self._1_proporcao_partos_vaginais,
                **self._2_proporcao_reinternacoes_30_dias,
                **self._3_taxa_pcr,
                **self._4_taxa_mortalidade,
                **self._5_tempo_medio_internacao,
                **self._6_tempo_medio_emergencia,
                **self._7_tempo_medio_espera_emergencia,
                **self._8_taxa_atb_profilatico,
                **self._9_taxa_infeccao_cirurgia_limpa,
                **self._10_incidencia_ipcs_cvc,
                **self._11_incidencia_itu_cvd,
                **self._12_taxa_profilaxia_tromboembolismo,
                **self._13_incidencia_queda,
                **self._14_evento_sentinela
            }
        }
        return result_dict

    def calculate(self, df: pd.DataFrame) -> dict:
        """
        Realiza os cálculos dos KPIs a partir de um DataFrame de entrada.

        Args:
            df (pd.DataFrame): DataFrame contendo os dados para os cálculos.

        Returns:
            dict: Dicionário com os resultados dos KPIs calculados.
        """
        self._1_proporcao_partos_vaginais = self.kpi.kpi1( total_partos_vaginais = df.at[0,'partos_vaginais'],
                                                           total_partos_cesareos = df.at[0,'partos_cesareos'] )
        self._2_proporcao_reinternacoes_30_dias = self.kpi.kpi2 ( cli_total_reinternacoes_30_dias = df.at[0,'reinternacoes_clinicas'],
                                                                  cli_total_saida_mes_anterior = df.at[0,'saidas_clinicas_anterior'],
                                                                  cir_total_reinternacoes_30_dias = df.at[0,'reinternacoes_cirurgicas'],
                                                                  cir_total_saida_mes_anterior = df.at[0,'saidas_cirurgicas_anterior'] )
        self._3_taxa_pcr = self.kpi.kpi3( total_pcr = df.at[0,'pcr_eventos'],
                                          total_pacientes_dia = df.at[0,'pacientes_dia'] )
        self._4_taxa_mortalidade = self.kpi.kpi4( cli_neo_precoce_total_obitos = df.at[0,'cli_neo_precoce_obitos'],
                                                  cli_neo_precoce_total_saidas = df.at[0,'cli_neo_precoce_saidas'],
                                                  cli_neo_tardio_total_obitos = df.at[0,'cli_neo_tardio_obitos'],
                                                  cli_neo_tardio_total_saidas = df.at[0,'cli_neo_tardio_saidas'],
                                                  cli_pedi_total_obitos = df.at[0,'cli_pedi_obitos'],
                                                  cli_pedi_total_saidas = df.at[0,'cli_pedi_saidas'],
                                                  cli_ad_total_obitos = df.at[0,'cli_ad_obitos'],
                                                  cli_ad_total_saidas = df.at[0,'cli_ad_saidas'],
                                                  cli_idoso_total_obitos = df.at[0,'cli_idoso_obitos'],
                                                  cli_idoso_total_saidas = df.at[0,'cli_idoso_saidas'],
                                                  cir_neo_precoce_total_obitos = df.at[0,'cir_neo_precoce_obitos'],
                                                  cir_neo_precoce_total_saidas = df.at[0,'cir_neo_precoce_saidas'],
                                                  cir_neo_tardio_total_obitos = df.at[0,'cir_neo_tardio_obitos'],
                                                  cir_neo_tardio_total_saidas = df.at[0,'cir_neo_tardio_saidas'],
                                                  cir_pedi_total_obitos = df.at[0,'cir_pedi_obitos'],
                                                  cir_pedi_total_saidas = df.at[0,'cir_pedi_saidas'],
                                                  cir_ad_total_obitos = df.at[0,'cir_ad_obitos'],
                                                  cir_ad_total_saidas = df.at[0,'cir_ad_saidas'],
                                                  cir_idoso_total_obitos = df.at[0,'cir_idoso_obitos'],
                                                  cir_idoso_total_saidas = df.at[0,'cir_idoso_saidas'] )
        self._5_tempo_medio_internacao = self.kpi.kpi5( cli_pedi_total_pacientes_dia = df.at[0,'cli_pedi_pacientes_dia'],
                                                        cli_pedi_total_saidas = df.at[0,'cli_pedi_saidas'],
                                                        cli_ad_total_pacientes_dia = df.at[0,'cli_ad_pacientes_dia'],
                                                        cli_ad_total_saidas = df.at[0,'cli_ad_saidas'],
                                                        cli_idoso_total_pacientes_dia = df.at[0,'cli_idoso_pacientes_dia'],
                                                        cli_idoso_total_saidas = df.at[0,'cli_idoso_saidas'],
                                                        cir_pedi_total_pacientes_dia = df.at[0,'cir_pedi_pacientes_dia'],
                                                        cir_pedi_total_saidas = df.at[0,'cir_pedi_saidas'],
                                                        cir_ad_total_pacientes_dia = df.at[0,'cir_ad_pacientes_dia'],
                                                        cir_ad_total_saidas = df.at[0,'cir_ad_saidas'],
                                                        cir_idoso_total_pacientes_dia = df.at[0,'cir_idoso_pacientes_dia'],
                                                        cir_idoso_total_saidas = df.at[0,'cir_idoso_saidas'] )
        self._6_tempo_medio_emergencia = self.kpi.kpi6( total_tempo_entrada_termino = df.at[0,'total_tempo_permanencia_emergencia_hr'],
                                                        total_pacientes_buscaram_atendimento = df.at[0,'total_pacientes_emergencia'] )
        self._7_tempo_medio_espera_emergencia = self.kpi.kpi7( nvl2_total_tempo_espera = df.at[0,'tempo_total_emergencia_nivel2_min'],
                                                               nvl2_total_pacientes_buscaram_atendimento = df.at[0,'pacientes_emergencia_nivel2'],
                                                               nvl3_total_tempo_espera = df.at[0,'tempo_total_emergencia_nivel3_min'],
                                                               nvl3_total_pacientes_buscaram_atendimento = df.at[0,'pacientes_emergencia_nivel3'] )
        self._8_taxa_atb_profilatico = self.kpi.kpi8( total_cirurgias_limpas_com_atb = df.at[0,'cirurgias_com_antibiotico'],
                                                      total_cirurgias_limpas = df.at[0,'total_cirurgias_limpas'] )
        self._9_taxa_infeccao_cirurgia_limpa = self.kpi.kpi9( total_isc_30_dias = df.at[0,'total_infeccoes'],
                                                              total_cirurgias_limpas_mes_anterior = df.at[0,'total_cirurgias_limpas_anterior'] )
        self._10_incidencia_ipcs_cvc = self.kpi.kpi10( ui_neo_total_ipcs = df.at[0,'ui_neo_infec'],
                                                       uti_neo_total_ipcs = df.at[0,'uti_neo_infec'],
                                                       ui_pedi_total_ipcs = df.at[0,'ui_pedi_infec'],
                                                       uti_pedi_total_ipcs = df.at[0,'uti_pedi_infec'],
                                                       ui_ad_total_ipcs = df.at[0,'ui_ad_infec'],
                                                       uti_ad_total_ipcs = df.at[0,'uti_ad_infec'],
                                                       ui_neo_total_cvc_dia = df.at[0,'ui_neo_cvc_dia'],
                                                       uti_neo_total_cvc_dia = df.at[0,'uti_neo_cvc_dia'],
                                                       ui_pedi_total_cvc_dia = df.at[0,'ui_pedi_cvc_dia'],
                                                       uti_pedi_total_cvc_dia = df.at[0,'uti_pedi_cvc_dia'],
                                                       ui_ad_total_cvc_dia = df.at[0,'ui_ad_cvc_dia'],
                                                       uti_ad_total_cvc_dia = df.at[0,'uti_ad_cvc_dia'] )
        self._11_incidencia_itu_cvd = self.kpi.kpi11( ui_neo_total_itu = df.at[0,'ui_neo_itu'],
                                                      uti_neo_total_itu = df.at[0,'uti_neo_itu'],
                                                      ui_pedi_total_itu = df.at[0,'ui_pedi_itu'],
                                                      uti_pedi_total_itu = df.at[0,'uti_pedi_itu'],
                                                      ui_ad_total_itu = df.at[0,'ui_ad_itu'],
                                                      uti_ad_total_itu = df.at[0,'uti_ad_itu'],
                                                      ui_neo_total_cvd_dia = df.at[0,'ui_neo_cvd_dia'],
                                                      uti_neo_total_cvd_dia = df.at[0,'uti_neo_cvd_dia'],
                                                      ui_pedi_total_cvd_dia = df.at[0,'ui_pedi_cvd_dia'],
                                                      uti_pedi_total_cvd_dia = df.at[0,'uti_pedi_cvd_dia'],
                                                      ui_ad_total_cvd_dia = df.at[0,'ui_ad_cvd_dia'],
                                                      uti_ad_total_cvd_dia = df.at[0,'uti_ad_cvd_dia'] )
        self._12_taxa_profilaxia_tromboembolismo = self.kpi.kpi12( cli_total_pacientes_risco_profilaxia_TEV = df.at[0,'cli_profilaxia'],
                                                                   cli_total_pacientes_risco = df.at[0,'cli_total_pacientes'],
                                                                   cir_orto_total_pacientes_risco_profilaxia_TEV = df.at[0,'cir_orto_profilaxia'],
                                                                   cir_orto_total_pacientes_risco = df.at[0,'cir_orto_total_pacientes'],
                                                                   cir_n_orto_total_pacientes_risco_profilaxia_TEV = df.at[0,'cir_nao_orto_profilaxia'],
                                                                   cir_n_orto_total_pacientes_risco = df.at[0,'cir_nao_orto_total_pacientes'] )
        self._13_incidencia_queda = self.kpi.kpi13( total_quedas_dano = df.at[0,'quedas_com_dano'],
                                                    total_pacientes_dia = df.at[0,'pacientes_dia'] )
        self._14_evento_sentinela = self.kpi.kpi14( total_eventos_sentinela = df.at[0,'eventos_sentinela'],
                                                    total_pacientes_dia = df.at[0,'pacientes_dia'] )
        result_dict = self.make_result_dict( organization_cnes = int(df.at[0,'organization_cnes']),
                                             year = int(df.at[0,'year']),
                                             month = int(df.at[0,'month']) )
        return result_dict

    def get_key_from_value(self, dict: dict, value):
        """
        Obtém a chave de um dicionário com base no valor correspondente.
        
        Args:
            dict (dict): Dicionário a ser pesquisado.
            value: Valor a ser encontrado.

        Returns:
            A chave correspondente ao valor encontrado ou None se não existir.
        """
        return next((k for k, v in dict.items() if v == value), None)

    # UPLOAD
    def valida_colunas(self, dataframe: pd.DataFrame, required_columns: list) -> list:
        """
        Valida se as colunas necessárias estão presentes no DataFrame.
        
        Args:
            dataframe (pd.DataFrame): DataFrame a ser validado.
            required_columns (list): Lista de colunas obrigatórias.

        Returns:
            list: Lista de colunas faltantes.
        """
        valida_coluna = []
        for col in required_columns:
            if col not in dataframe.columns:
                valida_coluna.append(col)
        return valida_coluna

    def valida_dados(self, dataframe: pd.DataFrame) -> list:
        """
        Valida se há dados nulos nas colunas do DataFrame.

        Args:
            dataframe (pd.DataFrame): DataFrame a ser validado.

        Returns:
            list: Lista de colunas com valores nulos.
        """
        valida_dado = []
        valida_dado = dataframe.columns[dataframe.isnull().any()].to_list()
        return valida_dado    

    def valida_registros(self, dataframe: pd.DataFrame) -> int:
        """
        Verifica se o DataFrame possui registros.

        Args:
            dataframe (pd.DataFrame): DataFrame a ser verificado.

        Returns:
            int: Retorna 1 se o DataFrame estiver vazio, caso contrário, retorna None.
        """
        if len(dataframe) == 0:
            return 1
        else:
            return None

    def verifica_competencias(self, dataframe: pd.DataFrame) -> int:
        """
        Verifica o número de registros no DataFrame.

        Args:
            dataframe (pd.DataFrame): DataFrame a ser verificado.

        Returns:
            int: Número de registros.
        """
        return len(dataframe)

    def valida_arquivo(self, arquivo):
        """
        Valida o arquivo CSV, verificando se contém as colunas e dados corretos.

        Args:
            arquivo: Arquivo CSV a ser validado.

        Returns:
            bool: Retorna True se o arquivo for válido, caso contrário, retorna False.
        """
        required_columns = [
            'organization_cnes', 'year', 'month', 'partos_vaginais',
            'partos_cesareos', 'saidas_clinicas_anterior',
            'saidas_cirurgicas_anterior', 'reinternacoes_clinicas',
            'reinternacoes_cirurgicas', 'pacientes_dia', 'pcr_eventos',
            'cli_neo_precoce_saidas', 'cli_neo_precoce_obitos',
            'cli_neo_precoce_pacientes_dia', 'cli_neo_tardio_saidas',
            'cli_neo_tardio_obitos', 'cli_neo_tardio_pacientes_dia',
            'cli_pedi_saidas', 'cli_pedi_obitos', 'cli_pedi_pacientes_dia',
            'cli_ad_saidas', 'cli_ad_obitos', 'cli_ad_pacientes_dia',
            'cli_idoso_saidas', 'cli_idoso_obitos', 'cli_idoso_pacientes_dia',
            'cir_neo_precoce_saidas', 'cir_neo_precoce_obitos',
            'cir_neo_precoce_pacientes_dia', 'cir_neo_tardio_saidas',
            'cir_neo_tardio_obitos', 'cir_neo_tardio_pacientes_dia',
            'cir_pedi_saidas', 'cir_pedi_obitos', 'cir_pedi_pacientes_dia',
            'cir_ad_saidas', 'cir_ad_obitos', 'cir_ad_pacientes_dia',
            'cir_idoso_saidas', 'cir_idoso_obitos', 'cir_idoso_pacientes_dia',
            'total_pacientes_emergencia', 'total_tempo_permanencia_emergencia_hr',
            'pacientes_emergencia_nivel2', 'pacientes_emergencia_nivel3',
            'tempo_total_emergencia_nivel2_min', 'tempo_total_emergencia_nivel3_min',
            'total_cirurgias_limpas', 'cirurgias_com_antibiotico',
            'total_cirurgias_limpas_anterior', 'total_infeccoes', 'ui_neo_cvc_dia',
            'ui_neo_infec', 'uti_neo_cvc_dia', 'uti_neo_infec', 'ui_pedi_cvc_dia',
            'ui_pedi_infec', 'uti_pedi_cvc_dia', 'uti_pedi_infec', 'ui_ad_cvc_dia',
            'ui_ad_infec', 'uti_ad_cvc_dia', 'uti_ad_infec', 'ui_neo_cvd_dia',
            'ui_neo_itu', 'uti_neo_cvd_dia', 'uti_neo_itu', 'ui_pedi_cvd_dia',
            'ui_pedi_itu', 'uti_pedi_cvd_dia', 'uti_pedi_itu', 'ui_ad_cvd_dia',
            'ui_ad_itu', 'uti_ad_cvd_dia', 'uti_ad_itu', 'cli_total_pacientes',
            'cli_profilaxia', 'cir_orto_total_pacientes', 'cir_orto_profilaxia',
            'cir_nao_orto_total_pacientes', 'cir_nao_orto_profilaxia',
            'quedas_com_dano', 'eventos_sentinela'
        ]
        invalid = None
        try:
            df = pd.read_csv(arquivo)
            colunas_validadas = self.valida_colunas(df, required_columns)
            if not colunas_validadas:
                registros_validados = self.valida_registros(df)
                if not registros_validados:
                    dados_validados = self.valida_dados(df)
        except ValueError as e:
            st.error(f"Erro ao ler arquivo. {e}")
            invalid = True
        
        if colunas_validadas:
            st.error(f"Uma ou mais colunas não encontradas. Esperado: {', '.join(colunas_validadas)}.", icon="🚨")
            return False
        elif registros_validados:
            st.error(f"O arquivo não possui registros", icon="🚨")
            return False
        elif dados_validados:
            st.error(f"Uma ou mais colunas estão com valor nulo: {', '.join(dados_validados)}.", icon="🚨")
            return False
        elif invalid:
            return False
        else:
            st.info(f"Arquivo validado. Empresa {df['organization_cnes'][0]}.", icon="✅")
            return True, df

    # HOME
    def valida_historico(self, raw_data: list) -> pd.DataFrame:
        """
        Valida e converte os dados de histórico para um DataFrame.
        
        Args:
            raw_data (list): Dados brutos a serem validados.

        Returns:
            pd.DataFrame: DataFrame com os dados de histórico.
        """
        if raw_data:
            dataframe = pd.DataFrame(raw_data).T.drop('year', axis=0)
            dataframe = pd.DataFrame(dataframe.apply(lambda x: not pd.isna(x.any()), axis=0)).T
        else:
            dataframe = pd.DataFrame()

        return dataframe

    def monta_historico(self, dados_metricas: pd.DataFrame, dados_resultados: pd.DataFrame) -> pd.DataFrame:
        """
        Concatena e organiza os dados históricos de métricas e resultados em um único DataFrame.

        Args:
            dados_metricas (pd.DataFrame): Dados das métricas.
            dados_resultados (pd.DataFrame): Dados dos resultados.

        Returns:
            pd.DataFrame: DataFrame contendo o histórico completo.
        """
        df_metricas = self.valida_historico(dados_metricas)
        df_resultados = self.valida_historico(dados_resultados)

        historico = pd.concat([df_metricas, df_resultados]).reset_index()
        historico['index'] = historico['index'].astype(str)
        historico.at[0, 'index'] = 'Enviado'
        historico.at[1, 'index'] = 'Consolidado'
        historico.columns = ["STATUS", "JAN", "FEV", "MAR", "ABR", "MAIO", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
        historico = historico.fillna(False)

        return historico
