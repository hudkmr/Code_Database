#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
s_addr = form.getvalue('start_address')
e_addr  = form.getvalue('end_address')
o_filename = form.getvalue('output_file_name')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s %s %s</h2>" % (s_addr,e_addr,o_filename)
print "<h3>Hello this third title and is located with a folder in server"
print "</body>"
print "</html>"