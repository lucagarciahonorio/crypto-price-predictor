# Projeto de Predição de Valor de Criptomoedas com Kafka e Machine Learning

Este projeto tem como objetivo prever o valor de criptomoedas em tempo real utilizando Apache Kafka, PostgreSQL e machine learning. Ele coleta dados de uma API pública, processa os dados com Kafka, armazena no PostgreSQL e faz previsões usando um modelo de regressão linear.

## Tecnologias Utilizadas

- **Apache Kafka**: Para processamento de dados em tempo real.
- **PostgreSQL**: Para armazenamento dos dados coletados.
- **Python**: Para scripts de coleta, processamento e modelagem.
- **Scikit-learn**: Para treinamento do modelo de machine learning.
- **Streamlit**: Para visualização dos dados em um dashboard (opcional).

## Pré-requisitos

- Docker e Docker Compose instalados.
- Python 3.8 ou superior.

## Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/projeto-kafka.git
   cd projeto-kafka