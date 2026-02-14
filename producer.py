import requests, time, json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    try:
        data = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        payload = {"symbol": data["symbol"], "price": float(data["price"])}
        producer.send('crypto_prices', payload)
        print(f"Sent: {payload}")
    except:
        print("API Error, retrying...")
    time.sleep(2)