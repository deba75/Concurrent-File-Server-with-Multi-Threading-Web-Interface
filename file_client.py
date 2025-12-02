"""
File Client - TCP Client for downloading files from the server
Can be used as a standalone client or imported by the web interface
"""

import socket
import os
from config import SERVER_HOST, SERVER_PORT


class FileClient:
    """Client class for requesting files from the server"""
    
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        """
        Initialize the file client
        
        Args:
            host: Server host address
            port: Server port number
        """
        self.host = host
        self.port = port
        
    def download_file(self, filename, save_path=None):
        """
        Download a file from the server
        
        Args:
            filename: Name of the file to download
            save_path: Path where the file should be saved (optional)
            
        Returns:
            Dictionary containing status, message, and file info
        """
        if save_path is None:
            save_path = os.path.join('downloads', filename)
        
        # Create downloads directory if it doesn't exist
        download_dir = os.path.dirname(save_path)
        if download_dir and not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        try:
            # Create TCP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to server
            print(f"[CLIENT] Connecting to server {self.host}:{self.port}")
            client_socket.connect((self.host, self.port))
            print(f"[CLIENT] Connected to server")
            
            # Send filename to server
            print(f"[CLIENT] Requesting file: {filename}")
            client_socket.send(filename.encode('utf-8'))
            
            # Receive file size or error message
            initial_response = client_socket.recv(1024).decode('utf-8')
            
            # Check for error
            if initial_response.startswith("ERROR"):
                error_msg = initial_response.split("ERROR: ")[1]
                print(f"[CLIENT] Server error: {error_msg}")
                client_socket.close()
                return {
                    'status': 'error',
                    'message': error_msg,
                    'filename': filename
                }
            
            # Parse file size
            if initial_response.startswith("FILESIZE:"):
                file_size = int(initial_response.split(":")[1])
                print(f"[CLIENT] File size: {file_size} bytes")
            else:
                raise Exception("Invalid server response")
            
            # Send ready acknowledgment
            client_socket.send("READY".encode('utf-8'))
            
            # Receive file data
            print(f"[CLIENT] Receiving file...")
            bytes_received = 0
            
            with open(save_path, 'wb') as file:
                while bytes_received < file_size:
                    # Receive data chunk
                    chunk = client_socket.recv(4096)
                    
                    if not chunk:
                        break
                    
                    # Check for EOF marker
                    if chunk.endswith(b"EOF"):
                        chunk = chunk[:-3]  # Remove EOF marker
                        if chunk:
                            file.write(chunk)
                            bytes_received += len(chunk)
                        break
                    
                    file.write(chunk)
                    bytes_received += len(chunk)
                    
                    progress = (bytes_received / file_size) * 100
                    print(f"[CLIENT] Progress: {bytes_received}/{file_size} bytes ({progress:.1f}%)")
            
            print(f"[CLIENT] File downloaded successfully: {save_path}")
            print(f"[CLIENT] Total bytes received: {bytes_received}")
            
            client_socket.close()
            
            return {
                'status': 'success',
                'message': 'File downloaded successfully',
                'filename': filename,
                'save_path': save_path,
                'size': bytes_received
            }
            
        except ConnectionRefusedError:
            error_msg = f"Connection refused. Is the server running on {self.host}:{self.port}?"
            print(f"[CLIENT] {error_msg}")
            return {
                'status': 'error',
                'message': error_msg,
                'filename': filename
            }
            
        except Exception as e:
            error_msg = f"Error downloading file: {str(e)}"
            print(f"[CLIENT] {error_msg}")
            return {
                'status': 'error',
                'message': error_msg,
                'filename': filename
            }


def main():
    """Main function for standalone client usage"""
    print("=== File Download Client ===")
    print(f"Server: {SERVER_HOST}:{SERVER_PORT}\n")
    
    filename = input("Enter filename to download: ").strip()
    
    if not filename:
        print("No filename provided. Exiting.")
        return
    
    client = FileClient()
    result = client.download_file(filename)
    
    if result['status'] == 'success':
        print(f"\n✓ SUCCESS: {result['message']}")
        print(f"  File: {result['filename']}")
        print(f"  Saved to: {result['save_path']}")
        print(f"  Size: {result['size']} bytes")
    else:
        print(f"\n✗ ERROR: {result['message']}")


if __name__ == "__main__":
    main()
