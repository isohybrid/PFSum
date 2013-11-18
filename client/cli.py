#!/usr/bin/env python

import json
from socket import *

PORT = 22222
BUFSIZ = 1024

data = {
    "server":"115.28.15.60",
    "server_port":'22',
    "local_port":'34163',
    "password":"k78931"
}

# data['server'] = socket.gethostbyaddr(data['server'])[2][0]
# print data

tcpCliSock = socket(AF_INET ,SOCK_STREAM)
tcpCliSock.connect((data['server'], PORT))

while True:
  encodedjson = json.dumps(data)
  tcpCliSock.send(encodedjson)
  tmp = tcpCliSock.recv(BUFSIZ)
  if not tmp:
    break
  print tmp

tcpCliSock.close()
