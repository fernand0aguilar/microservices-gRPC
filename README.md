# Microservices GRPC
This repository is an implementation of two different services via gRPC, an open source remote procedure call system.

The first service, **DISCOUNT** is written in python and applies discounts to the price of a product based on the date.

The second service, **PRODUCTS LISTING** is written in go and returns a list of products exposed on a REST API. We can pass in the /products route an user-id, this will call the discount service and authenticate via tcp ssl. Header example: _X-USER-ID: 1_

## How to:
### **Run via docker:**
```
clone the repo
cd microservices-grpc
./generate_keys.sh
docker-compose up -d
```
the default ports are 11080 and 11443. You can test the system by the following command:
```curl -H 'X-USER-ID: 1' http://localhost:11080/products```


### **Run locally:**

Requires:
* Go
* Python

To run **DISCOUNT** service:

Setup the environment:
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install --upgrade pip \
&& pip install grpcio grpcio-tools
```
Run the discount server:
```python server.py 11443```

To run **PRODUCTS LISTING** service:
```
cd products_listing
go run main.go
```
The ports are also 11080 and 11443. 
You can test with the same curl command:

```curl -H 'X-USER-ID: 1' http://localhost:11080/products```

***
Credits:
* [Github - microservices-grpc-go-python](https://github.com/gustavohenrique/microservices-grpc-go-python)
* [Website - gustavohenrique.com](https://gustavohenrique.com/)
