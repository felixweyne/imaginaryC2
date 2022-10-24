import base64
import os
from os.path import dirname, abspath

################################
state_file_mappping = {
	0: "1f38d7b1b8b30031d8ba15c2bf2efed1586f8e0e", 
	1: "ddb5c02fc62defdc3efede27281b599e4443cdee", 
	2: "756d2110ba27edceeacd2fa4f8b33cafbfb4b44a" 
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