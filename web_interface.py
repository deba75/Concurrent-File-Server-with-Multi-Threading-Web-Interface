"""
Web Interface for Concurrent File Server
Provides an interactive web UI for downloading files from the server
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import threading
from file_client import FileClient
from config import SERVER_HOST, SERVER_PORT, WEB_HOST, WEB_PORT, FILES_DIRECTORY

app = Flask(__name__)
CORS(app)

# Store download results
download_results = {}
download_lock = threading.Lock()


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/files', methods=['GET'])
def list_files():
    """Get list of available files on the server"""
    try:
        if not os.path.exists(FILES_DIRECTORY):
            return jsonify({
                'status': 'error',
                'message': 'Server files directory not found',
                'files': []
            })
        
        files = []
        for filename in os.listdir(FILES_DIRECTORY):
            filepath = os.path.join(FILES_DIRECTORY, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                files.append({
                    'name': filename,
                    'size': size,
                    'size_formatted': format_file_size(size)
                })
        
        files.sort(key=lambda x: x['name'])
        
        return jsonify({
            'status': 'success',
            'files': files,
            'count': len(files)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'files': []
        })


@app.route('/api/download', methods=['POST'])
def download_file():
    """Download a file from the server and send to browser"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({
                'status': 'error',
                'message': 'Filename is required'
            })
        
        # Create client and download file to temp location
        import tempfile
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        
        client = FileClient(SERVER_HOST, SERVER_PORT)
        result = client.download_file(filename, save_path=temp_path)
        
        # Store result
        with download_lock:
            download_results[filename] = result
        
        if result['status'] == 'success':
            # Return the file path for browser download
            return jsonify({
                'status': 'success',
                'message': 'File ready for download',
                'filename': filename,
                'download_url': f'/api/get-file/{filename}',
                'size': result['size']
            })
        else:
            return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/get-file/<filename>', methods=['GET'])
def get_file(filename):
    """Send the downloaded file to browser"""
    try:
        import tempfile
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        
        if os.path.exists(temp_path):
            return send_file(
                temp_path,
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({
                'status': 'error',
                'message': 'File not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/server-status', methods=['GET'])
def server_status():
    """Check if the file server is running"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((SERVER_HOST, SERVER_PORT))
        sock.close()
        
        if result == 0:
            return jsonify({
                'status': 'online',
                'host': SERVER_HOST,
                'port': SERVER_PORT
            })
        else:
            return jsonify({
                'status': 'offline',
                'host': SERVER_HOST,
                'port': SERVER_PORT
            })
    except:
        return jsonify({
            'status': 'offline',
            'host': SERVER_HOST,
            'port': SERVER_PORT
        })


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload a file to the server directory"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            })
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            })
        
        # Save file to server directory
        if not os.path.exists(FILES_DIRECTORY):
            os.makedirs(FILES_DIRECTORY)
        
        filepath = os.path.join(FILES_DIRECTORY, file.filename)
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        
        return jsonify({
            'status': 'success',
            'message': 'File uploaded successfully',
            'filename': file.filename,
            'size': file_size
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a file from the server directory"""
    try:
        filepath = os.path.join(FILES_DIRECTORY, filename)
        
        if not os.path.exists(filepath):
            return jsonify({
                'status': 'error',
                'message': 'File not found'
            })
        
        os.remove(filepath)
        
        return jsonify({
            'status': 'success',
            'message': 'File deleted successfully',
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def main():
    """Start the web server"""
    print(f"Starting Web Interface on http://{WEB_HOST}:{WEB_PORT}")
    print(f"Connected to File Server: {SERVER_HOST}:{SERVER_PORT}")
    print(f"Server Files Directory: {os.path.abspath(FILES_DIRECTORY)}")
    app.run(host=WEB_HOST, port=WEB_PORT, debug=True, threaded=True)


if __name__ == '__main__':
    main()
