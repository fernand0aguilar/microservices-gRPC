FROM golang
ADD . /app/src/microservices-grpc
ENV GOPATH=/app

RUN go get -u google.golang.org/grpc \
    && go get -u github.com/golang/protobuf/proto

WORKDIR /app/src/microservices-grpc
CMD ["go", "run", "main.go"]