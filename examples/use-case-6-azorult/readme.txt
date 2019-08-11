This use case aims to simulate the server side of Azorult. 

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------

The behavior of Azorult and its C2 communication is documented well in the following article written by Cylance:
https://threatvector.cylance.com/en_us/home/threat-spotlight-analyzing-azorult-infostealer-malware.html

The source of Azorult's C2 communication was found by a submission in the Any.Run sandbox: 
https://app.any.run/tasks/333bda58-5a37-4543-8492-d3b7d2d85361/

Azorult sends a HTTP (POST) web request to the C2 server upon execution. 
This POST request contains a (uniquely constructed) identifier of the infected machine. 
This identifier is URL encoded and then XOR'ed with the following key: 0x0355AE. 

The response to this request consists of three main parts:
-Azorult's instructions (which data to steal, which additional executable to download and run)
-Legitimate DLLs 
-List of strings used by Azorult

The response is encrypted and for the sake of brevity I will simplify the above response structure in this 'readme' overview. 

The simplified response can be split into two parts:
	*Part one - Start Offset: start of HTTP response. End Offset: start of '</n><d>' string (near the end of the response)
	*Part Two - Start Offset: start of '</n><d>' string. End Offset: end of HTTP response (HTTP response ends in '</d>')

Part one:

Is encrypted with the XOR key 0x0355AE. The decrypted contents look as follows:

	---------------------------------------------------------------------------------
	-+++---+++
	F	Desktop	%USERPROFILE%\Desktop\	*.txt	15	+	-	
	F	Desktop	%USERPROFILE%\Desktop\	*.doc	20	-	-	
	F	Documents	%USERPROFILE%\Documents\	*.txt,*.doc	20	+	-	
	L	xxxp://vh308850[.]eurodir[.]ru/start[.]exe	+	
	I	85[.]203[.]20[.]5:IT
	---------------------------------------------------------------------------------
Note:
F = upload files
L = download and run file
I = IP address and geolocation of infected machine

Part two: 
	data between the '<d>' and '</d>' tags. This data is base64 encoded and contains strings which will be used by the malware.

After having received the above response, Azorult will make a second HTTP request which will contain stolen browser data and exfiltrated files.
This request will be present in the Imaginary C2 log on the Desktop of the infected machine (imaginary_c2_server_log.txt). The request containing the stolen
data can easily be decoded as follows:
	-Scroll inside the Imaginary C2 log until you see the log entry 'Incoming POST request [2]'
	-Scroll past the headers (User-Agent, Host, Content-Length, etc). (Scroll past the last newline characters of the last headerline). 
	 We are now inside the request body.
	-Copy all data past this point into a new file.
	-Open GHCQ's Cyberchef. Insert the 'XOR' recipe. Use '0355AE' as Key (HEX). 
	-Drag and drop the cropped ImaginaryC2 server log (containing the Azorult request body) into the 'Input' box
	-Click on the 'Save to file' button inside the 'Output' box. This file will contain the decoded request.
	 Inside the decoded request you should see stolen browser cookie values, as well as an embedded ZIP file (search for the PK header in hex: '50 4B 03 04')

Use Case prerequisites 
-----------------------
*This use case should be used in conjunction with the following Azorult sample.
	MD5: c91a65a4837ae7b379574942f571d4cd 
	SHA1: 4e77ffa1fbd78badcdd888147c4ebdfb93e0195e
	SHA256: 5d4d21d66d2e7425253b2f3e66862270e2b1a7c802f9b4a3a17fd3e83021dcb0
*This use case has been tested in a windows 7 SP1, 64-bit virtual machine, with python 2.7 installed.
*(Set the system clock to July 2019 for optimal results).

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder.
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run Azorult (SHA1 above). You should see connections appearing in the imaginary C2's commmandline window.
*If all works correctly, you will see two incoming requests. The meaning of these requests have been explained in the previous section.