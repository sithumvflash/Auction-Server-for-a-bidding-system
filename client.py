import socket

from server import SERVER_PORT, SERVER_IP


def send_data(data):
    client_socket.send(data.encode())


def receive_data():
    return client_socket.recv(1024).decode()


def start_connection():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    client_id = input('Enter client ID: ')
    send_data(client_id)

    server_response = receive_data()
    print(server_response)


start_connection()

while True:
    stock_code = input('Enter stock code: ')
    bid_amount = input('Enter bid amount: ')

    send_data(stock_code + ' ' + bid_amount)

    server_response = receive_data()
    print(server_response)
