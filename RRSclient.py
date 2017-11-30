#!/usr/bin/env python

import socket
import tempfile
from lxml import etree
import pdfkit
import os

Record = 0
FileType = 'pdf'
TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

if os.name == 'nt':	#setting pdfkit config for windows
	path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
	pdfkitconfig = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(FileType + ',' + str(Record))
temphtmlfile = tempfile.mktemp('.html')	#creating temp unique file to discard later
with open(temphtmlfile, 'wb') as f:
	print 'file opened'
	data = s.recv(BUFFER_SIZE)
	if not data:
		f.close()
		print 'file closed, no data'
	f.write(data)	#saving temp html to convert to pdf
	f.close()
	if FileType == 'pdf':
		pdfkit.from_file(temphtmlfile, 'output.pdf', configuration=pdfkitconfig)
	elif FileType == 'xml':	#xml: direct transform asked for, so didn't bother reformatting @ correct xml structure
		with open('output.xml', 'wb') as xmlFile:
			xmlFile.write(data)
			xmlFile.close()		
	os.remove(temphtmlfile)	#removing temp file
	print('Successfully received file')

s.close()
print('connection closed')
