import requests
from flask import Flask, jsonify, request
from kafka import KafkaProducer
import json

app = Flask(__name__)

# Set up Kafka producer
kafka_bootstrap_servers = 'kafka-service:9092'
kafka_topic = 'orkor'
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Endpoint to handle a "buy" request and produce data object to Kafka
@app.route('/buy', methods=['POST'])
def handle_buy_request():
    data = request.get_json()
    username = data['username']
    userid = data['userid']
    price = data['price']
    timestamp = data['timestamp']

    purchase_data = {
        'username': username,
        'userid': userid,
        'price': price,
        'timestamp': timestamp
    }

    # Produce the data object to Kafka
    producer.send(kafka_topic, value=purchase_data)

    return jsonify({'message': 'Purchase successful'})

# Endpoint to handle a "getAllUserBuys" request
@app.route('/getAllUserBuys', methods=['GET'])
def handle_get_all_user_buys():
    # Send a GET request to the Customer Management service
    customer_management_service_url = 'http://api:5010/purchases'
    response = requests.get(customer_management_service_url)

    # Parse and present the response
    purchases = response.json()
    return jsonify(purchases)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5080, debug=True)

