FROM grpc/python
ADD . /microservices-gRPC
WORKDIR /microservices-gRPC/service01_discount
RUN pip install --upgrade pip \
&& pip install grpcio grpcio-tools
CMD ["python", "server.py", "11443"]