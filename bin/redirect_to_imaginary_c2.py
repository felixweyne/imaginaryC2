__author__ = "Felix Weyne, 2017"

#The goal of this script is to create redirections to the localhost.
#Domains are redirected by altering the hosts file. IPs are redirected by using the netsh command. 

#NOTE: only use this in a sandbox (throwaway Virtual Machine), as this script will alter network settings!

import os
from os.path import dirname, abspath
import subprocess 

def validip(ip):
	return ip.count('.') == 3 and  all(0<=int(num)<256 for num in ip.rstrip().split('.'))

iplist = []
domainlist = []

directory_one_up = dirname(dirname(abspath(__file__)))	
with open(directory_one_up+'\\redirect_config.txt') as file:
	for line in file:
		#print line
		cleaned = line.strip().split("#")
		if len(cleaned[0])>3:
			config_line = cleaned[0].strip()
			if validip(config_line):
				iplist.append(config_line)
			else:
				domainlist.append(config_line)

#netsh int ip sh int << look for loopback interface

for ip in iplist:
	print "Routing IP to local loopback adapter: "+ip
	#revert change: netsh int ip delete addr 1 *ip*
	subprocess.call("netsh int ip add addr 1 "+ip+"/32 st=ac sk=tr", shell=True)

print ""
print "----"
print ""

host_file_folder = "C:\\Windows\\System32\\drivers\\etc\\"
host_file = host_file_folder +"hosts"

if os.path.isfile(host_file):
	if not os.path.isfile(host_file_folder+"hosts.backup"):
		os.rename(host_file,host_file_folder+"hosts.backup")
	else:
		os.remove(host_file)
file = open(host_file, 'a+')
for domain in domainlist:
	print "Adding domain to hosts file: "+domain
	file.write("127.0.0.1    "+domain+"\r\n")
file.close()