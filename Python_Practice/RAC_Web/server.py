#!/usr/bin/env python
 
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
 
server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 8000)
handler.cgi_directories = ["/etc_reg_dump","/cgi-bin",]
 
httpd = server(server_address, handler)
httpd.serve_forever()