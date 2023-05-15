build_proto:
	mkdir -p ./services/telegram-bot/lib && protoc --proto_path=./protos/ --go_out=. --go-grpc_out=. ./protos/*.proto

