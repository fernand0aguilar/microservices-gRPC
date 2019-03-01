# Microservices GRPC
This repository is an implementation of two different services via gRPC, an open source remote procedure call system.

The first service, **DISCOUNT** is written in python and applies discounts to the price of a product based on the date.

The second service, **PRODUCTS LISTING** is written in go and returns a list of products exposed on a REST API. We can pass in the /products route an user-id, this will call the discount service and authenticate via tcp ssl. Header example: _X-USER-ID: 1_

#

# How to:

## Test if it's working:
Run both services.
The default ports are 11080 and 11443. 

You can test the system with the following command:

```curl -H 'X-USER-ID: 1' http://localhost:11080/products```


***

## **Run via docker:**
Requires:
* docker
* docker-compose

To run both services in detach mode:
```
clone the repo
cd microservices-grpc
docker-compose up -d
```
Generate the private keys for discount server if needed
```
openssl req -x509 -newkey rsa:4096 -keyout keys/private.key -out keys/cert.pem -days 365 -nodes -subj '/CN=discount'
```

## **Run locally:**

Requires:
* Go
* Python

To run **DISCOUNT** Python service:

Setup the environment
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install --upgrade pip \
&& pip install grpcio grpcio-tools
```
Run the discount server:
```python server.py 11443```

To run **PRODUCTS LISTING** Go service:
```
cd products_listing
go get -u google.golang.org/grpc
go get -u github.com/golang/protobuf/proto
go run main.go
```
Generate the private keys for localhost if needed
```
openssl req -x509 -newkey rsa:4096 -keyout keys/private.key -out keys/cert.pem -days 365 -nodes -subj '/CN=localhost'
```


***
Credits:
* [Github - microservices-grpc-go-python](https://github.com/gustavohenrique/microservices-grpc-go-python)
* [Website - gustavohenrique.com](https://gustavohenrique.com/)
