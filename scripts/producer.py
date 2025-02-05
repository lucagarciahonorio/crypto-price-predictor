import json
import time
import requests
import pytz
from confluent_kafka import Producer
from datetime import datetime, timezone

# Configuração do Kafka
KAFKA_BROKER = "localhost:9092"  # Atualize se necessário
KAFKA_TOPIC_BTC = "bitcoin_prices"
KAFKA_TOPIC_ETH = "ethereum_prices"

# Configuração do produtor Kafka
producer_conf = {
    "bootstrap.servers": KAFKA_BROKER
}
producer = Producer(producer_conf)

def get_crypto_price(crypto_id):
    """Consulta o preço de uma criptomoeda na API CoinGecko"""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data.get(crypto_id, {}).get("usd")
    except Exception as e:
        print(f"Erro ao buscar preço do {crypto_id}: {e}")
        return None

def send_to_kafka(topic, crypto_id, price):
    """Envia os dados para o tópico Kafka"""
    if price is not None:
        #utc_now = datetime.utcnow()
        utc_now = datetime.now(timezone.utc)
        brasilia_tz = pytz.timezone("America/Sao_Paulo")
        brasilia_time = utc_now.replace(tzinfo=pytz.utc).astimezone(brasilia_tz)
        timestamp_brasilia = brasilia_time.timestamp()
        
        message = json.dumps({"timestamp": timestamp_brasilia, "price": price})
        producer.produce(topic, key=crypto_id, value=message)
        producer.flush()
        print(f"Enviado para Kafka ({topic}): {message}")

if __name__ == "__main__":
    while True:
        bitcoin_price = get_crypto_price("bitcoin")
        send_to_kafka(KAFKA_TOPIC_BTC, "bitcoin", bitcoin_price)
        
        ethereum_price = get_crypto_price("ethereum")
        send_to_kafka(KAFKA_TOPIC_ETH, "ethereum", ethereum_price)
        
        time.sleep(60)  # Espera 1 minuto antes da próxima coleta
