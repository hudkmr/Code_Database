#!/usr/bin/python -tt
'''
Toggle IP power switch
 
Uses fence_ip9258 file:
https://github.com/geertj/fence_ip9258
'''

import time
import subprocess, shlex
 
IP = '192.168.0.49'
login = 'admin'
passwd = '12345678'
 
def call_ippower(command):
  args = shlex.split(command)
  p = subprocess.call(command)
  return p
 
