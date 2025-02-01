import re
import pandas as pd

class KPI(object):
    """
    Classe para cálculo e manipulação de Indicadores de Desempenho (KPIs).
    """

    def __init__(self):
        """
        Inicializa os atributos necessários para armazenar o valor do KPI e dados relacionados.
        """
        self.rkpi_1 = None
        self.rkpi_2_clinico = None
        self.rkpi_2_cirurgico = None
        self.rkpi_2 = None
        self.rkpi_3 = None
        self.rkpi_4_cli_neo_precoce = None
        self.rkpi_4_cli_neo_tardio = None
        self.rkpi_4_cli_pedi = None
        self.rkpi_4_cli_ad = None
        self.rkpi_4_cli_idoso = None
        self.rkpi_4_cir_neo_precoce = None
        self.rkpi_4_cir_neo_tardio = None
        self.rkpi_4_cir_pedi = None
        self.rkpi_4_cir_ad = None
        self.rkpi_4_cir_idoso = None
        self.rkpi_4_clinico = None
        self.rkpi_4_cirurgico = None
        self.rkpi_4_neo_precoce = None
        self.rkpi_4_neo_tardio = None
        self.rkpi_4_pedi = None
        self.rkpi_4_ad = None
        self.rkpi_4_idoso = None
        self.rkpi_4 = None
        self.rkpi_5_cli_pedi = None
        self.rkpi_5_cli_ad = None
        self.rkpi_5_cli_idoso = None
        self.rkpi_5_cir_pedi = None
        self.rkpi_5_cir_ad = None
        self.rkpi_5_cir_idoso = None
        self.rkpi_5_clinico = None
        self.rkpi_5_cirurgico = None
        self.rkpi_5_pedi = None
        self.rkpi_5_ad = None
        self.rkpi_5_idoso = None
        self.rkpi_5 = None
        self.rkpi_6 = None
        self.rkpi_7_nvl2 = None
        self.rkpi_7_nvl3 = None
        self.rkpi_7 = None
        self.rkpi_8 = None
        self.rkpi_9 = None
        self.rkpi_10_ui_neo = None
        self.rkpi_10_ui_pedi = None
        self.rkpi_10_ui_ad = None
        self.rkpi_10_uti_neo = None
        self.rkpi_10_uti_pedi = None
        self.rkpi_10_uti_ad = None
        self.rkpi_10_neo = None
        self.rkpi_10_pedi = None
        self.rkpi_10_ad = None
        self.rkpi_10_ui = None
        self.rkpi_10_uti = None
        self.rkpi_10 = None
        self.rkpi_11_ui_neo = None
        self.rkpi_11_ui_pedi = None
        self.rkpi_11_ui_ad = None
        self.rkpi_11_uti_neo = None
        self.rkpi_11_uti_pedi = None
        self.rkpi_11_uti_ad = None
        self.rkpi_11_neo = None
        self.rkpi_11_pedi = None
        self.rkpi_11_ad = None
        self.rkpi_11_ui = None
        self.rkpi_11_uti = None
        self.rkpi_11 = None
        self.rkpi_12_cir_orto = None
        self.rkpi_12_cir_n_orto = None
        self.rkpi_12_cirurgico = None
        self.rkpi_12 = None
        self.rkpi_13 = None
        self.rkpi_14 = None
        self.dados_resultado_kpi = None
        pass

    def validar_kwargs(self, kwargs, chaves_obrigatorias):
        """
        Valida se as chaves obrigatórias estão presentes em kwargs e se seus valores não são nulos.
        
        Args:
            kwargs (dict): Dicionário de argumentos a ser validado.
            chaves_obrigatorias (list): Lista de chaves obrigatórias que devem existir em kwargs.

        Returns:
            bool: True se todas as validações forem bem-sucedidas.

        Raises:
            ValueError: Se kwargs estiver vazio ou se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente em kwargs.
        """
        if not kwargs:
            raise ValueError("Os argumentos kwargs não podem estar vazios.")
        
        for chave in chaves_obrigatorias:
            if chave not in kwargs:
                raise KeyError(f"A chave obrigatória '{chave}' está ausente.")
        
        for chave in chaves_obrigatorias:
            if kwargs[chave] is None:
                raise ValueError(f"O valor da chave '{chave}' não pode ser nulo.")
        
        return True
    
    def cria_variavel(self, mascara: str) -> dict:
        """
        Cria um dicionário com variáveis cujo nome começa com a máscara fornecida.
        
        Args:
            mascara (str): Máscara a ser usada para filtrar as variáveis da classe.
        
        Returns:
            dict: Dicionário com as variáveis filtradas.
        """        
        if mascara == 'rkpi_1':            
            return {name: value for name, value in self.__dict__.items() if name==(mascara)}
        else:            
            return {name: value for name, value in self.__dict__.items() if name.startswith(mascara)}

    def cria_estratificacao(self, mascara: str) -> dict:
        """
        Cria a estratificação com base nas variáveis filtradas pela máscara.

        Args:
            mascara (str): Máscara usada para filtrar as variáveis da classe.
        
        Returns:
            tuple: Contém o dicionário dados_resultado_kpi, o nome da variável principal e a estratificação.
        """
        dados_resultado_kpi = self.cria_variavel(mascara)        
        nome = re.match("^.+_\\d+", list(dados_resultado_kpi.keys())[0]).group(0)
        estratificacao = []

        if type(dados_resultado_kpi) in [float, int]:
            pass  # Caso os dados não sejam um dicionário, não há estratificação
        else:
            for key in dados_resultado_kpi.keys():                
                if key != nome:
                    estratificacao.append({ "tipo": key.replace(nome+'_', ''), "valor": dados_resultado_kpi[key] })                    
                else:
                    break
        return dados_resultado_kpi, nome, estratificacao
    
    def cria_objeto(self, mascara: str) -> dict:
        """
        Cria um objeto de KPI com base nas variáveis filtradas pela máscara.
        
        Args:
            mascara (str): Máscara a ser usada para filtrar as variáveis da classe.

        Returns:
            dict: Objeto do KPI com o valor e a estratificação.
        """
        dados_resultado_kpi, nome, estratificacao = self.cria_estratificacao(mascara)        
        return { nome: { "valor": dados_resultado_kpi[nome], "variacao": "", "estratificacao": estratificacao } }

    def calcula_variacao_mensal(self, dados_resultado: list) -> list:
        """
        Calcula o tipo de variação dos valores entre meses.
        
        Args:
            dados (list): Objetos mongoDB dos resultados dos meses encontrado.

        Returns:
            list: Lista com a variação de cada KPI.
        """
        if len(dados_resultado) < 2:
            return []
                
        df_resultado = pd.DataFrame()
        for resultado in dados_resultado:
            ultimo_mes = resultado['dados']
            df = pd.DataFrame(ultimo_mes).drop(['variacao','estratificacao'], axis=0).reset_index()
            df.at[0, 'index'] = f"{resultado['ano']}-{resultado['mes']}"
            df_resultado = pd.concat([df_resultado,df])
        df_resultado = df_resultado.reset_index(drop=True).sort_values(by='index').T[1:]
        df_resultado['variacao'] = df_resultado.apply(lambda x: 1 if x[1]>x[0] else 0, axis=1)

        return df_resultado.reset_index()[['index', 'variacao']].to_dict(orient='records')

    def kpi_taxa(self, numerador: int, denominador: int) -> float:
        """
        Calcula a taxa de um KPI, ou seja, a proporção entre o numerador e denominador multiplicada por 100.
        
        Args:
            numerador (int): Valor do numerador.
            denominador (int): Valor do denominador.

        Returns:
            float: Taxa calculada.
        """
        return (numerador / denominador) * 100

    def kpi_tempo_medio(self, numerador: int, denominador: int) -> float:
        """
        Calcula o tempo médio de um KPI.
        
        Args:
            numerador (int): Valor do numerador.
            denominador (int): Valor do denominador.

        Returns:
            float: Tempo médio calculado.
        """
        return (numerador / denominador)

    def kpi_densidade(self, numerador: int, denominador: int) -> float:
        """
        Calcula a densidade de um KPI, ou seja, a proporção entre o numerador e denominador multiplicada por 1000.
        
        Args:
            numerador (int): Valor do numerador.
            denominador (int): Valor do denominador.

        Returns:
            float: Densidade calculada.
        """
        return (numerador / denominador) * 1000

    def kpi1(self, **kwargs) -> dict:
        """
        Calcula a proporção de partos vaginais em relação ao total de partos.

        Args:
            kwargs (dict): Dicionário com o total de partos vaginais e cesáreos.

        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """
        chaves_obrigatorias = ['total_partos_vaginais', 'total_partos_cesareos']
        if self.validar_kwargs(kwargs, chaves_obrigatorias):        
            total_partos = kwargs['total_partos_vaginais'] + kwargs['total_partos_cesareos']            
            self.rkpi_1 = self.kpi_taxa(numerador=kwargs['total_partos_vaginais'],
                                         denominador=total_partos)
            return self.cria_objeto('rkpi_1')
        else:
            return None
    
    def kpi2(self, **kwargs) -> dict:
        """
        Calcula a proporção de reinternações em até 30 dias da saída hospitalar.
        Estratificações: clínico e cirúrgico.

        Args:
            kwargs (dict): Dicionário com o total de saídas no mês anterior e o total de reinternações em 30 dias
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """   
        chaves_obrigatorias = [
            'cli_total_reinternacoes_30_dias','cli_total_saida_mes_anterior',
            'cir_total_reinternacoes_30_dias','cir_total_saida_mes_anterior'
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):                
            total_reinternacoes_ate_30_dias = kwargs['cli_total_reinternacoes_30_dias']+kwargs['cir_total_reinternacoes_30_dias']
            total_saidas_mes_anterior = kwargs['cli_total_saida_mes_anterior']+kwargs['cir_total_saida_mes_anterior']
            self.rkpi_2_clinico = self.kpi_taxa( numerador = kwargs['cli_total_reinternacoes_30_dias'],
                                         denominador = kwargs['cli_total_saida_mes_anterior'])
            self.rkpi_2_cirurgico = self.kpi_taxa( numerador = kwargs['cir_total_reinternacoes_30_dias'],
                                           denominador = kwargs['cir_total_saida_mes_anterior'])
            self.rkpi_2 = self.kpi_taxa( numerador = total_reinternacoes_ate_30_dias,
                                       denominador = total_saidas_mes_anterior )            
            return self.cria_objeto('rkpi_2')
        else:
            return None
    
    def kpi3(self, **kwargs) -> dict:
        """
        Calcula a taxa de parada cardiorrespiratória em unidade de internação.
        
        Args:
            kwargs (dict): Dicionário com o total de pacientes-dia e o total de PCRs
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """
        chaves_obrigatorias = ['total_pcr','total_pacientes_dia']
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):
            self.rkpi_3 = self.kpi_densidade( numerador = kwargs['total_pcr'],
                                              denominador = kwargs['total_pacientes_dia'] )
            return self.cria_objeto('rkpi_3')
        else:
            return None        

    def kpi4(self, **kwargs) -> dict:
        """
        Calcula a taxa de mortalidade institucional.
        Estratificações: clínico, cirúrgico, neo precoce, neo tardio, pediátrico, adulto, idoso.

        Args:
            kwargs (dict): Dicionário com o total de saídas e o total de óbitos 
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """   
        # 4. Taxa de mortalidade institucional
        chaves_obrigatorias = [
            'cli_neo_precoce_total_obitos','cli_neo_precoce_total_saidas',
            'cli_neo_tardio_total_obitos','cli_neo_tardio_total_saidas',
            'cli_pedi_total_obitos','cli_pedi_total_saidas',
            'cli_ad_total_obitos','cli_ad_total_saidas',
            'cli_idoso_total_obitos','cli_idoso_total_saidas',
            'cir_neo_precoce_total_obitos','cir_neo_precoce_total_saidas',
            'cir_neo_tardio_total_obitos','cir_neo_tardio_total_saidas',
            'cir_pedi_total_obitos','cir_pedi_total_saidas',
            'cir_ad_total_obitos','cir_ad_total_saidas',
            'cir_idoso_total_obitos','cir_idoso_total_saidas'
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):
            cli_total_obitos = kwargs['cli_neo_precoce_total_obitos']+kwargs['cli_neo_tardio_total_obitos']+kwargs['cli_pedi_total_obitos']+kwargs['cli_ad_total_obitos']+kwargs['cli_idoso_total_obitos']
            cir_total_obitos = kwargs['cir_neo_precoce_total_obitos']+kwargs['cir_neo_tardio_total_obitos']+kwargs['cir_pedi_total_obitos']+kwargs['cir_ad_total_obitos']+kwargs['cir_idoso_total_obitos']
            cli_total_saidas = kwargs['cli_neo_precoce_total_saidas']+kwargs['cli_neo_tardio_total_saidas']+kwargs['cli_pedi_total_saidas']+kwargs['cli_ad_total_saidas']+kwargs['cli_idoso_total_saidas']
            cir_total_saidas = kwargs['cir_neo_precoce_total_saidas']+kwargs['cir_neo_tardio_total_saidas']+kwargs['cir_pedi_total_saidas']+kwargs['cir_ad_total_saidas']+kwargs['cir_idoso_total_saidas']
            neo_precoce_total_obitos = kwargs['cli_neo_precoce_total_obitos']+kwargs['cir_neo_precoce_total_obitos']
            neo_tardio_total_obitos = kwargs['cli_neo_tardio_total_obitos']+kwargs['cir_neo_tardio_total_obitos']
            pedi_total_obitos = kwargs['cli_pedi_total_obitos']+kwargs['cir_pedi_total_obitos']
            ad_total_obitos = kwargs['cli_ad_total_obitos']+kwargs['cir_ad_total_obitos']
            idoso_total_obitos = kwargs['cli_idoso_total_obitos']+kwargs['cir_idoso_total_obitos']
            neo_precoce_total_saidas = kwargs['cli_neo_precoce_total_saidas']+kwargs['cir_neo_precoce_total_saidas']
            neo_tardio_total_saidas = kwargs['cli_neo_tardio_total_saidas']+kwargs['cir_neo_tardio_total_saidas']
            pedi_total_saidas = kwargs['cli_pedi_total_saidas']+kwargs['cir_pedi_total_saidas']
            ad_total_saidas = kwargs['cli_ad_total_saidas']+kwargs['cir_ad_total_saidas']
            idoso_total_saidas = kwargs['cli_idoso_total_saidas']+kwargs['cir_idoso_total_saidas']
            total_obitos = cli_total_obitos + cir_total_obitos
            total_saidas = cli_total_saidas + cir_total_saidas

            self.rkpi_4_cli_neo_precoce = self.kpi_tempo_medio( numerador = kwargs['cli_neo_precoce_total_obitos'],
                                                          denominador = kwargs['cli_neo_precoce_total_saidas'])
            self.rkpi_4_cli_neo_tardio = self.kpi_tempo_medio( numerador = kwargs['cli_neo_tardio_total_obitos'],
                                                         denominador = kwargs['cli_neo_tardio_total_saidas'])
            self.rkpi_4_cli_pedi = self.kpi_tempo_medio( numerador = kwargs['cli_pedi_total_obitos'],
                                                   denominador = kwargs['cli_pedi_total_saidas'])
            self.rkpi_4_cli_ad = self.kpi_tempo_medio( numerador = kwargs['cli_ad_total_obitos'],
                                                 denominador = kwargs['cli_ad_total_saidas'])
            self.rkpi_4_cli_idoso = self.kpi_tempo_medio( numerador = kwargs['cli_idoso_total_obitos'],
                                                    denominador = kwargs['cli_idoso_total_saidas'])
            self.rkpi_4_cir_neo_precoce = self.kpi_tempo_medio( numerador = kwargs['cir_neo_precoce_total_obitos'],
                                                          denominador = kwargs['cir_neo_precoce_total_saidas'])
            self.rkpi_4_cir_neo_tardio = self.kpi_tempo_medio( numerador = kwargs['cir_neo_tardio_total_obitos'],
                                                         denominador = kwargs['cir_neo_tardio_total_saidas'])
            self.rkpi_4_cir_pedi = self.kpi_tempo_medio( numerador = kwargs['cir_pedi_total_obitos'],
                                                   denominador = kwargs['cir_pedi_total_saidas'])
            self.rkpi_4_cir_ad = self.kpi_tempo_medio( numerador = kwargs['cir_ad_total_obitos'],
                                                 denominador = kwargs['cir_ad_total_saidas'])
            self.rkpi_4_cir_idoso = self.kpi_tempo_medio( numerador = kwargs['cir_idoso_total_obitos'],
                                                    denominador = kwargs['cir_idoso_total_saidas'])            
            self.rkpi_4_clinico = self.kpi_tempo_medio( numerador = cli_total_obitos,
                                                  denominador = cli_total_saidas)
            self.rkpi_4_cirurgico = self.kpi_tempo_medio( numerador = cir_total_obitos,
                                                    denominador = cir_total_saidas)
            self.rkpi_4_neo_precoce = self.kpi_tempo_medio( numerador = neo_precoce_total_obitos,
                                                      denominador = neo_precoce_total_saidas)
            self.rkpi_4_neo_tardio = self.kpi_tempo_medio( numerador = neo_tardio_total_obitos,
                                                     denominador = neo_tardio_total_saidas)
            self.rkpi_4_pedi = self.kpi_tempo_medio( numerador = pedi_total_obitos,
                                               denominador = pedi_total_saidas)
            self.rkpi_4_ad = self.kpi_tempo_medio( numerador = ad_total_obitos,
                                             denominador = ad_total_saidas)
            self.rkpi_4_idoso = self.kpi_tempo_medio( numerador = idoso_total_obitos,
                                                denominador = idoso_total_saidas)
            self.rkpi_4 = self.kpi_tempo_medio( numerador = total_obitos,
                                                denominador = total_saidas)            
            return self.cria_objeto('rkpi_4')
        else:
            return None

    def kpi5(self, **kwargs) -> dict:
        """
        Calcula o tempo médio de internação.
        Estratificações: clínico, cirúrgico, pediátrico, adulto, idoso.

        Args:
            kwargs (dict): Dicionário com o total de saídas e o total de pacientes-dia 
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """        
        chaves_obrigatorias = [
            'cli_pedi_total_pacientes_dia','cli_pedi_total_saidas',
            'cli_ad_total_pacientes_dia','cli_ad_total_saidas',
            'cli_idoso_total_pacientes_dia','cli_idoso_total_saidas',
            'cir_pedi_total_pacientes_dia','cir_pedi_total_saidas',
            'cir_ad_total_pacientes_dia','cir_ad_total_saidas',
            'cir_idoso_total_pacientes_dia','cir_idoso_total_saidas',
            ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):
            cli_total_pacientes_dia = kwargs['cli_pedi_total_pacientes_dia']+kwargs['cli_ad_total_pacientes_dia']+kwargs['cli_idoso_total_pacientes_dia']
            cir_total_pacientes_dia = kwargs['cir_pedi_total_pacientes_dia']+kwargs['cir_ad_total_pacientes_dia']+kwargs['cir_idoso_total_pacientes_dia']
            pedi_total_pacientes_dia = kwargs['cir_pedi_total_pacientes_dia']+kwargs['cli_pedi_total_pacientes_dia']
            ad_total_pacientes_dia = kwargs['cir_ad_total_pacientes_dia']+kwargs['cli_ad_total_pacientes_dia']
            idoso_total_pacientes_dia = kwargs['cir_idoso_total_pacientes_dia']+kwargs['cli_idoso_total_pacientes_dia']
            cli_total_saidas = kwargs['cli_pedi_total_saidas']+kwargs['cli_ad_total_saidas']+kwargs['cli_idoso_total_saidas']
            cir_total_saidas = kwargs['cir_pedi_total_saidas']+kwargs['cir_ad_total_saidas']+kwargs['cir_idoso_total_saidas']
            pedi_total_saidas = kwargs['cir_pedi_total_saidas']+kwargs['cli_pedi_total_saidas']
            ad_total_saidas = kwargs['cir_ad_total_saidas']+kwargs['cli_ad_total_saidas']
            idoso_total_saidas = kwargs['cir_idoso_total_saidas']+kwargs['cli_idoso_total_saidas']
            total_pacientes_dia = cli_total_pacientes_dia + cir_total_pacientes_dia
            total_saidas = cli_total_saidas + cir_total_saidas

            self.rkpi_5_cli_pedi = self.kpi_tempo_medio( numerador = kwargs['cli_pedi_total_pacientes_dia'],
                                                   denominador = kwargs['cli_pedi_total_saidas'])
            self.rkpi_5_cli_ad = self.kpi_tempo_medio( numerador = kwargs['cli_ad_total_pacientes_dia'],
                                                 denominador = kwargs['cli_ad_total_saidas'])
            self.rkpi_5_cli_idoso = self.kpi_tempo_medio( numerador = kwargs['cli_idoso_total_pacientes_dia'],
                                                    denominador = kwargs['cli_idoso_total_saidas'])
            self.rkpi_5_cir_pedi = self.kpi_tempo_medio( numerador = kwargs['cir_pedi_total_pacientes_dia'],
                                                   denominador = kwargs['cir_pedi_total_saidas'])
            self.rkpi_5_cir_ad = self.kpi_tempo_medio( numerador = kwargs['cir_ad_total_pacientes_dia'],
                                                 denominador = kwargs['cir_ad_total_saidas'])
            self.rkpi_5_cir_idoso = self.kpi_tempo_medio( numerador = kwargs['cir_idoso_total_pacientes_dia'],
                                                    denominador = kwargs['cir_idoso_total_saidas'])
            self.rkpi_5_clinico = self.kpi_tempo_medio( numerador = cli_total_pacientes_dia,
                                                  denominador = cli_total_saidas)
            self.rkpi_5_cirurgico = self.kpi_tempo_medio( numerador = cir_total_pacientes_dia,
                                                    denominador = cir_total_saidas)
            self.rkpi_5_pedi = self.kpi_tempo_medio( numerador = pedi_total_pacientes_dia,
                                               denominador = pedi_total_saidas)
            self.rkpi_5_ad = self.kpi_tempo_medio( numerador = ad_total_pacientes_dia,
                                             denominador = ad_total_saidas)
            self.rkpi_5_idoso = self.kpi_tempo_medio( numerador = idoso_total_pacientes_dia,
                                                denominador = idoso_total_saidas)
            self.rkpi_5 = self.kpi_tempo_medio( numerador = total_pacientes_dia,
                                                denominador = total_saidas)            
            return self.cria_objeto('rkpi_5')
        else:
            return None

    def kpi6(self, **kwargs) -> dict:
        """
        Calcula o tempo médio de permanência na emergência.
        
        Args:
            kwargs (dict): Dicionário com o total de pacientes que buscaram atendimento e o total de tempo entre a chegada e o término do atendimento.
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """          
        chaves_obrigatorias = [ 'total_tempo_entrada_termino', 'total_pacientes_buscaram_atendimento' ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):
            self.rkpi_6 = self.kpi_tempo_medio( numerador = kwargs['total_tempo_entrada_termino'],
                                                denominador = kwargs['total_pacientes_buscaram_atendimento'] )
            return self.cria_objeto('rkpi_6')
        else:
            return None

    def kpi7(self, **kwargs) -> dict:
        """
        Calcula o tempo médio de espera na emergência para primeiro atendimento.
        Estratificações: nível 2 (Laranja, Muito Urgente), nível 3 (Amarelo, Urgente)

        Args:
            kwargs (dict): Dicionário com o total de pacientes que buscaram atendimento e o total de tempo entre a triagem e o início do atendimento médico.
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """          
        chaves_obrigatorias = [ 'nvl2_total_tempo_espera', 'nvl2_total_pacientes_buscaram_atendimento',
                                'nvl3_total_tempo_espera', 'nvl3_total_pacientes_buscaram_atendimento' ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):
            total_tempo_espera = kwargs['nvl2_total_tempo_espera']+kwargs['nvl3_total_tempo_espera']
            total_pacientes_buscaram_atendimento = kwargs['nvl2_total_pacientes_buscaram_atendimento']+kwargs['nvl3_total_pacientes_buscaram_atendimento']
            self.rkpi_7_nvl2 = self.kpi_tempo_medio( numerador = kwargs['nvl2_total_tempo_espera'],
                                               denominador = kwargs['nvl2_total_pacientes_buscaram_atendimento'])
            self.rkpi_7_nvl3 = self.kpi_tempo_medio( numerador = kwargs['nvl3_total_tempo_espera'],
                                               denominador = kwargs['nvl2_total_pacientes_buscaram_atendimento'])
            self.rkpi_7 = self.kpi_tempo_medio( numerador = total_tempo_espera,
                                                denominador = total_pacientes_buscaram_atendimento )
            return self.cria_objeto('rkpi_7')
        else:
            return None

    def kpi8(self, **kwargs) -> dict:
        """
        Calcula a taxa de início de antibiótico intravenoso profilático.
        
        Args:
            kwargs (dict): Dicionário com o total cirurgias limpas e o total de cirurgias limpas com ATB.
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """
        chaves_obrigatorias = [ 'total_cirurgias_limpas_com_atb', 'total_cirurgias_limpas' ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            self.rkpi_8 = self.kpi_taxa( numerador = kwargs['total_cirurgias_limpas_com_atb'],
                                         denominador = kwargs['total_cirurgias_limpas'] )
            return self.cria_objeto('rkpi_8')
        else:
            return None

    def kpi9(self, **kwargs) -> dict:
        """
        Calcula a taxa de infecção de sítio cirúrgico em cirurgia limpa.
        
        Args:
            kwargs (dict): Dicionário com o total cirurgias limpas no mês anterior e o total de infecções de sítio cirúrgico em até 30 dias.
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """
        chaves_obrigatorias = [ 'total_isc_30_dias', 'total_cirurgias_limpas_mes_anterior' ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            self.rkpi_9 = self.kpi_taxa( numerador = kwargs['total_isc_30_dias'],
                                         denominador = kwargs['total_cirurgias_limpas_mes_anterior'] )    
            return self.cria_objeto('rkpi_9')  
        else:
            return None

    def kpi10(self, **kwargs) -> dict:
        """
        Calcula a densidade de incidência de infecção primária de corrente sanguínea (IPCS) em pacientes em uso de cateter venoso central (CVC).
        Estratificações: uti, unidade de internação, neonatal, pediátrico, adulto.
        
        Args:
            kwargs (dict): Dicionário com o total cateter-dia e o total de infecções de corrente sanguínea.
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """        
        chaves_obrigatorias = [
            'ui_neo_total_ipcs', 'uti_neo_total_ipcs',
            'ui_pedi_total_ipcs', 'uti_pedi_total_ipcs',
            'ui_ad_total_ipcs', 'uti_ad_total_ipcs',
            'ui_neo_total_cvc_dia', 'uti_neo_total_cvc_dia',            
            'ui_pedi_total_cvc_dia', 'uti_pedi_total_cvc_dia',
            'ui_ad_total_cvc_dia', 'uti_ad_total_cvc_dia'            
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            ui_total_ipcs = kwargs['ui_neo_total_ipcs']+kwargs['ui_pedi_total_ipcs']+kwargs['ui_ad_total_ipcs']
            uti_total_ipcs = kwargs['uti_neo_total_ipcs']+kwargs['uti_pedi_total_ipcs']+kwargs['uti_ad_total_ipcs']
            ui_total_cvc_dia = kwargs['ui_neo_total_cvc_dia']+kwargs['ui_pedi_total_cvc_dia']+kwargs['ui_ad_total_cvc_dia']
            uti_total_cvc_dia = kwargs['uti_neo_total_cvc_dia']+kwargs['uti_pedi_total_cvc_dia']+kwargs['uti_ad_total_cvc_dia']
            neo_total_ipcs = kwargs['ui_neo_total_ipcs']+kwargs['uti_neo_total_ipcs']
            pedi_total_ipcs = kwargs['ui_pedi_total_ipcs']+kwargs['uti_pedi_total_ipcs']
            ad_total_ipcs = kwargs['ui_ad_total_ipcs']+kwargs['uti_ad_total_ipcs']
            neo_total_cvc_dia = kwargs['ui_neo_total_cvc_dia']+kwargs['uti_neo_total_cvc_dia']
            pedi_total_cvc_dia = kwargs['ui_pedi_total_cvc_dia']+kwargs['uti_pedi_total_cvc_dia']
            ad_total_cvc_dia = kwargs['ui_ad_total_cvc_dia']+kwargs['uti_ad_total_cvc_dia']  
            total_ipcs = ui_total_ipcs + uti_total_ipcs
            total_cvc_dia = ui_total_cvc_dia + uti_total_cvc_dia            

            self.rkpi_10_ui_neo = self.kpi_densidade( numerador = kwargs['ui_neo_total_ipcs'],
                                                denominador = kwargs['ui_neo_total_cvc_dia'] )  
            self.rkpi_10_ui_pedi = self.kpi_densidade( numerador = kwargs['ui_pedi_total_ipcs'],
                                                 denominador = kwargs['ui_pedi_total_cvc_dia'] )  
            self.rkpi_10_ui_ad = self.kpi_densidade( numerador = kwargs['ui_ad_total_ipcs'],
                                               denominador = kwargs['ui_ad_total_cvc_dia'] )  
            self.rkpi_10_uti_neo = self.kpi_densidade( numerador = kwargs['uti_neo_total_ipcs'],
                                                 denominador = kwargs['uti_neo_total_cvc_dia'] )  
            self.rkpi_10_uti_pedi = self.kpi_densidade( numerador = kwargs['uti_pedi_total_ipcs'],
                                                  denominador = kwargs['uti_pedi_total_cvc_dia'] )  
            self.rkpi_10_uti_ad = self.kpi_densidade( numerador = kwargs['uti_ad_total_ipcs'],
                                                denominador = kwargs['uti_ad_total_cvc_dia'] )  
            self.rkpi_10_neo = self.kpi_densidade( numerador = neo_total_ipcs,
                                             denominador = neo_total_cvc_dia )
            self.rkpi_10_pedi = self.kpi_densidade( numerador = pedi_total_ipcs,
                                              denominador = pedi_total_cvc_dia )
            self.rkpi_10_ad = self.kpi_densidade( numerador = ad_total_ipcs,
                                            denominador = ad_total_cvc_dia )
            self.rkpi_10_ui = self.kpi_densidade( numerador = ui_total_ipcs,
                                            denominador = ui_total_cvc_dia )
            self.rkpi_10_uti = self.kpi_densidade( numerador = uti_total_ipcs,
                                             denominador = uti_total_cvc_dia ) 
            self.rkpi_10 = self.kpi_densidade( numerador = total_ipcs,
                                               denominador = total_cvc_dia )             
            return self.cria_objeto('rkpi_10')
        else:
            return None

    def kpi11(self, **kwargs) -> dict:
        """
        Calcula a densidade de incidência de infecção do trato urinário (ITU) associada a um cateter vesical de demora (CVD).
        Estratificações: uti, unidade de internação, neonatal, pediátrico, adulto.
        
        Args:
            kwargs (dict): Dicionário com o total cateter-dia e o total de infecções do trato urinário.
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """        
        chaves_obrigatorias = [
            'ui_neo_total_itu', 'uti_neo_total_itu',
            'ui_pedi_total_itu', 'uti_pedi_total_itu',
            'ui_ad_total_itu', 'uti_ad_total_itu',
            'ui_neo_total_cvd_dia', 'uti_neo_total_cvd_dia',            
            'ui_pedi_total_cvd_dia', 'uti_pedi_total_cvd_dia',
            'ui_ad_total_cvd_dia', 'uti_ad_total_cvd_dia'            
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            ui_total_itu = kwargs['ui_neo_total_itu']+kwargs['ui_pedi_total_itu']+kwargs['ui_ad_total_itu']
            uti_total_itu = kwargs['uti_neo_total_itu']+kwargs['uti_pedi_total_itu']+kwargs['uti_ad_total_itu']
            ui_total_cvd_dia = kwargs['ui_neo_total_cvd_dia']+kwargs['ui_pedi_total_cvd_dia']+kwargs['ui_ad_total_cvd_dia']
            uti_total_cvd_dia = kwargs['uti_neo_total_cvd_dia']+kwargs['uti_pedi_total_cvd_dia']+kwargs['uti_ad_total_cvd_dia']
            neo_total_itu = kwargs['ui_neo_total_itu']+kwargs['uti_neo_total_itu']
            pedi_total_itu = kwargs['ui_pedi_total_itu']+kwargs['uti_pedi_total_itu']
            ad_total_itu = kwargs['ui_ad_total_itu']+kwargs['uti_ad_total_itu']
            neo_total_cvd_dia = kwargs['ui_neo_total_cvd_dia']+kwargs['uti_neo_total_cvd_dia']
            pedi_total_cvd_dia = kwargs['ui_pedi_total_cvd_dia']+kwargs['uti_pedi_total_cvd_dia']
            ad_total_cvd_dia = kwargs['ui_ad_total_cvd_dia']+kwargs['uti_ad_total_cvd_dia']  
            total_itu = ui_total_itu + uti_total_itu
            total_cvd_dia = ui_total_cvd_dia + uti_total_cvd_dia            

            self.rkpi_11_ui_neo = self.kpi_densidade( numerador = kwargs['ui_neo_total_itu'],
                                                denominador = kwargs['ui_neo_total_cvd_dia'] )  
            self.rkpi_11_ui_pedi = self.kpi_densidade( numerador = kwargs['ui_pedi_total_itu'],
                                                 denominador = kwargs['ui_pedi_total_cvd_dia'] )  
            self.rkpi_11_ui_ad = self.kpi_densidade( numerador = kwargs['ui_ad_total_itu'],
                                               denominador = kwargs['ui_ad_total_cvd_dia'] )  
            self.rkpi_11_uti_neo = self.kpi_densidade( numerador = kwargs['uti_neo_total_itu'],
                                                 denominador = kwargs['uti_neo_total_cvd_dia'] )  
            self.rkpi_11_uti_pedi = self.kpi_densidade( numerador = kwargs['uti_pedi_total_itu'],
                                                  denominador = kwargs['uti_pedi_total_cvd_dia'] )  
            self.rkpi_11_uti_ad = self.kpi_densidade( numerador = kwargs['uti_ad_total_itu'],
                                                denominador = kwargs['uti_ad_total_cvd_dia'] )  
            self.rkpi_11_neo = self.kpi_densidade( numerador = neo_total_itu,
                                             denominador = neo_total_cvd_dia )
            self.rkpi_11_pedi = self.kpi_densidade( numerador = pedi_total_itu,
                                              denominador = pedi_total_cvd_dia )
            self.rkpi_11_ad = self.kpi_densidade( numerador = ad_total_itu,
                                            denominador = ad_total_cvd_dia )
            self.rkpi_11_ui = self.kpi_densidade( numerador = ui_total_itu,
                                            denominador = ui_total_cvd_dia )
            self.rkpi_11_uti = self.kpi_densidade( numerador = uti_total_itu,
                                             denominador = uti_total_cvd_dia ) 
            self.rkpi_11 = self.kpi_densidade( numerador = total_itu,
                                               denominador = total_cvd_dia )            
            return self.cria_objeto('rkpi_11')
        else:
            return None

    def kpi12(self, **kwargs) -> dict:
        """
        Calcula a taxa de profilaxia de tromboembolismo venoso.
        Estratificações: clínico, cirúrgico ortopédico, cirúrgico não ortopédico.
        
        Args:
            kwargs (dict): Dicionário com o total de pacientes em risco trombótico não baixo e o total de pacientes com risco que receberam profilaxia.
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """           
        chaves_obrigatorias = [
            'cli_total_pacientes_risco_profilaxia_TEV','cli_total_pacientes_risco',
            'cir_orto_total_pacientes_risco_profilaxia_TEV','cir_orto_total_pacientes_risco',
            'cir_n_orto_total_pacientes_risco_profilaxia_TEV','cir_n_orto_total_pacientes_risco'
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            cir_total_pacientes_risco_profilaxia_TEV = kwargs['cir_orto_total_pacientes_risco_profilaxia_TEV']+kwargs['cir_n_orto_total_pacientes_risco_profilaxia_TEV']
            total_pacientes_risco_profilaxia_TEV = cir_total_pacientes_risco_profilaxia_TEV+kwargs['cli_total_pacientes_risco_profilaxia_TEV']
            cir_total_pacientes_risco = kwargs['cir_orto_total_pacientes_risco']+kwargs['cir_n_orto_total_pacientes_risco']
            total_pacientes_risco = cir_total_pacientes_risco+kwargs['cli_total_pacientes_risco']
            self.rkpi_12_cir_orto = self.kpi_taxa( numerador = kwargs['cir_orto_total_pacientes_risco_profilaxia_TEV'],
                                             denominador = kwargs['cir_orto_total_pacientes_risco'])
            self.rkpi_12_cir_n_orto = self.kpi_taxa( numerador = kwargs['cir_n_orto_total_pacientes_risco_profilaxia_TEV'],
                                               denominador = kwargs['cir_n_orto_total_pacientes_risco'])
            self.rkpi_12_cirurgico = self.kpi_taxa( numerador = cir_total_pacientes_risco_profilaxia_TEV,
                                              denominador = cir_total_pacientes_risco)
            self.rkpi_12 = self.kpi_taxa( numerador = total_pacientes_risco_profilaxia_TEV,
                                          denominador = total_pacientes_risco )
            return self.cria_objeto('rkpi_12')
        else:
            return None
        
    def kpi13(self, **kwargs) -> dict:
        """
        Calcula a densidade de incidência de queda resultando em lesão em paciente.
                
        Args:
            kwargs (dict): Dicionário com o total de pacientes-dia e o total de quedas com dano.
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """
        chaves_obrigatorias = [ 'total_quedas_dano', 'total_pacientes_dia' ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            self.rkpi_13 = self.kpi_densidade( numerador = kwargs['total_quedas_dano'],
                                               denominador = kwargs['total_pacientes_dia'] )  
            return self.cria_objeto('rkpi_13')
        else:
            return None

    def kpi14(self, **kwargs) -> dict:
        """
        Calcula a densidade de eventos sentinela.
                
        Args:
            kwargs (dict): Dicionário com o total de pacientes-dia e o total de eventos sentinela.
            
        Returns:
            dict: Objeto com o valor do KPI calculado e a estratificação.

        Raises:
            ValueError: Se algum valor de chave obrigatória for nulo.
            KeyError: Se alguma chave obrigatória estiver ausente.
        """
        chaves_obrigatorias = [ 'total_eventos_sentinela', 'total_pacientes_dia' ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            self.rkpi_14 = self.kpi_densidade( numerador = kwargs['total_eventos_sentinela'],
                                               denominador = kwargs['total_pacientes_dia'] )  
            return self.cria_objeto('rkpi_14')
        else:
            return None     
