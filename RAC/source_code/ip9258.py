#!/usr/bin/python -tt
'''
Toggle IP power switch
 
Uses fence_ip9258 file:
https://github.com/geertj/fence_ip9258
'''

import time
import subprocess, shlex
 
IP = '10.64.44.152'
login = 'admin'
passwd = '12345678'
 
def call_ippower(command):
  args = shlex.split(command)
  p = subprocess.call(command)
  return p
 
