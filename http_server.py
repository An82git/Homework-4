from socket_server import SOCKET_ADDRESS

from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import urllib.parse
import mimetypes
import logging
import socket


SERVER_ADDRESS = "127.0.0.1", 3000


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('front-init/index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('front-init/message.html')
        else:
            if Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('front-init/error.html', 404)

    def do_POST(self) -> None:
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        
        self.sending_data(data_parse, SOCKET_ADDRESS)
        logging.debug("The data was sent for storage.")
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename, status=200) -> None:
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self) -> None:
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def sending_data(self, data:str, socket_address:tuple) -> None:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(data.encode(), socket_address)
        client.close()


def run_http_server() -> None:
    logging.debug("Run socket server.")
    server = HTTPServer(SERVER_ADDRESS, HttpHandler)
    server.serve_forever()


if __name__ == "__main__":
    run_http_server()
