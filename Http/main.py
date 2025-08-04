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

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            new_contact = json.loads(body)
        except json.JSONDecodeError:
            self.send_json({'error': 'Invalid JSON'}, status=400)
            return
        new_contact['id'] = max([c['id'] for c in contacts], default=0) + 1
        contacts.append(new_contact)
        self.send_json({'message': 'Contact added', 'contact': new_contact}, status=201)
    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_json({'error': 'Invalid JSON'}, status=400)
            return

        contact_id = data.get('id')
        if contact_id is None:
            self.send_json({'error': 'ID is required'}, status=400)
            return

    
        for i, contact in enumerate(contacts):
            if contact['id'] == contact_id:
                contacts[i] = data
                self.send_json({'message': 'Contact updated', 'contact': data})
                return

        self.send_json({'error': 'Contact not found'}, status=404)

    def do_PATCH(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            patch_data = json.loads(body)
        except json.JSONDecodeError:
            self.send_json({'error': 'Invalid JSON'}, status=400)
            return

        contact_id = patch_data.get('id')
        if contact_id is None:
            self.send_json({'error': 'ID is required'}, status=400)
            return
        for contact in contacts:
            if contact['id'] == contact_id:
                contact.update({k: v for k, v in patch_data.items() if k != 'id'})
                self.send_json({'message': 'Contact patched', 'contact': contact})
                return

        self.send_json({'error': 'Contact not found'}, status=404)
    def do_DELETE(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            delete_data = json.loads(body)
        except json.JSONDecodeError:
            self.send_json({'error': 'Invalid JSON'}, status=400)
            return

        contact_id = delete_data.get('id')
        if contact_id is None:
            self.send_json({'error': 'ID is required'}, status=400)
            return


        for contact in contacts:
            if contact['id'] == contact_id:
                contacts.remove(contact)
                self.send_json({'message': 'Contact deleted', 'contact': contact})
                return

        self.send_json({'error': 'Contact not found'}, status=404)

# Starts the server
def run():
    print("Server running at http://127.0.0.1:8000")
    HTTPServer(('localhost', 8000), SimpleHandler).serve_forever()

# Start server when file is run
run()
