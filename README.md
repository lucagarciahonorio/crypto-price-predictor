# 📌 Projeto: Predição de Preços de Criptomoedas

## 📖 Descrição
Este projeto coleta dados de preço do Bitcoin e do Ethereum a cada minuto usando APIs de mercado. Os dados são processados pelo Apache Kafka, armazenados no PostgreSQL e utilizados por um modelo preditivo de regressão linear para gerar previsões. Por fim, os preços reais e preditivos são exibidos em um dashboard interativo com Streamlit.

---

## 🚀 Tecnologias Utilizadas
- **Linguagem:** Python  
- **Banco de Dados:** PostgreSQL  
- **Mensageria:** Apache Kafka  
- **Processamento de Dados:** Pandas, NumPy  
- **Machine Learning:** Scikit-Learn  
- **APIs de Dados:** CoinGecko  
- **Visualização:** Streamlit, Plotly  
- **Gerenciamento de Contêineres:** Docker, Docker Compose  

---

## 📂 Arquitetura

1️⃣ **APIs (CoinGecko, etc.)** → Coletam preços do Bitcoin e Ethereum.  
2️⃣ **Kafka** → Processa e distribui os dados coletados.  
3️⃣ **PostgreSQL** → Armazena dados históricos e previsões.  
4️⃣ **Modelo Preditivo** → Treina um modelo de regressão linear para prever preços futuros.  
5️⃣ **Dashboard (Streamlit)** → Exibe os preços reais e previstos.  

![Arquitetura](arquitetura.png)

---

## 🛠️ Requisitos
- Docker e Docker Compose instalados  
- Python 3.8+  
- Conta de acesso à API CoinGecko (caso necessário)  

---

## ⚙️ Configuração e Instalação

1️⃣ **Clone o repositório:**
```bash
 git clone https://github.com/lucagarciahonorio/crypto-price-predictor.git
```

2️⃣ **Configure o ambiente:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3️⃣ **Configure o PostgreSQL e Kafka via Docker:**
```bash
docker-compose up -d
```

4️⃣ **Execute o script de coleta e consumo de dados:**
```bash
python consumer.py
python producer.py
```

5️⃣ **Execute o modelo preditivo:**
```bash
python model.py
```

6️⃣ **Execute o dashboard:**
```bash
streamlit run dashboard.py
```

---

## 📊 Uso
Após iniciar todos os serviços, o dashboard apresentará dois gráficos:
- **Bitcoin**: Preço real vs. previsão  
- **Ethereum**: Preço real vs. previsão  

A atualização ocorre a cada minuto automaticamente.

---

## 🏗️ Estrutura do Projeto
```bash
📂 projeto-predicao-crypto
 ├── 📂 scripts
 │   ├── producer.py  # Obtém os dados da API
 │   ├── consumer.py  # conso os dados e armazena no PostgreSQL
 │   ├── model.py  # Treina e gera previsões
 │   ├── dashboard.py  # Interface gráfica com Streamlit
 │   ├── clean_database.py  # Limpa os bancos de dados 
 ├── 📂 configs
 │   ├── docker-compose.yml  # Configuração do PostgreSQL e Kafka
 ├── 📂 data
 │   ├── arquitetura.png  # Diagrama da arquitetura
 ├── README.md
 ├── requirements.txt  # Pacotes Python necessários
```

---

## 📜 Licença
Este projeto está licenciado sob a MIT License.

---

## 🤝 Contribuição
1️⃣ Faça um fork do projeto.  
2️⃣ Crie uma nova branch (`git checkout -b minha-feature`).  
3️⃣ Commit suas alterações (`git commit -m 'Minha nova feature'`).  
4️⃣ Faça um push para o repositório (`git push origin minha-feature`).  
5️⃣ Abra um Pull Request.  

---

## 📬 Contato
Se tiver dúvidas ou sugestões, entre em contato via [lucatestecod@gmail.com](mailto:seu-email@example.com).

