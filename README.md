# OrkorChart Helm Repository

This repository contains a collection of Helm charts for the task. Follow the instructions below to fetch and install the desired artifacts using Helm.

## Prerequisites

- Helm CLI installed on your machine. See the Helm documentation for installation instructions.

## Adding the Helm Repository

To access the OrkorChart Helm repository, you need to add it as a repository in Helm. Use the following command:

```
helm repo add orkorhelm https://orkoresh4.github.io/orkorchart/
```

## Searching for Available Charts

- To see the available charts in the OrkorChart repository, use the following command:
 ```
 helm search repo orkorhelm
 ```

## Fetching and Installing Charts
- To fetch and install a specific chart, use the helm install command followed by the name of the chart and a release name:

  ```
	helm install kafka orkorhelm/orkor-kafka-chart
	helm install mongo orkorhelm/orkor-mongo-chart
	helm install web orkorhelm/orkor-web-chart
	helm install api orkorhelm/orkor-api-chart
  ```


API:


* When Kafka is up and running, run consume request so the API server will start consuming from kafka:

```

	curl -X POST http://<api SERVICE IP>:5010/consume

```




Kafka:

* If you want to debug Kafk  ,add kafaka-service IP to etc/hosts:
```
	<kafka-service SERVICE IP> kafka-service
```
* Check that kafka topic is getting updated:
  ```
	kafkacat -b <kafka-service SERVICE IP>:9092 -C -t orkor
  ```



Web:

* Preform Buy Request
```
 curl -X POST -H "Content-Type: application/json" -d '{"username": "helmkafka", "userid": "111123", "price": 1222, "timestamp": "2023-07-07T12:00:00"}' http://<web SERVICE IP>:5080/buy
```
 * Handle a “getAllUserBuys” request:
```
 curl http://<web SERVICE IP>:5080/getAllUserBuys
```
 Mongo:

 * Login to mongo to verify buy reqeusts have been updated:
```
  mongo --host <mongo-nodeport-svc SERVICE IP> --port 27017 --username adminuser --password password123 --authenticationDatabase admin
  
  use testdb

  db.testcollection.find()
```



You can find the scripts for web and api servers in scripts folder:

https://github.com/orkoresh4/orkorchart.git




