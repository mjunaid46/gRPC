import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc

# Implement the service defined in the .proto file
class ExampleServiceServicer(example_pb2_grpc.ExampleServiceServicer):
    def SayHello(self, request, context):
        response = example_pb2.HelloResponse()
        response.message = f"Hello, {request.name}!"
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
