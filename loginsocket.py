import socket
import sqlite3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 8000))
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
rows=cursor.execute("SELECT * FROM users_data WHERE username=(?) AND password=(?)",(data_dict['username'], data_dict['password']))
rows=rows.fetchall()

if len(rows)==1:
    print("all ok")
else:
    print("try again")

conn.close()

connection.close()





















