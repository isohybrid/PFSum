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
    data = dict(json.loads(encodedjson))

    # deal with the data
    f = open('portraffic.log', 'r')
    IN = 0
    OUT = 0
    for eachLine in f:
      tline = eachLine.split(',')
      if tline[2] == data['server_port'] and\
         tline[3] == data['local_port']:
           OUT += int(tline[4])
      elif tline[3] == data['server_port'] and\
           tline[2] == data['local_port']:
           IN += int(tline[4])
    ## traffic = {}.fromkeys(('IN', 'OU'),(IN, OUT))
    traffic = {'IN': IN, 'OUT': OUT}
    jsontra = json.dumps(traffic)
    f.close()

    tcpCliSock.send('[%s] %s' % (ctime(), jsontra))
    # tcpCliSock.send('[%s] %s' % (ctime(), encodedjson))
    print json.loads(encodedjson)

  tcpCliSock.close()
tcpSerSock.close()
