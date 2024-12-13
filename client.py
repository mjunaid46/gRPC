import grpc
import chat_pb2
import chat_pb2_grpc
import threading
import sys
import time
from queue import Queue
from grpc import ssl_channel_credentials


def handle_server_responses(response_iterator, response_queue):
    """Handle server responses and add them to a queue."""
    try:
        for response in response_iterator:
            response_queue.put(f"{response.user}: {response.message}")
    except grpc.RpcError as e:
        response_queue.put(f"Error occurred: {e.details()}")

def chat():
    # Load the CA certificate to verify the server
    with open('ca.crt', 'rb') as f:
        trusted_certs = f.read()

    # Create SSL credentials using the trusted CA certs
    credentials = ssl_channel_credentials(root_certificates=trusted_certs)

    # Create a secure channel to connect to the server
    with grpc.secure_channel('localhost:50051', credentials) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        response_queue = Queue()

        def message_generator():
            """Generate messages from user input only after the server response is handled."""
            while True:
                # Wait for the server's response to be fully processed before accepting new input
                while not response_queue.empty():  # Only allow new input if the queue is empty
                    pass  # Do nothing, wait until the server's response is processed

                user = input("\nEnter your username: ").strip()
                message = input("Enter your message: ").strip()
                yield chat_pb2.ChatMessage(user=user, message=message)
                time.sleep(2)

        # Start a thread to handle server responses
        response_iterator = stub.Chat(message_generator())
        response_thread = threading.Thread(
            target=handle_server_responses, args=(response_iterator, response_queue)
        )
        response_thread.daemon = True
        response_thread.start()

        # Main loop to display server responses and control input
        while True:
            # Wait until the server's response is processed
            while not response_queue.empty():
                print(f"\n{response_queue.get()}")
                sys.stdout.flush()  # Ensure output order is correct

            # Only prompt for new input if the server has responded and the queue is empty
            if response_queue.empty():
                continue  # Wait until the response from the server is fully processed

if __name__ == "__main__":
    chat()
