from http.server import BaseHTTPRequestHandler, HTTPServer

class InternalResourceHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.headers.get('X-Internal-Request') != 'true':
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"error": "Access denied"}')
            return
        # Simulate a sensitive internal resource
        if self.path == "/internal-service":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"secret": "This is a sensitive internal resource"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    # Run the internal resource server on port 5000
    server_address = ('127.0.0.1', 5000)
    httpd = HTTPServer(server_address, InternalResourceHandler)
    print("Internal resource server running on http://127.0.0.1:5000")
    httpd.serve_forever()