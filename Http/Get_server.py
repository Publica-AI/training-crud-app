from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# In-memory list acting as a database of contacts
contacts = [
    {"id": 1, "name": "Moji", "phone": "876654326"},
    {"id": 2, "name": "Alex", "phone": "123456789"}
]

class SimpleHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        self.send_json(contacts)
        
        # Starts the server
def run():
    print("Server running at http://127.0.0.1:8000")
    HTTPServer(('localhost', 8000), SimpleHandler).serve_forever()

# Start server when file is run
run()
