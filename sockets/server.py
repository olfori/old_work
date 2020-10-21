''' Class server - return uppercase inp'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket


class Server:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('', 9090))
        self.sock.listen(1)
        self.start()

    def start(self):
        conn, addr = self.sock.accept()
        print('connected to:', addr)

        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.send(data.upper())

        conn.close()


if __name__ == '__main__':
    Server()
