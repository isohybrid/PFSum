#!/usr/bin/env python

data = {
    'server': '115.28.15.60',
    'server_port': '22',
    'local_port': '34163',
    'password': "k78931"
}

IN = 0
OU = 0

f = open('portraffic.log', 'r')
for eachLine in f:
  tline = eachLine.split(',')
  ## print '----------------------------------------'
  ## print tline
  ## print tline[0], tline[2], tline[3]
  ## print data['server'], data['server_port'], data['local_port']
  ## print 'local_port:', tline[3], ',', data['local_port'], 'server_port:', tline[2], ',', data['server_port']
  ## if (tline[3] == data['local_port']) and (tline[2] == data['server_port']):
  ## if not cmp((tline[3]+tline[2]), (data['local_port']+data['server_port'])):
  if tline[3] == data['local_port'] and tline[2] == data['server_port']:
    ## print 'src IP:', tline[0], 'server PORT:', tline[2]
    IN += int(tline[4])
  elif tline[2] == data['local_port'] and tline[3] == data['server_port']:
    OU += int(tline[4])
  '''
  if tline[0] == data['server'] and \
     tline[2] == data['server_port'] and \
     tline[3] == data['local_port']:
       print "equal"
       print tline[0], tline[2], tline[3]
       print data['server'], data['server_port'], data['local_port']
       OU += tline[4]
  if tline[1] == data['server'] and \
     tline[3] == data['server_port'] and \
     tline[2] == data['local_port']:
       IN += tline[4]
  '''
##traffic = {}.fromkeys(('IN', 'OUT'), (IN, OU))
traffic = {'OUT': OU, 'IN': IN}
print traffic
f.close()
