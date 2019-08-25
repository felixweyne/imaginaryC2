import base64
import os
from os.path import dirname, abspath

################################
state_file_mappping = {
	0: "a9a3ecc1a33dad7eab2cd765a61fb9e1f4316a53_decoded",
	1: "458faaff4aa709014812a83f4e26a14cebd41609_decoded",
	2: "b65b04239c32642c2cea14f297a56cc9648e81a2"
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