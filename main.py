from http_server import run_http_server
from socket_server import run_socket_server

from threading import Thread
import logging


threads = []


def run_servers() -> None:
    http_server = Thread(target=run_http_server)
    socket_server = Thread(target=run_socket_server)

    threads.append(http_server)
    threads.append(socket_server)

    http_server.start()
    socket_server.start()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    logging.debug("Start of the program.")

    run_servers()

    [el.join() for el in threads]

    logging.debug("End of the program.")


if __name__ == "__main__":
    main()
