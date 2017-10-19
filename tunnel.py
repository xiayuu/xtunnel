#!/usr/bin/env python
# encoding: utf-8

import eventlet
import pytun
import os
import sys

tun = pytun.open()
os.system("ip link set %s up" % tun.name)
os.system("ip link set dev %s mtu 520" % tun.name)
os.system("ip addr add 192.167.100.1/24 dev %s" % tun.name)

endpoint = set()


def handle(fd):
    while True:
        try:
            x = fd.readline()
            print("net recv:%s" % x)
            tun.send(x)
        except Exception:
            break

def handletap():
    server = None
    while True:
        msg = tun.recv()
        print("tun recv:%s" % msg)
        try:
            if not server:
                server = eventlet.connect((sys.argv[1], 25702))
            server.sendall(msg)
        except Exception:
            server = None

eventlet.spawn_n(handletap)
server = eventlet.listen(('0.0.0.0', 25702))
while True:
    try:
        new_sock, address = server.accept()
        eventlet.spawn_n(handle, new_sock.makefile('rw'))
    except (SystemExit, KeyboardInterrupt):
        tun.close()
        break
