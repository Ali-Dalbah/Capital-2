from http.server import SimpleHTTPRequestHandler
import socketserver
port = 5000
server = socketserver.TCPServer(("", port), SimpleHTTPRequestHandler)
def run():
  print('http server is ready')
  server.serve_forever()
