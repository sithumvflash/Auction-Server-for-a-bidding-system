import socket
import sys
import threading
import time

import pandas as pd

SERVER_PORT = 2022
SERVER_IP = 'localhost'

stocks = {}


def handle_client(client_socket, client_id):
    client_socket.send(get_dict().encode())

    while True:
        data = client_socket.recv(1024).decode()
        args = data.split()

        code, amount = args
        amount = float(amount)
        if code in stocks:
            client_socket.send(bid(stocks[code], client_id, amount).encode())

        else:
            client_socket.send("Invalid Stock Code {}".format(code).encode())


def main():
    timeout = 4

    try:
        a = int(sys.argv[1])
        if a > 2:
            timeout = a
    except:
        pass

    print('Server waiting for connection')

    end = time.time() + (timeout * 60)
    data = pd.read_csv('stocks.csv')

    for i, row in data.iterrows():
        company = row['Company']
        code = row['Stock Code']
        base = row['Base price']
        security = row['Stock Security']
        profit = row['Profit']

        stocks[code] = {
            'company': company,
            'code': code,
            'base': base,
            'security': security,
            'profit': profit,
            'end': end,
            'current': base,
            'bids': []
        }

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    clients = {}

    while True:
        client_socket, client_address = server_socket.accept()
        print('Client connected from', client_address)
        client_id = client_socket.recv(1024).decode()
        clients[client_id] = client_socket

        thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        thread.start()


def get_dict():
    result = " Company    | Stock Code | Bid\n"

    for code, stock in stocks.items():
        result += " {} | {} | {}\n".format(stock['company'].ljust(10), stock['code'].ljust(10), stock['current'])

    return result


def bid(stock, user_id, bid):
    if stock['end'] < time.time():
        return "Bidding Ended - Invalid bid {} {}".format(stock['code'], bid)

    if stock['current'] >= bid:
        return "Invalid Bid"

    stock['current'] = bid
    stock['bids'].append({'user_id': user_id, 'bid': bid, 'when': time.time()})

    file = open("SYM.txt", "a")  # append mode
    file.write("{}\t{}\t{}\t{}\n".format(int(time.time()), stock['code'].ljust(6), user_id, bid))
    file.close()

    return "Successfully Bided! {} {}".format(stock['code'], bid)


if __name__ == '__main__':
    main()
