'''Class client'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket


class Client:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect((b'localhost', 9090))
        self.sock.send(b'Test complited')
        self.start()

    def start(self):
        ''' Start client '''
        data = self.sock.recv(1024)
        self.sock.close()

        print(data)


if __name__ == '__main__':
    Client()
