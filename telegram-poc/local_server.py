from http.server import HTTPServer
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_connector import Handler

def run_local_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, Handler)
    print(f"Starting local server on port {port}...")
    print(f"Test the API at: http://localhost:{port}/api/telegram-connector")
    httpd.serve_forever()

if __name__ == "__main__":
    run_local_server() 