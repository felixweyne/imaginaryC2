import base64
import os
import sys
from os.path import dirname, abspath
import struct, binascii,hashlib
from decryptbeacon import serpent_cbc_decrypt

################################
state_file_mappping = {
	0: "46f4f6d16c277b01926c731be2dc2881d00e49ef",
	1: "a93fe153399477c1cfb00dc4ebcfb0a863623620",
	2: "5345284d1071d0141c9d700e75a8abd41702fe17",
	3: "0856a03d6e14471eb88bc5de0d7e91a858ab6985",
	4: "f0a3396abe48545d6bf0f973cb0a2c56c2c3d4b9",
	5: "67326636c4e9f9875136da9455ca43b2b65a678f",
	6: "b21ebc2e521bd63cc63fc3ec81c8c93618c6f157",
	7: "6246ed828432911d04140ea6d8f5313ae7530c7e",
	8: "30a4542ffbd8bed30f5451fb25c79f65f544f70a",
	9: "59eb4d92743a58d2adbfde25fa4aa797db93dfda",
	10: "",
	11: ""
}
################################

script_directory=dirname(abspath(__file__))
state_file=script_directory+"\\state.txt"

	
def print_file_contents(fileName):
	fileContents=""
	with open(script_directory+"\\"+fileName, mode='rb') as file:
		print base64.b64encode(file.read())

is_windows_ten=True

if len(sys.argv) > 2 or is_windows_ten:
	#for some reason, Gozi V3 doesn't always send POST requests on Windows 10?
	if not is_windows_ten:
		#Content-Disposition: form-data; name="ufwstqt"
		#...
		#--57877131fe284542--

		debugDesktop = open(os.path.join(os.environ["HOMEPATH"], "Desktop")+'\gozi_request_log.txt', 'ab')
		postReq = base64.b64decode(sys.argv[2])
		postReq = postReq.split('\n')
		postReq = postReq[3]
		
		path_to_decrypt = postReq.replace('/', '')
		path_to_decrypt = path_to_decrypt.replace('_2F', '/')
		path_to_decrypt = path_to_decrypt.replace('_2B', '+')
		path_to_decrypt = path_to_decrypt.replace('_0A', '\n')
		path_to_decrypt = path_to_decrypt.replace('_0D', '\r')
		path_to_decrypt +="=="
		

		debugDesktop.write("Encoded gozi: "+path_to_decrypt+"\n")

		bytes_encoded = base64.b64decode(path_to_decrypt)
		decoded = serpent_cbc_decrypt("30YnVhwn0RuYgeCd", bytes_encoded)

		debugDesktop.write("Decoded gozi: "+decoded+"\n")

	state=0
	if os.path.isfile(state_file):
		with open(state_file) as file:
			state=int(file.readline())

	print_file_contents(state_file_mappping.get(state))

	with open(state_file, "w") as file:
		file.write(str(state+1))
else:
	print base64.b64encode("fail!")