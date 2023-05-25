import socket
import sqlite3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 2020))
s.listen(1)
connection, address = s.accept()
data = connection.recv(1024)
lines = data.decode("utf-8") .splitlines()

getdata = lines[len(lines)-1]
getdata_list = getdata.split("&")

data_dict = {}
for param in getdata_list:
    key, value = param.split('=')
    data_dict[key] = value

print(data_dict)


conn = sqlite3.connect('form_data.db')



cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users_data
                  (username text, email text, password text)''')

cursor.execute("INSERT INTO users_data VALUES (?, ?, ?)", (data_dict['username'], data_dict['email'], data_dict['password']))

conn.commit()

conn.close()

connection.close()
