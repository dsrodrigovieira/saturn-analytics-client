# Saturn Analytics Client

[Saturn Analytics Client](https://saturn-analytics-client.streamlit.app) é uma aplicação desenvolvida em Python que permite o upload de dados para uma API, sendo parte de uma solução web de painel de indicadores assistenciais. Este projeto foi projetado para auxiliar na gestão da saúde hospitalar, oferecendo suporte na análise e visualização de métricas assistenciais.

## Recursos Principais

- Interface simples e intuitiva para upload de dados.
- Integração com uma API para processamento de dados.
- Utilização de **MongoDB Atlas** para o armazenamento e gerenciamento de dados.
- Desenvolvido com o framework **Streamlit** para uma interface web moderna e interativa.

## Objetivo

A aplicação tem como foco facilitar a coleta, o cálculo e o envio de dados para a API que apresenta indicadores em um painel de controle. Esses indicadores visam melhorar a tomada de decisão e a gestão hospitalar, promovendo eficiência e qualidade nos serviços de saúde.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Streamlit**: Framework utilizado para criar a interface web.
- **MongoDB Atlas**: Banco de dados utilizado para armazenar os dados enviados pela aplicação.
- **Git**: Para controle de versão e colaboração no desenvolvimento.

## Instalação e Uso

### Pré-requisitos

- Python v3.8 ou superior.
- pip v24 ou superior para gerenciamento de pacotes.
- Bibliotecas listadas no arquivo `requirements.txt`
- Conta no [MongoDB Atlas](https://www.mongodb.com/atlas/database) para configuração do banco de dados.

### Passos para Rodar o Projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/dsrodrigovieira/saturn-analytics-client.git
   ```

2. Acesse o diretório do projeto:
   ```bash
   cd saturn-analytics-client
   ```

3. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate # No Windows: venv\Scripts\activate
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure o arquivo `.toml` conforme o padrão do Streamlit [Saiba mais](https://docs.streamlit.io/develop/api-reference/connections/secrets.toml):
   ```toml
   [database]
   MONGO_URI = "mongodb+srv://[user]:[password]@[mongoCluster]"
   DATABASE = ""
   ```

6. Execute a aplicação:
   ```bash
    streamlit run __init__.py
   ```
  
### Contribuição
Contribuições são bem-vindas! Se você deseja melhorar o projeto ou reportar problemas, sinta-se à vontade para abrir uma issue ou enviar um pull request.

### Licença
Este projeto está licenciado sob a [MIT License](LICENSE).

### Contato
Para dúvidas ou sugestões, entre em contato com:
- **Rodrigo Vieira**
    - Email: dsrodrigovieira@gmail.com
    - LinkedIn: [dsrodrigovieira](https://linkedin.com/in/dsrodrigovieira)
