import BaseHTTPServer, SimpleHTTPServer
import ssl

httpd = BaseHTTPServer.HTTPServer(
    ('0.0.0.0', 4443),
    SimpleHTTPServer.SimpleHTTPRequestHandler
)
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    server_side=True,
    certfile='dev-server.local.pem',
    keyfile='dev-server.local.key'
)
httpd.serve_forever()
