__author__ = "Felix Weyne, 2017"

#This script's purpose is to examine and process HTTP traffic inside packet captures (pcap files)
#This script 'converts' a packet capture into request definitions which can be parsed by imaginary C2.

#This script requires the commandline wireshark (tshark) to be installed (installed by the wireshark installer)
#Please note that the extracted contents will be extracted byte-by-byte as they appeared in the packet capture. No transformations will be performed:
#If the HTTP response had e.g. chuncked transfer-encoding and GZIP content-encoding, then the extracted response will also be GZIP-encoded with chunked transfer-encoding.

#Via this script, the user can:
#	A) Generate an overview of HTTP request URLs with the corresponding stream numbers (as captured by the pcap).
#	B) Export a stream. Exporting a stream will result in:
#		-The associated HTTP response body written to a file (filename = SHA1 hash of response body)
#		-The HTTP request domain written to the redirection configuration file
#		-The HTTP request URL path written to the request configuration file

import subprocess
import os
import sys
import re
import urlparse
import urllib
import datetime
import hashlib
import json
import binascii
import http_decompress

tshark_location = "C:\\Program Files\\Wireshark\\tshark.exe"
debug = False

#parse PCAP with commandline wireshark for HTTP requests
#1. Filter PCAP on presence of HTTP requests
#2. Select frame number, TCP stream number, HTTP host and HTTP URI as fields
#3. HTTP host and HTTP URI values will be used for the redirect_config and request_config
#	TCP stream number and frame number will be used to extract the HTTP response
#4. A TCP stream may contain multiple HTTP request/response pairs. For each response in a TCP stream, we need to keep track of its position (order) inside the TCP stream
pcap_file_path = sys.argv[1]
tshark_argument_pcap_location = "-r \"" + pcap_file_path + "\""
tshark_argument_fields = "-T fields -e frame.number -e tcp.stream -e http.host -e http.request.uri"
tshark_argument_filter = "-Y \"http.request\""
tshark_command = "\""+tshark_location+"\" "+tshark_argument_pcap_location+" "+tshark_argument_fields+ " "+tshark_argument_filter

if not(os.path.isfile(tshark_location)):
	print "Can not find the commandline Wireshark executable. Ensure the path in the script is configured correctly."
	sys.exit(-1)
if not(os.path.isfile(pcap_file_path)):
	print "Can not find the packet capture file. Please supply a correct path to the packet capture as an argument."
	sys.exit(-1)


tshark_output = ""
try:
	if debug:
		print "## Launching cmdline: "+tshark_command
	tshark_output = subprocess.check_output(tshark_command, shell=False)
	if debug:
		print "## Tshark returned:"
		print tshark_output
except subprocess.CalledProcessError as exc:
	print "Error while parsing PCAP:" +exc
	sys.exit(-1)
tshark_column_index = 1
temp_stream_number = ""
temp_url = ""
temp_hostname = ""
temp_framenumber = ""

http_urls = []
stream_dict = {}

#tshark output should look like:4\t0\t1.2.3.4\t/input.php\r\n11\t1\t1.2.3.4\t/file.pdf
tshark_output_splitted = re.split('\t|\r',tshark_output)
for column in tshark_output_splitted:
	column = column.replace("\n","")
	if debug:
		print "## ("+str(tshark_column_index)+") " + column

	if tshark_column_index == 1:
		temp_framenumber = column
	if tshark_column_index == 2:
		temp_stream_number = column
		#if TCP stream contains multiple HTTP responses, we need to keep track of the order of the HTTP response inside the TCP stream
		if temp_stream_number in stream_dict:
			existing_list_for_stream_number = stream_dict[temp_stream_number]
			existing_list_for_stream_number.append(temp_framenumber)
			stream_dict[temp_stream_number] = existing_list_for_stream_number
		else:
			stream_dict[temp_stream_number] = [temp_framenumber]
	elif tshark_column_index == 3:
		temp_hostname =  column
	elif tshark_column_index == 4:
		temp_url =  column
		http_urls.append([temp_framenumber,temp_stream_number,temp_hostname,temp_url])
		tshark_column_index = 1
		continue
	tshark_column_index += 1

if debug:
	print ""
	print "## List(tcpstream_nr,frame_nr):"
	print "## " + str(stream_dict)
	print ""
	
	temp_counter=0
	print "##(frame_nr,stream_nr,hostname,URL):"
	for entry in http_urls:
		print "## (" + str(temp_counter) + ") " + str(entry)
		temp_counter += 1
	print ""

entry_count = 0
for entry in http_urls:
	print str(entry_count)+": http://"+entry[2]+entry[3]
	entry_count += 1

