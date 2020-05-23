import base64
import os
from os.path import dirname, abspath

################################
state_file_mappping = {
	0: "01_87d7c7c51ad37c91a6791dc851f21cf93a82cc50", 
	1: "02_738e0c5096005c09f397a9feba932707e42d1c50", 
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