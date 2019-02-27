FROM golang

ADD . /app/src/microservices-grpc
ENV GOPATH=/app

WORKDIR /app/src/microservices-grpc/products_listing

RUN go get google.golang.org/grpc \
    && go get github.com/golang/protobuf/proto

CMD ["go", "run", "main.go"]