#function to extract contents of HTTP response inside a TCP stream
def extract_responses_from_tcp_stream(tcpStreamNumber):
	tshark_argument_tcp_stream = "-q -z \"follow,tcp,raw,"+str(tcpStreamNumber)+"\""
	tshark_command = "\""+tshark_location+"\" "+tshark_argument_pcap_location+" "+tshark_argument_tcp_stream

	if debug:
		print "## Calling Tshark: " +tshark_command
	#parse PCAP with commandline wireshark for HTTP requests
	tshark_output = ""
	try:
		tshark_output = subprocess.check_output(tshark_command, shell=False)
	except subprocess.CalledProcessError as exc:
		print "Error while parsing PCAP:" +exc
		sys.exit(-1)
	#print tshark_output
	
	#tshark splits TCP stream output over multiple lines
	tshark_output_splitted = re.split('\r',tshark_output)

	#First and last lines of Tshark output contain general information about the TCP stream. Lines in between contain actual TCP stream contents (hex encoded).  
	#Requests don't contain tabs (client -> server). Tshark appends TAB for responses (server->client).
	temp_tcp_response = ""
	tcp_responses = []
	#Find start of stream output (first occurrence of hexadecimal string)
	start_of_stream_output = 8
	for i in range(0, len(tshark_output_splitted)-1):
		if re.match("\\n[A-Fa-f0-9]{15}", tshark_output_splitted[i]):
			start_of_stream_output = i
			break
	if debug:
		print "## Tshark TCP stream output starts at index: "+str(start_of_stream_output)
		temp_counter=0
		for entry in tshark_output_splitted:
			entry_shortened = entry[0:20].replace("\n","")
			hexadecimal_match = re.search("[A-Fa-f0-9]{4,16}", entry_shortened)
			hexadecimal_decoded = ""
			if hexadecimal_match:
				hexadecimal_decoded = binascii.unhexlify(hexadecimal_match.group(0))
			print "## ("+str(temp_counter)+") "+entry_shortened+"... ("+hexadecimal_decoded+")"
			temp_counter+=1
	for i in range(start_of_stream_output, len(tshark_output_splitted)-1):
		tcp_stream_lines = tshark_output_splitted[i].replace("\n","")
		#check if we are in response area. If so, continue building the response
		if tcp_stream_lines.startswith("\t"):
			temp_tcp_response = temp_tcp_response + tcp_stream_lines.replace("\t","")
		else:
			#we are in request area, stop building the response.
			if len(temp_tcp_response) > 0:
				tcp_responses.append(temp_tcp_response)
			temp_tcp_response = ""
	if debug:
		print ""
		print "## Found: "+str(len(tcp_responses))+" TCP response(s):"
		for entry in tcp_responses:
			print "## length: "+str(len(entry))+". Start: " + entry[0:30] +"..."
		print ""
	return tcp_responses

def select_response(responses, tcpStreamNumber, framenumber):
	if debug:
		print "## Selecting the response for which the request is situated at frame nr: "+framenumber+" and TCP stream nr: "+tcpStreamNumber
	frame_numbers = stream_dict[tcpStreamNumber]
	index=frame_numbers.index(framenumber)
	if debug:
		print "## This corresponds with TCP response nr: "+str(index)
		print ""
	return responses[index]
	
print "\r\n    Enter the number of the stream you want to export."
print "\r\n    Enter 'X' to stop the input"
print "\r\n    Enter 'I' to get an overview of exported resources"

stop_input = False

#create output folder on Desktop
now = datetime.datetime.now()
output_folder = os.path.join(os.environ["HOMEPATH"], "Desktop")+'\\pcap_extract_'+now.strftime("%H_%M_%S") +'\\'
data_folder = output_folder + "server_data\\"
os.makedirs(output_folder)
os.makedirs(data_folder)
with open(data_folder+"default.txt", "a+") as file:
	file.write("Default server response! Hi!")

#Export stream functionality
redirected_domains = []
captured_URLs = []

default_config = "{ \"default\":{ \"source\":\"default.txt\", \"sourcetype\":\"data\"},\"requests\":[ ]}"
requests_config = json.loads(default_config)

