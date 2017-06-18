from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from tensorflorserver import TensorFlowServer

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    
class Handler(BaseHTTPRequestHandler):
    counter = []  
    @classmethod
    def set_server(cls, tensorFlowServer):
      cls.tensorFlowServer = tensorFlowServer

    def do_GET(self):
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
 
        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def do_POST(self):
        post_body = self.rfile.read(int(self.headers['Content-Length']))
        print(post_body)
        tensor = TensorFlowServer()
        tensor.runServer(self.counter, ["localhost:2222", "localhost:2223"])
        print(len(self.counter))
        return