from ip_header import *
from tcp_header import *

s = socket.socket(socket.AF_INET,
                  socket.SOCK_RAW,
                  socket.IPPROTO_RAW)
src_host = "10.0.2.15"
dest_host = socket.gethostbyname("www.reddit.com")
data = "TEST!!"
 
# IP Header
ipobj = ip(src_host, dest_host)
iph = ip_object.pack()
 
# TCP Header
tcpobj = tcp(1234, 80)
tcpobj.data_length = len(data)  # Used in pseudo header
tcph = tcpobj.pack(ipobj.source,
                   ipobj.destination)
 
# Injection
packet = iph + tcph + data
s.send(packet, (dest_host, 0))