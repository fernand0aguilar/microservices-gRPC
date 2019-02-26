FROM golang

ADD . /app/src/microservices-grpc
WORKDIR /app/src/microservices-grpc

ENV GOPATH=/app
# RUN ls && pwd
RUN go get google.golang.org/grpc \
    && go get github.com/golang/protobuf/proto

CMD ["go", "run", "service02_products_listing/main.go"]