# Secure gRPC Chat Application

This project is a secure gRPC-based chat application that implements bidirectional streaming for real-time communication between clients and the server. The communication is secured using SSL/TLS with pre-configured certificates.

## Features
- **Secure Communication**: Uses SSL/TLS for encryption.
- **Bidirectional Streaming**: Real-time message exchange between server and clients.
- **Threaded Client Handling**: Supports multiple clients simultaneously.

## Prerequisites

1. **Python**: Python 3.7+ is required.
2. **gRPC Tools**: Ensure `grpcio` and `grpcio-tools` are installed in your environment.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/mjunaid46/gRPC
cd gRPC
```
### 2. Install Dependencies
Install the required Python libraries:

```bash
pip install grpcio grpcio-tools
```
### 3. Run the Server
Start the server to handle client connections:
```bash
python server.py
```
### 4. Run the Client
Launch a client instance to connect to the server:
```bash
python client.py
```
## How It Works
### Server
- Loads SSL certificates (server.key, server.crt) for encrypted communication.
- Listens on port 50051 and accepts multiple client connections.
- Broadcasts messages received from any client to all connected clients.
### Client
- Verifies the server using the provided SSL certificate (server.crt).
- Connects to the server securely and starts a bidirectional stream for chat.
- Sends and receives messages in real-time.
## Configuration
### Server Configuration
The server runs on localhost:50051 by default. Update the server.py script to modify the address or port.

### Client Configuration
The client connects to localhost:50051 by default. Update the client.py script to modify the target address or port.

