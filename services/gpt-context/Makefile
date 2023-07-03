build_proto:
	mkdir -p ./lib && poetry run python -m grpc_tools.protoc -I ../../protos --python_betterproto_out=lib ../../protos/*.proto

init_vector_store:
	poetry run python gpt_context/ingest.py

weaviate_console:
	open https://console.weaviate.cloud/