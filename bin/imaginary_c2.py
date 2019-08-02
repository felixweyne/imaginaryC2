__author__ = "Felix Weyne, 2017"

#Imaginary C2:
#-Capture HTTP requests towards selectively chosen domains/IPs
#-Easily replay captured C&C responses/served payloads

#Imaginary C2 is a python tool which aims to help in the behavioral (network) analysis of malware. Imaginary C2 hosts a HTTP server which captures HTTP requests 
#towards selectively chosen domains/IPs. Additionally, the tool aims to make it easy to replay captured Command-and-Control responses/served payloads.
#By using this tool, an analyst can feed the malware consistent network responses (e.g. C&C instructions for the malware to execute). Additionally, the analyst can
#capture and inspect HTTP requests towards a domain/IP which is offline at the time of the analysis.

#Created for python 2.7, intended to run on a Windows virtual machine

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import datetime
import os
import ssl
import urllib
import urlparse
import json
import sys
import subprocess
from pprint import pprint
import re
import base64 
from os.path import dirname, abspath
from threading import Thread
from SocketServer import ThreadingMixIn

one_directory_up = dirname(dirname(abspath(__file__)))	
config_data = json.load(open(one_directory_up+'\\requests_config.txt'))
server_data_folder = one_directory_up + "\\server_data\\"
bin_folder = one_directory_up + "\\bin\\"
HTTP_oneDotOne_enabled=False
#pprint(config_data)

def printlog(logMessage,isResponse=False):
	file = open(os.path.join(os.environ["HOMEPATH"], "Desktop")+'\imaginary_c2_server_log.txt', 'ab')
	if not isResponse:
		print logMessage
		file.write(logMessage+"\n")
	else:
		file.write("----- OUTGOING Response ----->\n")
		file.write(logMessage+"\n")
		file.write("<----------------\n\n")
	file.close()
	
request_count = 0
fixed_URL_list = []
regex_URL_list = []

for config_entry in config_data["requests"]:
	url_type = config_entry["urltype"]
	if url_type == "fixed":
		fixed_URL_list.append(config_entry["url"])
	elif url_type == "regex":
		regex_URL_list.append(config_entry["url"])

