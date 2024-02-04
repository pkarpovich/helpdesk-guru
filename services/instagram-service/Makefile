build_proto:
	mkdir -p ./lib && poetry run python -m grpc_tools.protoc -I ../../protos --python_betterproto_out=lib ../../protos/*.proto