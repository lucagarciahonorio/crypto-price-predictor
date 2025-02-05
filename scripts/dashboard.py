import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import time

# Conectar ao PostgreSQL
engine = create_engine("postgresql://admin:admin@localhost:5432/crypto_db")

# Funções para carregar os dados de cada criptomoeda
def load_bitcoin_data():
    query_real = "SELECT timestamp, price FROM bitcoin_prices ORDER BY timestamp"
    query_pred = "SELECT timestamp, predicted_price FROM bitcoin_predictions ORDER BY timestamp"
    data_real = pd.read_sql(query_real, engine)
    data_pred = pd.read_sql(query_pred, engine)
    # Converte timestamp para datetime
    data_real['timestamp'] = pd.to_datetime(data_real['timestamp'])
    data_pred['timestamp'] = pd.to_datetime(data_pred['timestamp'])
    return data_real, data_pred

def load_ethereum_data():
    query_real = "SELECT timestamp, price FROM ethereum_prices ORDER BY timestamp"
    query_pred = "SELECT timestamp, predicted_price FROM ethereum_predictions ORDER BY timestamp"
    data_real = pd.read_sql(query_real, engine)
    data_pred = pd.read_sql(query_pred, engine)
    # Converte timestamp para datetime
    data_real['timestamp'] = pd.to_datetime(data_real['timestamp'])
    data_pred['timestamp'] = pd.to_datetime(data_pred['timestamp'])
    return data_real, data_pred

# Configuração da página
st.title("📈 Criptomoedas: Preço Real vs Previsão")

# Cria um placeholder para atualizar os gráficos
placeholder = st.empty()

while True:
    # --- Dados e gráfico do Bitcoin ---
    btc_real, btc_pred = load_bitcoin_data()
    fig_btc = px.line(title="Bitcoin: Preço Real vs Previsão")
    fig_btc.add_scatter(x=btc_real['timestamp'], y=btc_real['price'],
                        mode='lines', name='Preço Real', line=dict(color='blue'))
    fig_btc.add_scatter(x=btc_pred['timestamp'], y=btc_pred['predicted_price'],
                        mode='lines', name='Previsão', line=dict(color='red', dash='dash'))
    
    # --- Dados e gráfico do Ethereum ---
    eth_real, eth_pred = load_ethereum_data()
    fig_eth = px.line(title="Ethereum: Preço Real vs Previsão")
    fig_eth.add_scatter(x=eth_real['timestamp'], y=eth_real['price'],
                        mode='lines', name='Preço Real', line=dict(color='green'))
    fig_eth.add_scatter(x=eth_pred['timestamp'], y=eth_pred['predicted_price'],
                        mode='lines', name='Previsão', line=dict(color='orange', dash='dash'))

    # Atualiza o placeholder com os dois gráficos
    with placeholder.container():
        st.subheader("Bitcoin")
        st.plotly_chart(fig_btc, use_container_width=True)
        st.subheader("Ethereum")
        st.plotly_chart(fig_eth, use_container_width=True)
    
    # Aguarda 60 segundos antes da próxima atualização
    time.sleep(60)
