"""
Concurrent File Server - Multi-threaded TCP Server
Handles multiple client connections simultaneously using threading.
Each client connection is handled by a separate thread.
"""

import socket
import threading
import time
import os
import sys
from config import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, SLEEP_TIME, FILES_DIRECTORY


class FileServerThread(threading.Thread):
    """Thread class to handle individual client file requests"""
    
    def __init__(self, client_socket, client_address, filename):
        """
        Initialize the file server thread
        
        Args:
            client_socket: Socket object for client connection
            client_address: Tuple containing client's address information
            filename: Name of the file requested by the client
        """
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.filename = filename
        self.daemon = True
        
    def run(self):
        """
        Thread execution method - handles file transfer to client
        """
        print(f"[THREAD {threading.current_thread().name}] Handling request from {self.client_address}")
        print(f"[THREAD {threading.current_thread().name}] Requested file: {self.filename}")
        
        try:
            # Construct the full file path
            file_path = os.path.join(FILES_DIRECTORY, self.filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                error_message = f"ERROR: File '{self.filename}' not found on server"
                self.client_socket.send(error_message.encode('utf-8'))
                print(f"[THREAD {threading.current_thread().name}] File not found: {self.filename}")
                return
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Send file size first
            self.client_socket.send(f"FILESIZE:{file_size}".encode('utf-8'))
            
            # Wait for acknowledgment
            ack = self.client_socket.recv(1024).decode('utf-8')
            if ack != "READY":
                print(f"[THREAD {threading.current_thread().name}] Client not ready")
                return
            
            print(f"[THREAD {threading.current_thread().name}] Starting file transfer ({file_size} bytes)")
            
            # Open and send file in chunks
            bytes_sent = 0
            with open(file_path, 'rb') as file:
                while True:
                    # Read chunk of data (max BUFFER_SIZE bytes)
                    chunk = file.read(BUFFER_SIZE)
                    
                    if not chunk:
                        break
                    
                    # Send the chunk
                    self.client_socket.send(chunk)
                    bytes_sent += len(chunk)
                    
                    print(f"[THREAD {threading.current_thread().name}] Sent {len(chunk)} bytes "
                          f"({bytes_sent}/{file_size} bytes total)")
                    
                    # Sleep for 200 milliseconds after each flush
                    time.sleep(SLEEP_TIME)
            
            print(f"[THREAD {threading.current_thread().name}] File transfer completed: {bytes_sent} bytes sent")
            
            # Send completion signal
            self.client_socket.send(b"EOF")
            
        except Exception as e:
            error_message = f"ERROR: {str(e)}"
            try:
                self.client_socket.send(error_message.encode('utf-8'))
            except:
                pass
            print(f"[THREAD {threading.current_thread().name}] Error: {str(e)}")
            
        finally:
            # Close the client socket
            self.client_socket.close()
            print(f"[THREAD {threading.current_thread().name}] Connection closed with {self.client_address}")


class ConcurrentFileServer:
    """Main server class that accepts connections and spawns threads"""
    
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        """
        Initialize the file server
        
        Args:
            host: Server host address
            port: Server port number
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.thread_count = 0
        
    def start(self):
        """Start the file server"""
        
        # Create server files directory if it doesn't exist
        if not os.path.exists(FILES_DIRECTORY):
            os.makedirs(FILES_DIRECTORY)
            print(f"[SERVER] Created directory: {FILES_DIRECTORY}")
        
        # Create TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Bind socket to address
            self.server_socket.bind((self.host, self.port))
            
            # Listen for incoming connections (max 5 in queue)
            self.server_socket.listen(5)
            
            self.running = True
            print(f"[SERVER] File Server started on {self.host}:{self.port}")
            print(f"[SERVER] Serving files from: {os.path.abspath(FILES_DIRECTORY)}")
            print(f"[SERVER] Buffer size: {BUFFER_SIZE} bytes")
            print(f"[SERVER] Sleep time: {SLEEP_TIME} seconds")
            print("[SERVER] Waiting for client connections...")
            
            self.accept_connections()
            
        except Exception as e:
            print(f"[SERVER] Error starting server: {str(e)}")
            sys.exit(1)
    
    def accept_connections(self):
        """Accept incoming client connections and spawn threads"""
        
        while self.running:
            try:
                # Accept client connection
                client_socket, client_address = self.server_socket.accept()
                
                print(f"\n[SERVER] New connection from {client_address}")
                
                # Receive filename from client
                filename = client_socket.recv(1024).decode('utf-8').strip()
                
                if filename:
                    # Create and start a new thread for this client
                    self.thread_count += 1
                    client_thread = FileServerThread(client_socket, client_address, filename)
                    client_thread.name = f"ClientThread-{self.thread_count}"
                    client_thread.start()
                    
                    print(f"[SERVER] Spawned {client_thread.name} for file: {filename}")
                else:
                    print(f"[SERVER] No filename received from {client_address}")
                    client_socket.close()
                    
            except KeyboardInterrupt:
                print("\n[SERVER] Shutting down server...")
                self.running = False
                break
            except Exception as e:
                print(f"[SERVER] Error accepting connection: {str(e)}")
                
        self.stop()
    
    def stop(self):
        """Stop the file server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("[SERVER] Server stopped")


def main():
    """Main function to start the server"""
    server = ConcurrentFileServer()
    server.start()


if __name__ == "__main__":
    main()
