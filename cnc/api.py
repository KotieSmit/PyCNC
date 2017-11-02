import BaseHTTPServer


class SimpleRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):

        print self.path
        self.wfile.write('HTTP-1.0 200 Okay\r\n\r\nHere is your output for '+self.path)

    def do_POST(self):

        print self.path
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        # self._set_headers()
        # self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        self.wfile.write('HTTP-1.0 200 Okay\r\n\r\nHere is your output for ' + self.path)
        self.wfile.write('HTTP-1.0 200 Okay\r\n\r\nHere is your output for ' + post_data)

def run(server_class=BaseHTTPServer.HTTPServer,
    handler_class=SimpleRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()