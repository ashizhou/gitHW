#!/usr/bin/env python3
# nameclient.py - Program to receive web name lookup command
# This CGI program used the python nameserver to lookup names
# And return result to web page
# James Skon, 2019
#!/usr/bin/env python
import os
from os import path
import sys

import cgi
import cgitb

cgitb.enable()

fifoname="team4"  # Unique name for fifos
sendFifoFile = "/home/fifo/"+fifoname+"_sendFifo"
getFifoFile = "/home/fifo/"+fifoname+"_getFifo"
def print_header():
    print ("""Content-type: text/html\n""")

def callChatServer(id,message):
    #Create Fifos if they don't exist
    if not path.exists(sendFifoFile):
        os.mkfifo(sendFifoFile)
        os.chmod(sendFifoFile, 0o777)
    if not path.exists(getFifoFile):
        os.mkfifo(getFifoFile)
        os.chmod(getFifoFile, 0o777)

    sendFifo=open(sendFifoFile, "w")
    getFifo=open(getFifoFile, "r")
    sendFifo.write(id+"_"+message)
    sendFifo.close()

    result=""
    for line in getFifo:
        result+=line
    getFifo.close()
    return(result)


def main():
    print_header()
    form = cgi.FieldStorage()
    if "message" not in form or "id" not in form:
        print("<H1>Error in Submission</H1>")

    id=form.getvalue("id")
    message=form.getvalue("message")
    result=callChatServer(id,message)
    result=result.replace("\n", "")
    print(result)


main()
