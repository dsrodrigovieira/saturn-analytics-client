class KPI(object):

    def __init__ ( self ):
        self.rkpi2_clinico = None
        self.rkpi2_cirurgico = None
        self.rkpi2_geral = None
        self.rkpi4_cli_neo_precoce = None
        self.rkpi4_cli_neo_tardio = None
        self.rkpi4_cli_pedi = None
        self.rkpi4_cli_ad = None
        self.rkpi4_cli_idoso = None
        self.rkpi4_cir_neo_precoce = None
        self.rkpi4_cir_neo_tardio = None
        self.rkpi4_cir_pedi = None
        self.rkpi4_cir_ad = None
        self.rkpi4_cir_idoso = None
        self.rkpi4_clinico = None
        self.rkpi4_cirurgico = None
        self.rkpi4_neo_precoce = None
        self.rkpi4_neo_tardio = None
        self.rkpi4_pedi = None
        self.rkpi4_ad = None
        self.rkpi4_idoso = None
        self.rkpi4_geral = None
        self.rkpi5_cli_pedi = None
        self.rkpi5_cli_ad = None
        self.rkpi5_cli_idoso = None
        self.rkpi5_cir_pedi = None
        self.rkpi5_cir_ad = None
        self.rkpi5_cir_idoso = None
        self.rkpi5_clinico = None
        self.rkpi5_cirurgico = None
        self.rkpi5_pedi = None
        self.rkpi5_ad = None
        self.rkpi5_idoso = None
        self.rkpi5_geral = None
        self.rkpi7_nvl2 = None
        self.rkpi7_nvl3 = None
        self.rkpi7_geral = None
        self.rkpi10_ui_neo = None
        self.rkpi10_ui_pedi = None
        self.rkpi10_ui_ad = None
        self.rkpi10_uti_neo = None
        self.rkpi10_uti_pedi = None
        self.rkpi10_uti_ad = None
        self.rkpi10_neo = None
        self.rkpi10_pedi = None
        self.rkpi10_ad = None
        self.rkpi10_ui = None
        self.rkpi10_uti = None
        self.rkpi10_geral = None
        self.rkpi11_ui_neo = None
        self.rkpi11_ui_pedi = None
        self.rkpi11_ui_ad = None
        self.rkpi11_uti_neo = None
        self.rkpi11_uti_pedi = None
        self.rkpi11_uti_ad = None
        self.rkpi11_neo = None
        self.rkpi11_pedi = None
        self.rkpi11_ad = None
        self.rkpi11_ui = None
        self.rkpi11_uti = None
        self.rkpi11_geral = None
        self.rkpi12_cir_orto = None
        self.rkpi12_cir_n_orto = None
        self.rkpi12_cirurgico = None
        self.rkpi12_geral = None
        pass

    def validar_kwargs(self, kwargs, chaves_obrigatorias):
        # Validar se kwargs está vazio
        if not kwargs:
            raise ValueError("Os argumentos kwargs não podem estar vazios.")
        
        # Validar se todas as chaves obrigatórias estão presentes
        for chave in chaves_obrigatorias:
            if chave not in kwargs:
                raise KeyError(f"A chave obrigatória '{chave}' está ausente.")
        
        # Validar se os valores das chaves obrigatórias não são nulos
        for chave in chaves_obrigatorias:
            if kwargs[chave] is None:
                raise ValueError(f"O valor da chave '{chave}' não pode ser nulo.")
        
        # Retornar True se tudo estiver válido
        return True
    
    def cria_dict(self, mascara:str) -> dict:
        return {name: value for name, value in self.__dict__.items() if name.startswith(mascara)}
        
    def kpi_taxa(self, numerador:int,denominador:int) -> float:
        return (numerador/denominador) *100

    def kpi_tempo_medio(self, numerador:int,denominador:int) -> float:
        return (numerador/denominador)

    def kpi_densidade(self, numerador:int,denominador:int) -> float:
        return (numerador/denominador) *1000
    
    def kpi1(self, **kwargs) -> float:
        # 1. Proporção de partos vaginais 
        chaves_obrigatorias = ['total_partos_vaginais','total_partos_cesareos']
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            # Calcular o KPI
            total_partos = kwargs['total_partos_vaginais'] + kwargs['total_partos_cesareos']            
            return self.kpi_taxa( numerador = kwargs['total_partos_vaginais'],
                                  denominador = total_partos )
        else:
            return None
    
    def kpi2(self, **kwargs) -> dict:
        # 2. Proporção de reinternações em até 30 dias da saída hospitalar
        chaves_obrigatorias = [
            'cli_total_reinternacoes_30_dias','cli_total_saida_mes_anterior',
            'cir_total_reinternacoes_30_dias','cir_total_saida_mes_anterior'
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):                
            total_reinternacoes_ate_30_dias = kwargs['cli_total_reinternacoes_30_dias']+kwargs['cir_total_reinternacoes_30_dias']
            total_saidas_mes_anterior = kwargs['cli_total_saida_mes_anterior']+kwargs['cir_total_saida_mes_anterior']
            self.rkpi2_clinico = self.kpi_taxa( numerador = kwargs['cli_total_reinternacoes_30_dias'],
                                         denominador = kwargs['cli_total_saida_mes_anterior'])
            self.rkpi2_cirurgico = self.kpi_taxa( numerador = kwargs['cir_total_reinternacoes_30_dias'],
                                           denominador = kwargs['cir_total_saida_mes_anterior'])
            self.rkpi2_geral = self.kpi_taxa( numerador = total_reinternacoes_ate_30_dias,
                                       denominador = total_saidas_mes_anterior )            
            return self.cria_dict('rkpi2')
        else:
            return None
    
    def kpi3(self, **kwargs) -> float:
        # 3. Taxa de parada cardiorrespiratória em unidade de internação
        chaves_obrigatorias = ['total_pcr','total_pacientes_dia']
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):
            # Calcular o KPI        
            return self.kpi_densidade( numerador = kwargs['total_pcr'],
                                       denominador = kwargs['total_pacientes_dia'] )
        else:
            return None        

    def kpi4(self, **kwargs) -> dict:
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
            # Calcular o KPI        
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

            self.rkpi4_cli_neo_precoce = self.kpi_tempo_medio( numerador = kwargs['cli_neo_precoce_total_obitos'],
                                                          denominador = kwargs['cli_neo_precoce_total_saidas'])
            self.rkpi4_cli_neo_tardio = self.kpi_tempo_medio( numerador = kwargs['cli_neo_tardio_total_obitos'],
                                                         denominador = kwargs['cli_neo_tardio_total_saidas'])
            self.rkpi4_cli_pedi = self.kpi_tempo_medio( numerador = kwargs['cli_pedi_total_obitos'],
                                                   denominador = kwargs['cli_pedi_total_saidas'])
            self.rkpi4_cli_ad = self.kpi_tempo_medio( numerador = kwargs['cli_ad_total_obitos'],
                                                 denominador = kwargs['cli_ad_total_saidas'])
            self.rkpi4_cli_idoso = self.kpi_tempo_medio( numerador = kwargs['cli_idoso_total_obitos'],
                                                    denominador = kwargs['cli_idoso_total_saidas'])
            self.rkpi4_cir_neo_precoce = self.kpi_tempo_medio( numerador = kwargs['cir_neo_precoce_total_obitos'],
                                                          denominador = kwargs['cir_neo_precoce_total_saidas'])
            self.rkpi4_cir_neo_tardio = self.kpi_tempo_medio( numerador = kwargs['cir_neo_tardio_total_obitos'],
                                                         denominador = kwargs['cir_neo_tardio_total_saidas'])
            self.rkpi4_cir_pedi = self.kpi_tempo_medio( numerador = kwargs['cir_pedi_total_obitos'],
                                                   denominador = kwargs['cir_pedi_total_saidas'])
            self.rkpi4_cir_ad = self.kpi_tempo_medio( numerador = kwargs['cir_ad_total_obitos'],
                                                 denominador = kwargs['cir_ad_total_saidas'])
            self.rkpi4_cir_idoso = self.kpi_tempo_medio( numerador = kwargs['cir_idoso_total_obitos'],
                                                    denominador = kwargs['cir_idoso_total_saidas'])            
            self.rkpi4_clinico = self.kpi_tempo_medio( numerador = cli_total_obitos,
                                                  denominador = cli_total_saidas)
            self.rkpi4_cirurgico = self.kpi_tempo_medio( numerador = cir_total_obitos,
                                                    denominador = cir_total_saidas)
            self.rkpi4_neo_precoce = self.kpi_tempo_medio( numerador = neo_precoce_total_obitos,
                                                      denominador = neo_precoce_total_saidas)
            self.rkpi4_neo_tardio = self.kpi_tempo_medio( numerador = neo_tardio_total_obitos,
                                                     denominador = neo_tardio_total_saidas)
            self.rkpi4_pedi = self.kpi_tempo_medio( numerador = pedi_total_obitos,
                                               denominador = pedi_total_saidas)
            self.rkpi4_ad = self.kpi_tempo_medio( numerador = ad_total_obitos,
                                             denominador = ad_total_saidas)
            self.rkpi4_idoso = self.kpi_tempo_medio( numerador = idoso_total_obitos,
                                                denominador = idoso_total_saidas)
            self.rkpi4_geral = self.kpi_tempo_medio( numerador = total_obitos,
                                                denominador = total_saidas)            
            return self.cria_dict('rkpi4')
        else:
            return None

    def kpi5(self, **kwargs) -> dict:
        # 5. Tempo médio de internação
        chaves_obrigatorias = [
            'cli_pedi_total_pacientes_dia','cli_pedi_total_saidas',
            'cli_ad_total_pacientes_dia','cli_ad_total_saidas',
            'cli_idoso_total_pacientes_dia','cli_idoso_total_saidas',
            'cir_pedi_total_pacientes_dia','cir_pedi_total_saidas',
            'cir_ad_total_pacientes_dia','cir_ad_total_saidas',
            'cir_idoso_total_pacientes_dia','cir_idoso_total_saidas',
            ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):
            # Calcular o KPI        
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

            self.rkpi5_cli_pedi = self.kpi_tempo_medio( numerador = kwargs['cli_pedi_total_pacientes_dia'],
                                                   denominador = kwargs['cli_pedi_total_saidas'])
            self.rkpi5_cli_ad = self.kpi_tempo_medio( numerador = kwargs['cli_ad_total_pacientes_dia'],
                                                 denominador = kwargs['cli_ad_total_saidas'])
            self.rkpi5_cli_idoso = self.kpi_tempo_medio( numerador = kwargs['cli_idoso_total_pacientes_dia'],
                                                    denominador = kwargs['cli_idoso_total_saidas'])
            self.rkpi5_cir_pedi = self.kpi_tempo_medio( numerador = kwargs['cir_pedi_total_pacientes_dia'],
                                                   denominador = kwargs['cir_pedi_total_saidas'])
            self.rkpi5_cir_ad = self.kpi_tempo_medio( numerador = kwargs['cir_ad_total_pacientes_dia'],
                                                 denominador = kwargs['cir_ad_total_saidas'])
            self.rkpi5_cir_idoso = self.kpi_tempo_medio( numerador = kwargs['cir_idoso_total_pacientes_dia'],
                                                    denominador = kwargs['cir_idoso_total_saidas'])
            self.rkpi5_clinico = self.kpi_tempo_medio( numerador = cli_total_pacientes_dia,
                                                  denominador = cli_total_saidas)
            self.rkpi5_cirurgico = self.kpi_tempo_medio( numerador = cir_total_pacientes_dia,
                                                    denominador = cir_total_saidas)
            self.rkpi5_pedi = self.kpi_tempo_medio( numerador = pedi_total_pacientes_dia,
                                               denominador = pedi_total_saidas)
            self.rkpi5_ad = self.kpi_tempo_medio( numerador = ad_total_pacientes_dia,
                                             denominador = ad_total_saidas)
            self.rkpi5_idoso = self.kpi_tempo_medio( numerador = idoso_total_pacientes_dia,
                                                denominador = idoso_total_saidas)
            self.rkpi5_geral = self.kpi_tempo_medio( numerador = total_pacientes_dia,
                                                denominador = total_saidas)            
            return self.cria_dict('rkpi5')
        else:
            return None

    def kpi6(self, **kwargs) -> float:
        # 6. Tempo médio de permanência na emergência
        chaves_obrigatorias = [
            'total_tempo_entrada_termino',
            'total_pacientes_buscaram_atendimento'
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):
            # Calcular o KPI        
            return self.kpi_tempo_medio( numerador = kwargs['total_tempo_entrada_termino'],
                                         denominador = kwargs['total_pacientes_buscaram_atendimento'] )
        else:
            return None

    def kpi7(self, **kwargs) -> dict:
        # 7. Tempo médio de espera na emergência para primeiro atendimento
        chaves_obrigatorias = [
            'nvl2_total_tempo_espera',
            'nvl2_total_pacientes_buscaram_atendimento',
            'nvl3_total_tempo_espera',
            'nvl3_total_pacientes_buscaram_atendimento'
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):
            total_tempo_espera = kwargs['nvl2_total_tempo_espera']+kwargs['nvl3_total_tempo_espera']
            total_pacientes_buscaram_atendimento = kwargs['nvl2_total_pacientes_buscaram_atendimento']+kwargs['nvl3_total_pacientes_buscaram_atendimento']
            self.rkpi7_nvl2 = self.kpi_tempo_medio( numerador = kwargs['nvl2_total_tempo_espera'],
                                               denominador = kwargs['nvl2_total_pacientes_buscaram_atendimento'])
            self.rkpi7_nvl3 = self.kpi_tempo_medio( numerador = kwargs['nvl3_total_tempo_espera'],
                                               denominador = kwargs['nvl2_total_pacientes_buscaram_atendimento'])
            self.rkpi7_geral = self.kpi_tempo_medio( numerador = total_tempo_espera,
                                                denominador = total_pacientes_buscaram_atendimento )
            return self.cria_dict('rkpi7')
        else:
            return None

    def kpi8(self, **kwargs) -> float:
        # 8. Taxa de início de antibiótico intravenoso profilático
        chaves_obrigatorias = [
            'total_cirurgias_limpas_com_atb',
            'total_cirurgias_limpas'
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            # Calcular o KPI        
            return self.kpi_taxa( numerador = kwargs['total_cirurgias_limpas_com_atb'],
                                  denominador = kwargs['total_cirurgias_limpas'] )
        else:
            return None

    def kpi9(self, **kwargs) -> float:
        # 9. Taxa de infecção de sítio cirúrgico em cirurgia limpa
        chaves_obrigatorias = [
            'total_isc_30_dias',
            'total_cirurgias_limpas_mes_anterior'
        ]

        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            # Calcular o KPI        
            return self.kpi_taxa( numerador = kwargs['total_isc_30_dias'],
                                  denominador = kwargs['total_cirurgias_limpas_mes_anterior'] )      
        else:
            return None

    def kpi10(self, **kwargs) -> dict:
        # 10. Densidade de incidência de infecção primária de corrente sanguínea (IPCS)
        # em pacientes em uso de cateter venoso central (CVC)
        chaves_obrigatorias = [
            'ui_neo_total_ipcs', 'uti_neo_total_ipcs',
            'ui_pedi_total_ipcs', 'uti_pedi_total_ipcs',
            'ui_ad_total_ipcs', 'uti_ad_total_ipcs',
            'ui_neo_total_cvc_dia', 'uti_neo_total_cvc_dia',            
            'ui_pedi_total_cvc_dia', 'uti_pedi_total_cvc_dia',
            'ui_ad_total_cvc_dia', 'uti_ad_total_cvc_dia'            
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            # Calcular o KPI
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

            self.rkpi10_ui_neo = self.kpi_densidade( numerador = kwargs['ui_neo_total_ipcs'],
                                                denominador = kwargs['ui_neo_total_cvc_dia'] )  
            self.rkpi10_ui_pedi = self.kpi_densidade( numerador = kwargs['ui_pedi_total_ipcs'],
                                                 denominador = kwargs['ui_pedi_total_cvc_dia'] )  
            self.rkpi10_ui_ad = self.kpi_densidade( numerador = kwargs['ui_ad_total_ipcs'],
                                               denominador = kwargs['ui_ad_total_cvc_dia'] )  
            self.rkpi10_uti_neo = self.kpi_densidade( numerador = kwargs['uti_neo_total_ipcs'],
                                                 denominador = kwargs['uti_neo_total_cvc_dia'] )  
            self.rkpi10_uti_pedi = self.kpi_densidade( numerador = kwargs['uti_pedi_total_ipcs'],
                                                  denominador = kwargs['uti_pedi_total_cvc_dia'] )  
            self.rkpi10_uti_ad = self.kpi_densidade( numerador = kwargs['uti_ad_total_ipcs'],
                                                denominador = kwargs['uti_ad_total_cvc_dia'] )  
            self.rkpi10_neo = self.kpi_densidade( numerador = neo_total_ipcs,
                                             denominador = neo_total_cvc_dia )
            self.rkpi10_pedi = self.kpi_densidade( numerador = pedi_total_ipcs,
                                              denominador = pedi_total_cvc_dia )
            self.rkpi10_ad = self.kpi_densidade( numerador = ad_total_ipcs,
                                            denominador = ad_total_cvc_dia )
            self.rkpi10_ui = self.kpi_densidade( numerador = ui_total_ipcs,
                                            denominador = ui_total_cvc_dia )
            self.rkpi10_uti = self.kpi_densidade( numerador = uti_total_ipcs,
                                             denominador = uti_total_cvc_dia ) 
            self.rkpi10_geral = self.kpi_densidade( numerador = total_ipcs,
                                               denominador = total_cvc_dia )             
            return self.cria_dict('rkpi10')
        else:
            return None

    def kpi11(self, **kwargs) -> dict:
        # 11. Densidade de incidência de infecção do trato urinário (ITU) associada a um
        # cateter vesical de demora (CVD)
        chaves_obrigatorias = [
            'ui_neo_total_itu', 'uti_neo_total_itu',
            'ui_pedi_total_itu', 'uti_pedi_total_itu',
            'ui_ad_total_itu', 'uti_ad_total_itu',
            'ui_neo_total_cvd_dia', 'uti_neo_total_cvd_dia',            
            'ui_pedi_total_cvd_dia', 'uti_pedi_total_cvd_dia',
            'ui_ad_total_cvd_dia', 'uti_ad_total_cvd_dia'            
        ]
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            # Calcular o KPI
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

            self.rkpi11_ui_neo = self.kpi_densidade( numerador = kwargs['ui_neo_total_itu'],
                                                denominador = kwargs['ui_neo_total_cvd_dia'] )  
            self.rkpi11_ui_pedi = self.kpi_densidade( numerador = kwargs['ui_pedi_total_itu'],
                                                 denominador = kwargs['ui_pedi_total_cvd_dia'] )  
            self.rkpi11_ui_ad = self.kpi_densidade( numerador = kwargs['ui_ad_total_itu'],
                                               denominador = kwargs['ui_ad_total_cvd_dia'] )  
            self.rkpi11_uti_neo = self.kpi_densidade( numerador = kwargs['uti_neo_total_itu'],
                                                 denominador = kwargs['uti_neo_total_cvd_dia'] )  
            self.rkpi11_uti_pedi = self.kpi_densidade( numerador = kwargs['uti_pedi_total_itu'],
                                                  denominador = kwargs['uti_pedi_total_cvd_dia'] )  
            self.rkpi11_uti_ad = self.kpi_densidade( numerador = kwargs['uti_ad_total_itu'],
                                                denominador = kwargs['uti_ad_total_cvd_dia'] )  
            self.rkpi11_neo = self.kpi_densidade( numerador = neo_total_itu,
                                             denominador = neo_total_cvd_dia )
            self.rkpi11_pedi = self.kpi_densidade( numerador = pedi_total_itu,
                                              denominador = pedi_total_cvd_dia )
            self.rkpi11_ad = self.kpi_densidade( numerador = ad_total_itu,
                                            denominador = ad_total_cvd_dia )
            self.rkpi11_ui = self.kpi_densidade( numerador = ui_total_itu,
                                            denominador = ui_total_cvd_dia )
            self.rkpi11_uti = self.kpi_densidade( numerador = uti_total_itu,
                                             denominador = uti_total_cvd_dia ) 
            self.rkpi11_geral = self.kpi_densidade( numerador = total_itu,
                                               denominador = total_cvd_dia )            
            return self.cria_dict('rkpi11')
        else:
            return None

    def kpi12(self, **kwargs) -> dict:
        # 12. Taxa de profilaxia de tromboembolismo venoso
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
            self.rkpi12_cir_orto = self.kpi_taxa( numerador = kwargs['cir_orto_total_pacientes_risco_profilaxia_TEV'],
                                             denominador = kwargs['cir_orto_total_pacientes_risco'])
            self.rkpi12_cir_n_orto = self.kpi_taxa( numerador = kwargs['cir_n_orto_total_pacientes_risco_profilaxia_TEV'],
                                               denominador = kwargs['cir_n_orto_total_pacientes_risco'])
            self.rkpi12_cirurgico = self.kpi_taxa( numerador = cir_total_pacientes_risco_profilaxia_TEV,
                                              denominador = cir_total_pacientes_risco)
            self.rkpi12_geral = self.kpi_taxa( numerador = total_pacientes_risco_profilaxia_TEV,
                                          denominador = total_pacientes_risco )
            return self.cria_dict('rkpi12')
        else:
            return None
        
    def kpi13(self, **kwargs) -> float:
        # 13. Densidade de incidência de queda resultando em lesão em paciente
        chaves_obrigatorias = ['total_quedas_dano','total_pacientes_dia']
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            # Calcular o KPI        
            return self.kpi_densidade( numerador = kwargs['total_quedas_dano'],
                                       denominador = kwargs['total_pacientes_dia'] )  
        else:
            return None

    def kpi14(self, **kwargs) -> float:
        # 14. Evento sentinela
        chaves_obrigatorias = ['total_eventos_sentinela','total_pacientes_dia']
        if (self.validar_kwargs(kwargs,chaves_obrigatorias)):        
            # Calcular o KPI        
            return self.kpi_densidade( numerador = kwargs['total_eventos_sentinela'],
                                       denominador = kwargs['total_pacientes_dia'] )  
        else:
            return None     
