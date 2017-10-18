#!/usr/bin/env python
# encoding: utf-8

import eventlet
import pytun
import os

tun = pytun.open()
os.system("ip link set %s up" % tun.name)
os.system("ip link set dev %s mtu 520")
os.system("ip addr add 192.167.100.1/24 dev %s" % tun.name)

endpoint = set()

def handle(fd):
    endpoint.add(fd)
    while True:
        try:
            x = fd.readline()
            tun.send(x)
        except Exception:
            break
    endpoint.remove(fd)

def handletap():
    while True:
        msg = tun.recv()
        for e in endpoint:
            e.write(msg)
            e.flush()

eventlet.spawn_n(handletap)
server = eventlet.listen('0.0.0.0', 25021)
while True:
    try:
        new_sock, address = server.accept()
        eventlet.spawn_n(handle, new_sock.makefile('rw'))
    except (SystemExit, KeyboardInterrupt):
        tun.close()
        break
