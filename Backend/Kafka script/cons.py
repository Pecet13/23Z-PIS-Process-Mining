from kafka import KafkaConsumer
import json
import requests  # If you're using HTTP requests to send data to your app

# Set up the Kafka consumer
consumer = KafkaConsumer(
    'logsmining_data',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='my-group'
)

# Continuously listen for messages
for message in consumer:
    data = json.loads(message.value)
    print(data)
    response = requests.post('https://pismining.azurewebsites.net/api/endpoint', json=data)
