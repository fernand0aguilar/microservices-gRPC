FROM grpc/python
ADD . /microservices-grpc
WORKDIR /microservices-grpc/service01_discount
RUN pip install --upgrade pip \
&& pip install grpcio grpcio-tools
CMD ["python", "server.py", "11443"]