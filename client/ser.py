#!/usr/bin/env python

from socket import *
from time import ctime
import json

HOST = '115.28.15.60'
PORT = 22222
BUFSIZ = 1024

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((HOST, PORT))
tcpSerSock.listen(5)

while(True):
  print 'waiting for connection...'
  tcpCliSock, addr = tcpSerSock.accept()
  print 'Connected from:', addr, '...'

  while True:
    encodedjson = tcpCliSock.recv(BUFSIZ)
    if not encodedjson:
      break

    # deal with the data
    f = open('portraffic.log', 'r')
    # for eachLine in f:

    tcpCliSock.send('[%s] %s' % (ctime(), encodedjson))
    print json.loads(encodedjson)

  tcpCliSock.close()
tcpSerSock.close()
