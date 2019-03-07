FROM golang
LABEL author="Fernando Aguilar <fernando.aguilar@hotmail.com.br>"

COPY . /app/src/github.com/fernand0aguilar/microservices-grpc/products_listing
WORKDIR /app/src/github.com/fernand0aguilar/microservices-grpc/products_listing

ENV PORT 11080


RUN go get google.golang.org/grpc \
    && go get github.com/golang/protobuf/proto \
    && go get github.com/fernand0aguilar/microservices-grpc/tree/v1.0/products_listing

RUN sh -c "go build -i -v -o products_listing main.go \
    && mv products_listing /usr/local/bin"

CMD ["products_listing"]