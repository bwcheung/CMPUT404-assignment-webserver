#  coding: utf-8 
import SocketServer

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

from os import curdir
class MyWebServer(SocketServer.BaseRequestHandler):
    

    def handle(self):

	self.header = "HTTP/1.1 200 OK\r\n"
        self.type = ""
        self.lengthHeader = "Content-Length: "
	self.file = ""
        self.data = self.request.recv(1024).strip()

        print ("Got a request of: %s\n" % self.data)
	if (self.data[4] == "/"):
		i = 4
		namelist = list()
		while (self.data[i] != " "):
			namelist.append(self.data[i])
			i = i + 1
		namestr = ''.join(namelist)

	try:
		if (namestr.endswith(".css")):
			self.file = open(curdir + "/www" + namestr, "r").read()
			self.type = "Content-Type: text/css\r\n"
		elif (namestr.endswith(".html")):
			self.file = open(curdir + "/www" + namestr, "r").read()
			self.type = "Content-Type: text/html\r\n"
		elif (namestr.endswith("/")):
			self.file = open(curdir + "/www" + namestr + "/index.html", "r").read()
			self.type = "Content-Type: text/html\r\n"
		else:
			self.request.sendall("HTTP/1.1 301 Moved Permanently\r\nLocation: " + namestr + "/\r\n")
			print("HTTP/1.1 301 Moved Permanently\r\nLocation: " + namestr + "/\r\n")
	except:
		self.request.sendall("HTTP/1.1 404 Not Found\r\n")	

	self.length = self.lengthHeader + str(len(self.file)) + "\r\n"		
        self.request.sendall(self.header + self.type + self.length + "\r\n" + self.file)
	namelist = list()

    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
