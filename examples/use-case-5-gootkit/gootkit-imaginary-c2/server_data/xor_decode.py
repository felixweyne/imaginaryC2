import os
import base64

dir_path = os.path.dirname(os.path.realpath(__file__))

xor_encoded = bytearray(open(dir_path+"\\c9ba13a1ff99764e755ddd85523e18faed342dbc", 'rb').read())
size = len(xor_encoded)
xord_byte_array = bytearray(size)
 
for i in range(size):
	xord_byte_array[i] = xor_encoded[i] ^ 0xFE
 
print base64.b64encode(xord_byte_array)