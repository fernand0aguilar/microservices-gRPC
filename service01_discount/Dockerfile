FROM grpc/python
ADD . /microservices-grpc
WORKDIR /microservices-grpc
RUN ls && pip install --upgrade pip \
&& pip install grpcio grpcio-tools
CMD ["python", "service01_discount/server.py", "11443"]