exported_streams = {}	
while (stop_input == False):
	#user 'interface'
	my_input = raw_input("\r\n    Export stream:  ")
	if my_input.lower() == 'x':
		print "Stopping output"
		stop_input = True
	elif my_input.lower() == 'i':
		print ""
		for exported_stream in exported_streams:
			exported_stream_overview = ""
			for stream_property in exported_streams[exported_stream]:
				if exported_streams[exported_stream][stream_property] == True:
					exported_stream_overview = exported_stream_overview + " "+stream_property + "[X]"
			print "      *Stream "+exported_stream+": "+exported_stream_overview
	elif re.match("\d", my_input) is None:
		print "      *Your input was not a number, try again"
	elif my_input in exported_streams:
		print "      *Stream has already been exported"
	#extract HTTP response body, domain, URL path
	else:
		try:
			print "      *Exporting " +my_input
			http_request_domain = http_urls[int(my_input)][2]
			if http_request_domain.find(":") != -1:
				http_request_domain, port = http_request_domain.split(':')
			http_request_path = http_urls[int(my_input)][3]
			if http_request_path[:1] == "/":
				http_request_path = http_request_path[1:]
			print "        *domain: "+http_request_domain
			print "        *path: "+http_request_path
			tcp_stream_nr=http_urls[int(my_input)][1]
			if debug:
				print "## Response is inside TCP stream number: "+str(tcp_stream_nr)
			tcp_stream = extract_responses_from_tcp_stream(tcp_stream_nr)
			response_contents = select_response(tcp_stream,http_urls[int(my_input)][1], http_urls[int(my_input)][0])
			response_contents =  binascii.unhexlify(response_contents)
			if debug:
				print "## Start extracted response (headers): "
				print response_contents[0:100]
				print ""
			http_response_body_offset = response_contents.find('\r\n\r\n')
			if http_response_body_offset >= 0:
				stream_properties = {"file":False, "domain":False, "path":False}
				http_headers = response_contents[:http_response_body_offset]
				http_response = response_contents[http_response_body_offset+4:]
				if debug:
					print "## Start extracted response (body): "
					print http_response[0:100]
					print ""
				hash_object = hashlib.sha1(http_response)
				http_response_hex = hash_object.hexdigest()
				http_response_exported_file = data_folder + http_response_hex

				if http_request_path not in captured_URLs:
					if len(http_request_path) > 0: 
						requests_config["requests"].append({"url":http_request_path, "urltype":"fixed", "source":http_response_hex, "sourcetype":"data"})
						captured_URLs.append(http_request_path)
						with open(output_folder+"requests_config.txt", "w") as file:
							file.write(json.dumps(requests_config, indent=2))
						print "        Adding path to JSON request_config"
						stream_properties["path"] = True
					else:
						print "        <>No path found. Use the default response instead."
						continue
				else:
					print "        <>Path already in JSON request_config"
				
				#Support decoding of HTTP response
				#Transfer-Encoding is hop-by-hop (e.g server <-> proxy),
				#while Content-Encoding is end-to-end (e.g. server <-> proxy <-> client).
				
				http_encodings=[]
				if "Transfer-Encoding"  in http_headers:
					encoding_type = re.findall("Transfer-Encoding: ([^\r]{3,20})", http_headers)[0]
					print "        Info: seems like HTTP response is encoded with: "+encoding_type+" (transfer-encoding)"
					http_encodings.append(encoding_type)
				if "Content-Encoding" in http_headers:
					encoding_type = re.findall("Content-Encoding: ([^\r]{3,20})", http_headers)[0]
					print "        Info: seems like HTTP response is encoded with: "+encoding_type+" (content-encoding)"
					http_encodings.append(encoding_type)
				
				http_response_is_chunked=False
				http_response_compression_type=None
				
				if "chunked" in http_encodings:
					http_response_is_chunked=True
				if "gzip" in http_encodings:
					http_response_compression_type = 'gzip'

				if os.path.isfile(http_response_exported_file):
					print "        <>HTTP response already written to: "+http_response_hex
				else:
					print "        Writing HTTP response to: "+http_response_hex
					with  open(http_response_exported_file, "wb") as file:
						file.write(http_response)
						file.close()
					if ((http_response_is_chunked == True) or (http_response_compression_type != None)):
						print "        Encoding detected. Trying to auto decode to: "+http_response_hex+"_decoded"
						try:
							http_response_decoded = ""
							with open(http_response_exported_file, 'rb') as fh:
								http_response_decoded = b''.join(http_decompress.read_body_stream(fh, chunked=http_response_is_chunked, compression=http_response_compression_type))
							with open(http_response_exported_file+"_decoded", "wb") as file:
								file.write(http_response_decoded)
						except Exception as e:
							print "      !!! Decoding failed: "+str(e)
					stream_properties["file"] = True
				if http_request_domain not in redirected_domains:
					print "        Exporting to redirect_config: "+http_request_domain
					with open(output_folder+"redirect_config.txt", "ab") as file:
						file.write(http_request_domain+" #"+http_request_domain+"/"+http_request_path+"\r\n")
					redirected_domains.append(http_request_domain)
					stream_properties["domain"] = True
				else:
					print "        <>Domain already in redirected domains: "+http_request_domain
				exported_streams[my_input] = stream_properties
			else:
				print "Couldn't split HTTP response"
				sys.exit(-1)
		except Exception as e:
			print "      !!! Error: "+str(e)