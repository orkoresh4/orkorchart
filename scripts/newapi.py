from flask import Flask, jsonify, request
from pymongo import MongoClient
import base64
from kafka import KafkaConsumer
from threading import Thread
import json

# Decode the base64-encoded credentials
username = base64.b64decode("YWRtaW51c2Vy").decode('utf-8')
password = base64.b64decode("cGFzc3dvcmQxMjM=").decode('utf-8')

# Set up MongoDB connection
mongo_client = MongoClient('mongodb://' + username + ':' + password + '@mongo-nodeport-svc:27017/')
db = mongo_client['testdb']
collection = db['testcollection']

# Set up Kafka consumer
kafka_bootstrap_servers = 'kafka-service:9092'
kafka_topic = 'orkor'
consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_bootstrap_servers)

def consume_messages():
    for message in consumer:
        # Assuming the message is in JSON format
        data = json.loads(message.value.decode('utf-8'))
        print('Received message:', data)  # Print the consumed message
        try:
            # Insert the data into MongoDB
            collection.insert_one(data)
            print('Message processed successfully')
        except Exception as e:
            print('Error:', str(e))

def get_all_purchases():
    # Query all documents from the collection
    purchases = list(collection.find())

    # Transform the documents into a list of dictionaries
    purchase_list = []
    for purchase in purchases:
        purchase_dict = {
            'username': purchase['username'],
            'userid': purchase['userid'],
            'price': purchase['price'],
            'timestamp': purchase['timestamp']
        }
        purchase_list.append(purchase_dict)

    return purchase_list

app = Flask(__name__)

# Endpoint to return all customer purchases
@app.route('/purchases', methods=['GET'])
def get_all_purchases_route():
    purchases = get_all_purchases()
    return jsonify(purchases)

# Define an API endpoint to consume messages from Kafka and write to MongoDB
@app.route('/consume', methods=['POST'])
def consume_and_write():
    # Start the Kafka consumer in a separate thread
    consumer_thread = Thread(target=consume_messages)
    consumer_thread.start()

    return {'message': 'Consuming messages from Kafka and writing to MongoDB.'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)

