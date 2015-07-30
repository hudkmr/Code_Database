#!rebol -cs
REBOL []
print "Content-type: text/html^/"

html: make string! 2000
emit: func [data] [repend html data]

emit [
    <HTML><BODY BGCOLOR="#FFC080">
    <b> "CGI Form Data:" </b><p>
    "Submitted: " now <BR>
    "REBOL Version: " system/version <P>
    <TABLE BORDER="1" CELLSPACING="0" CELLPADDING="5">
]

foreach [var value] decode-cgi system/options/cgi/query-string [
    emit [<TR><TD> mold var </TD><TD> mold value </TD></TR>]
]

emit [</TABLE></BODY></HTML>]
print html