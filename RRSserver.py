#!/usr/bin/env python

from lxml import etree
from lxml.builder import E
import psycopg2
import tempfile
import pdfkit
import psycopg2.extras
import sys, ast
import os
import socket
from threading import Thread
from SocketServer import ThreadingMixIn

TCP_IP = 'localhost'	#limiting incoming connections to local server for safety
TCP_PORT = 9001
BUFFER_SIZE = 1024

def joinclass(*args):
  return {"class":' '.join(args)}

def joindiv(*args):
  return {"align":' '.join(args)}

#in a prod env the below login params would be part of the API call instead?
conn_string = "host='candidate.suade.org' dbname='suade' user='interview' password='LetMeIn'"
conn = psycopg2.connect(conn_string)	#setting up postgresql connection
cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
cursor.execute('SELECT * FROM reports LIMIT 1000')
data1 = []	#loading the database:
for row in cursor:
	data1.append(row)

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print " New thread started for "+ip+":"+str(port)

    def run(self):
		callparams = self.sock.recv(1024)
		print callparams.split(',')
		FileType = callparams.split(',')[0]	#deducing filetype from API call
		Record = int(callparams.split(',')[1])	#deducing Record# from API call
		currrow = ast.literal_eval(data1[Record][1])
		orgname = currrow["organization"]
		reported = currrow["reported_at"]
		created = currrow["created_at"]
		inventory = currrow["inventory"]
		#BEGIN reusable tamplate : not bothered with a jinja flask template to avoid file fragmentation
		html = (
		   E.html(       # create an Element called "html"
			 E.body(
			   E.h1("The Report", joinclass("title")),			 
			   E.div("Organization: ", orgname, joindiv("right")),
					 E.div("Reported: ", reported, joindiv("right")),
					 E.div("Created: ", created, joindiv("right")),
					 E.TABLE(
						 *[E.TR(
							 *[
								 E.TD("%s : %s" % (item["name"], item["price"]))
								]
								) for item in inventory]
					)
			 )
		   )
		 )
		#END reusable tamplate : not bothered with a jinja flask template to avoid file fragmentation
		# write to file: exporting both files
		tree = etree.ElementTree(html)
		if FileType == 'pdf':
			l = etree.tostring(html, pretty_print=True, xml_declaration=True)
		elif FileType == 'xml':
			l = etree.tostring(html, pretty_print=True, xml_declaration=True)
		else:
			print 'incorrect filetype request'
			self.sock.close()
		
		self.sock.send(l)
		self.sock.close()

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)	#will accept upto 5 concurrent connections
    print "Waiting for incoming connections ..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got connection from ', (ip,port)
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
