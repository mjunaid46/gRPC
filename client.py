import grpc
import example_pb2
import example_pb2_grpc

def run():
    # Connect to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = example_pb2_grpc.ExampleServiceStub(channel)
        # Make a request
        response = stub.SayHello(example_pb2.HelloRequest(name="Junaid"))
        print(f"Received: {response.message}")

if __name__ == "__main__":
    run()
