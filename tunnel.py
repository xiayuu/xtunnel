#!/usr/bin/env python
# encoding: utf-8

import eventlet
import pytun
import os
import sys

tun = pytun.open('tap')
os.system("ip link set %s up" % tun.name)
os.system("ip link set dev %s mtu 520" % tun.name)
os.system("ip addr add 192.167.100.1/24 dev %s" % tun.name)

endpoint = set()


def handle(sock):
    while True:
        try:
            x = sock.recv(520)
            tun.send(x)
        except Exception,e:
            print(e)
            break

def handletap():
    net = None
    while True:
        msg = tun.recv()
        try:
            if not net:
                net = eventlet.connect((sys.argv[1], 25702))
            server.sendall(msg)
        except Exception,e:
            print(e)
            net = None

eventlet.spawn_n(handletap)
server = eventlet.listen(('0.0.0.0', 25702))
while True:
    try:
        new_sock, address = server.accept()
        eventlet.spawn_n(handle, new_sock)
    except (SystemExit, KeyboardInterrupt):
        tun.close()
        break
