import base64
import os
from os.path import dirname, abspath

################################
state_file_mappping = {
	0: "48e79c2413bd1090c3e99bce786bc4b33f0f632d", #download instruction??
	1: "dfef1067c4c404be770adbfc4c7c23204b69d3bb", #encrypted Dridex payload
	2: "0f6ed930dfae0b4f093a01cd1838b29756c9aa0c", #ping response??
	3: "0f6ed930dfae0b4f093a01cd1838b29756c9aa0c"  #ping response??
}
################################

script_directory=dirname(abspath(__file__))
state_file=script_directory+"\\state.txt"

def print_file_contents(fileName):
	fileContents=""
	with open(script_directory+"\\"+fileName, mode='rb') as file:
		print base64.b64encode(file.read())

state=0
if os.path.isfile(state_file):
	with open(state_file) as file:
		state=int(file.readline())

print_file_contents(state_file_mappping.get(state))

with open(state_file, "w") as file:
	file.write(str(state+1))