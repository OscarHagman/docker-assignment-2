FROM golang:alpine AS builder

WORKDIR /go/src/app
COPY main.go .

RUN go build main.go

FROM alpine
WORKDIR /app
COPY --from=builder /go/src/app /app/

CMD [ "./main" ]
