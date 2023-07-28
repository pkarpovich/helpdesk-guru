import grpc
import gpt_pb2 as gpt
import gpt_pb2_grpc as gpt_grpc
class client_grpc:
   def __int__(self,target,contextName,conversationId):
       self.target=target
       self.contextName=contextName
       self.conversationId=conversationId
   def run(self,query):
    channel = grpc.insecure_channel(target=self.target)
    stub = gpt_grpc.GptServiceStub(channel)
    request = gpt.AskRequest(contextName=self.contextName, conversationId=self.conversationId, query=query)
    answer = stub.ask(request)
    response = answer.answer
    channel.close()
    return response 
