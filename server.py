import grpc
from concurrent import futures
import chat_pb2
import chat_pb2_grpc
from grpc import ssl_channel_credentials



# Paths to your .crt and .key files
server_crt = 'server.crt'  # Server certificate
server_key = 'server.key'  # Server private key
ca_crt = 'ca.crt'  # CA certificate (optional, if you want to authenticate clients)

# Load the server certificate and private key
with open(server_crt, 'rb') as f:
    server_certificate = f.read()

with open(server_key, 'rb') as f:
    server_private_key = f.read()

# Optionally, load the CA certificate for client authentication
with open(ca_crt, 'rb') as f:
    trusted_certificates = f.read()
# Create server credentials using the certificate and private key
server_credentials = grpc.ssl_server_credentials(
    [(server_private_key, server_certificate)],
    root_certificates=trusted_certificates,
    require_client_auth=False  # Change this to True if you require client authentication
)
# Optionally, load the CA certificate for client authentication
with open(ca_crt, 'rb') as f:
    trusted_certificates = f.read()

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def Chat(self, request_iterator, context):
        for chat_message in request_iterator:
            print(f"Received from {chat_message.user}: {chat_message.message}")
            yield chat_pb2.ChatMessage(user="Server", message=f"Echo from server: {chat_message.message}")

def serve():
    

    # Create the server and add the secure port
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)

    # Use secure port with SSL
    server.add_secure_port('localhost:50051', server_credentials)

    server.start()
    print("Server started on secure port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
