import time
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine, text

# Conectar ao PostgreSQL
engine = create_engine("postgresql://admin:admin@localhost:5432/crypto_db")

# Criar tabela para armazenar previsões do Bitcoin, se ainda não existir
create_table_query_bitcoin = """
CREATE TABLE IF NOT EXISTS bitcoin_predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    predicted_price NUMERIC NOT NULL
);
"""

# Criar tabela para armazenar previsões do Ethereum, se ainda não existir
create_table_query_ethereum = """
CREATE TABLE IF NOT EXISTS ethereum_predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    predicted_price NUMERIC NOT NULL
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_query_bitcoin))
    conn.execute(text(create_table_query_ethereum))
    conn.commit()

while True:
    try:
        print("\nAtualizando modelo e gerando previsão para Bitcoin e Ethereum...")

        # ------------------ Predição do Bitcoin ------------------
        # Lê os dados da tabela do Bitcoin
        query_bitcoin = "SELECT timestamp, price FROM bitcoin_prices ORDER BY timestamp"
        data_bitcoin = pd.read_sql(query_bitcoin, engine)

        # Converte o timestamp para número (segundos desde a Epoch)
        data_bitcoin['timestamp'] = pd.to_datetime(data_bitcoin['timestamp']).astype('int64') // 10**9

        # Prepara os dados para o modelo
        X_bitcoin = data_bitcoin['timestamp'].values.reshape(-1, 1)
        y_bitcoin = data_bitcoin['price'].values

        # Treina o modelo para o Bitcoin
        model_bitcoin = LinearRegression()
        model_bitcoin.fit(X_bitcoin, y_bitcoin)

        # Faz uma previsão para o próximo minuto
        next_timestamp_bitcoin = np.array([[data_bitcoin['timestamp'].max() + 60]])
        predicted_price_bitcoin = model_bitcoin.predict(next_timestamp_bitcoin)[0]
        predicted_price_bitcoin = float(predicted_price_bitcoin)

        print(f"Previsão para o Bitcoin no próximo minuto: ${predicted_price_bitcoin:.2f}")

        # Insere a previsão do Bitcoin no banco de dados
        insert_query_bitcoin = text("""
            INSERT INTO bitcoin_predictions (timestamp, predicted_price)
            VALUES (:timestamp, :predicted_price)
        """)
        with engine.connect() as conn:
            conn.execute(
                insert_query_bitcoin,
                {
                    "timestamp": pd.to_datetime(next_timestamp_bitcoin[0][0], unit='s'),
                    "predicted_price": predicted_price_bitcoin
                }
            )
            conn.commit()

        # ------------------ Predição do Ethereum ------------------
        # Lê os dados da tabela do Ethereum
        query_ethereum = "SELECT timestamp, price FROM ethereum_prices ORDER BY timestamp"
        data_ethereum = pd.read_sql(query_ethereum, engine)

        # Converte o timestamp para número (segundos desde a Epoch)
        data_ethereum['timestamp'] = pd.to_datetime(data_ethereum['timestamp']).astype('int64') // 10**9

        # Prepara os dados para o modelo
        X_ethereum = data_ethereum['timestamp'].values.reshape(-1, 1)
        y_ethereum = data_ethereum['price'].values

        # Treina o modelo para o Ethereum
        model_ethereum = LinearRegression()
        model_ethereum.fit(X_ethereum, y_ethereum)

        # Faz uma previsão para o próximo minuto
        next_timestamp_ethereum = np.array([[data_ethereum['timestamp'].max() + 60]])
        predicted_price_ethereum = model_ethereum.predict(next_timestamp_ethereum)[0]
        predicted_price_ethereum = float(predicted_price_ethereum)

        print(f"Previsão para o Ethereum no próximo minuto: ${predicted_price_ethereum:.2f}")

        # Insere a previsão do Ethereum no banco de dados
        insert_query_ethereum = text("""
            INSERT INTO ethereum_predictions (timestamp, predicted_price)
            VALUES (:timestamp, :predicted_price)
        """)
        with engine.connect() as conn:
            conn.execute(
                insert_query_ethereum,
                {
                    "timestamp": pd.to_datetime(next_timestamp_ethereum[0][0], unit='s'),
                    "predicted_price": predicted_price_ethereum
                }
            )
            conn.commit()

    except Exception as e:
        print(f"Erro ao processar modelo: {e}")

    # Aguarda 60 segundos antes da próxima previsão
    time.sleep(60)
