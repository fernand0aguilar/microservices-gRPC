FROM grpc/python
LABEL author="Fernando Aguilar <fernando.aguilar@hotmail.com.br>"

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip \
&& pip install grpcio grpcio-tools

CMD ["python", "server.py", "11443"]