class RequestHandler(BaseHTTPRequestHandler): 
	if HTTP_oneDotOne_enabled:
		protocol_version = 'HTTP/1.1'

	#remove this to get default SimpleHTTP server log output 
	#overwrites function log_message in Python27\Lib\BaseHTTPServer.py
	def log_message(self, format, *args):
		return

	def do_GET(self):    
		request_path = self.path
		self.log_my_request("GET")
		self.send_response(200)

		self.process_request(request_path)

	def do_POST(self):
		request_path = self.path

		request_headers = self.headers
		content_length = request_headers.getheaders('content-length')
		length = int(content_length[0]) if content_length else 0
		post_contents = self.rfile.read(length)

		self.log_my_request("POST",post_contents)
		self.send_response(200)
		self.process_request(request_path,post_contents)

	def log_my_request(self,request_type,post_contents=""):
		request_path = self.path
		
		global request_count
		request_count = request_count + 1
		verbose = True

		now = datetime.datetime.now()		
		log_line = "["+now.strftime("%H:%M:%S")+"] \""+request_type+" "+request_path+"\" (host: "+self.headers.get('Host')+")"

		request_headers = self.headers
		if verbose:
			printlog("----- Incoming "+request_type+" request ["+str(request_count)+"] ----->\n")
			printlog(str(log_line))
			printlog("")
			printlog(request_path)

			printlog(str(request_headers))
			if request_type == "POST":
				printlog(post_contents)

			printlog("<----------------\n")
		else:
			printlog(log_line)

	def process_request(self,request_path,post_request=""):
		#remove get parameters. E.g.: index.php?param1=value1&param2=value2 -> index.php
		request_path_filtered = urlparse.urlparse(urllib.unquote(request_path[1:]))[2]

		regex_URL_listmatch = False
		fixed_URL_listmatch = False
	####--START-- request to predefined URL####
		if (request_path_filtered in fixed_URL_list) and (len(request_path_filtered)>0):
			list_entry_number = 0
			fixed_URL_listmatch = True
			
			for entry in config_data["requests"]:
				if entry["url"] == request_path_filtered:
					break
				else:
					list_entry_number = list_entry_number + 1
			request_config = config_data["requests"][list_entry_number]
			self.get_response_data(request_config,request_path,post_request)
	####--STOP-- request to predefined URL####

	####--START-- request to URL that matches a defined regex#####
		else:
			list_entry_number = 0
			for regex in regex_URL_list:
				if re.match(regex, request_path_filtered):
					regex_URL_listmatch = True
					for entry in config_data["requests"]:
						if entry["url"] == regex:
							break
						else:
							list_entry_number = list_entry_number + 1
					break

			if regex_URL_listmatch: 
				request_config = config_data["requests"][list_entry_number]
				self.get_response_data(request_config,request_path,post_request)
	####--STOP-- request to URL that matches a defined regex#####	

	####--START-- default request#####
		if not regex_URL_listmatch and not fixed_URL_listmatch:
			request_config = config_data["default"]
			self.get_response_data(request_config,request_path,post_request)
	####--STOP-- default request#####
	
	def send_tail_headers(self,contentLength):
		self.send_header("Content-Length",str(contentLength)) 
		self.send_header("Connection", "keep-alive")
		self.end_headers()

	def get_response_data(self,request_config,request_path,post_request):
		response_log = ""
		#headers
		for key in request_config:
			if key.startswith("addHeader"):
				response_log = response_log + "Header: "+request_config[key][0]+":"+request_config[key][1] + " \n"
				self.send_header(request_config[key][0],request_config[key][1]) 
		if not HTTP_oneDotOne_enabled:
			self.end_headers()

		#body (&Content-Length header in case of HTTP 1.1)
		source_type=request_config["sourcetype"]
		if source_type=="data":
			with open(server_data_folder+request_config["source"], 'rb') as f: 
				file_contents = f.read()
				if HTTP_oneDotOne_enabled:
					self.send_tail_headers(len(file_contents))
				self.wfile.write(file_contents)
				try:
					response_log = response_log + file_contents
				except UnicodeDecodeError:
					response_log = response_log + base64.b64encode(file_contents)
		elif source_type=="python":
			script_output = ""
			if (len(post_request) > 0):
				post_request=base64.b64encode(post_request)
				script_output = subprocess.check_output([sys.executable, server_data_folder+request_config["source"], request_path, post_request]).strip()
			else:
				script_output = subprocess.check_output([sys.executable, server_data_folder+request_config["source"], request_path]).strip()
			script_output = base64.b64decode(script_output)
			if HTTP_oneDotOne_enabled:
				self.send_tail_headers(len(script_output))
			self.wfile.write(script_output)
			try:
				response_log = response_log + script_output
			except UnicodeDecodeError:
				response_log = response_log + base64.b64encode(script_output)
		printlog(response_log, True)

	do_PUT = do_POST
	do_DELETE = do_GET

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
	pass

def serve_on_port(port,ssl_enabled):
	server = ThreadingHTTPServer(('',port), RequestHandler)
	if ssl_enabled:
		server.socket = ssl.wrap_socket (server.socket, certfile=bin_folder+'server.pem', server_side=True) 
	server.serve_forever()

def main():
	http_port = 80
	https_port = 443 #ssl_server needs to be enabled
	http_multi_port = [80,8080,448] #multiport needs to be enabled
	https_multi_port = [443,447] #multiport needs to be enabled
	ssl_server = False
	multiport = False

	if ssl_server:
		#generate certificate on Linux: 
		###openssl genrsa -des3 -out server.key 1024
		###openssl req -new -key server.key -out server.csr (must fill in the common name with something (e.g. localhost)
		###openssl x509 -req -days 1024 -in server.csr -signkey server.key -out server.crt
		###cat server.crt server.key > server.pem
		if multiport:
			print('Listening on localhost (SSL): %s' % https_multi_port)
			for configured_port in https_multi_port:
				Thread(target=serve_on_port, args=[configured_port,True]).start()
		else:
			print('Listening on localhost (SSL): %s' % https_port)
			server = HTTPServer(('', https_port), RequestHandler)
			server.socket = ssl.wrap_socket (server.socket, certfile=bin_folder+'server.pem', server_side=True)
			server.serve_forever()
	else:
		if multiport:
			print('Listening on localhost: %s' % http_multi_port)
			for configured_port in http_multi_port:
				Thread(target=serve_on_port, args=[configured_port,False]).start()
		else:
			print('Listening on localhost: %s' % http_port)
			server = HTTPServer(('', http_port), RequestHandler)
			server.serve_forever()
main()