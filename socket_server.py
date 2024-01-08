from datetime import datetime
import logging
import socket
import json


SOCKET_ADDRESS = "127.0.0.1", 5000
PATH_SAVE_DATA = "front-init/storage/data.json"


def read_data(data_path:str) -> dict:
    with open(data_path, "r") as file:
        data = json.load(file)
    return data


def save_data(data: str, data_path:str) -> None:
    data_dict = read_data(data_path)
    data = {key: value for key, value in [el.split('=') for el in data.split('&')]}
    time = str(datetime.now())
    data_dict[time] = data
    
    with open(data_path, "w") as file:
        json.dump(data_dict, file)


def run_socket_server() -> None:
    logging.debug("Run http server.")

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(SOCKET_ADDRESS)
    try:
        while True:
            
            try:
                data, address = server.recvfrom(1024)
                logging.debug("Data started to be stored.")
                save_data(data.decode(), PATH_SAVE_DATA)
                logging.debug("Data has been successfully saved.")
            
            except OSError:
                logging.debug("Failed to save data, message too long.")

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        server.close()


if __name__ == "__main__":
    run_socket_server()
    # save_data("username=Krabat&message=Second message", PATH_SAVE_DATA)
