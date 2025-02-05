import json
import psycopg2
from confluent_kafka import Consumer

# Configuração do Kafka
KAFKA_BROKER = "localhost:9092"  # Atualize se necessário
KAFKA_TOPIC_BTC = "bitcoin_prices"
KAFKA_TOPIC_ETH = "ethereum_prices"

# Configuração do PostgreSQL (alterar se necessário)
DB_CONFIG = {
    "dbname": "crypto_db",
    "user": "admin",
    "password": "admin",
    "host": "localhost",
    "port": 5432
}

def create_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bitcoin_prices (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            price DECIMAL(10,2) NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ethereum_prices (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            price DECIMAL(10,2) NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

create_tables()  # Garante que as tabelas existam antes de consumir os dados
print("Tabelas verificadas!")

# Configuração do consumidor Kafka
consumer_conf = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "crypto_consumer_group",
    "auto.offset.reset": "earliest"
}
consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC_BTC, KAFKA_TOPIC_ETH])

def insert_into_postgres(topic, timestamp, price):
    """Insere os dados no PostgreSQL na tabela correspondente"""
    table_name = "bitcoin_prices" if topic == KAFKA_TOPIC_BTC else "ethereum_prices"
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {table_name} (timestamp, price) VALUES (TO_TIMESTAMP(%s), %s);",
            (timestamp, price)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Dados inseridos na {table_name}: timestamp={timestamp}, price={price}")
    except Exception as e:
        print(f"Erro ao inserir no PostgreSQL: {e}")

if __name__ == "__main__":
    print("Consumidor Kafka rodando...")
    while True:
        msg = consumer.poll(1.0)
        if msg is not None and msg.value():
            try:
                data = json.loads(msg.value().decode("utf-8"))
                insert_into_postgres(msg.topic(), data["timestamp"], data["price"])
            except Exception as e:
                print(f"Erro ao processar mensagem: {e}")
