import grpc
import gpt_pb2 as gpt
import gpt_pb2_grpc as gpt_grpc
def run():
    channel = grpc.insecure_channel(target=gRPC_server_address)
    stub = gpt_grpc.GptServiceStub(channel)
    request = gpt.AskRequest(contextName=contextName, conversationId=conversationId, query=query)
    answer = stub.ask(request)
    response = answer.answer
    print(response)
    channel.close()
