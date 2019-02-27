FROM grpc/python

ADD . /microservices-grpc
WORKDIR /microservices-grpc/discount

RUN ls && pip install --upgrade pip \
&& pip install grpcio grpcio-tools

CMD ["python", "server.py", "11443"]