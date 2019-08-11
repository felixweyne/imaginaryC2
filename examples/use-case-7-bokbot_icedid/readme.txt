This use case aims to partially simulate the server side of Bokbot/IcedID. 

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the hosting of the encrypted Bokbot/IcedID modules, as well as the Bokbot instructions.

Upon execution, Bokbot/IcedID injects itself into svchost. After 5 minutes it creates a series of HTTPS requests to the C2 server.
This behavior is documented well in an article written by Crowdstrike: https://www.crowdstrike.com/blog/digging-into-bokbots-core-module/

An example HTTP request URL looks as follows:
https://c2server/in.php?g=18&c=A2B16A089E65A9462&p=0&r=108&d=0 

The request parameters have the following meaning (source: Crowdstrike article):
g = request type
c = unique botID
p = response type (0 = no response data, 1 = process list)
r = BokBot major version

During my test run, I observed the following HTTP requests. I will briefly explain their meaning based on the information of the Crowdstrike article:

Request to: https://c2server/in.php?g=2&c=425BC8A089E65A9462&p=0&r=108&i=0&n=0&o=0&k=4264&a=2&l=
Request data: username (urlencoded), hostname (urlencoded), windows version information, etc.
Purpose of request:
	g=2 (request type) - general beacon request
	Response contains (numeric) bot instructions. Example:
		0;7;
		0;6;
		0;13;*URL*
		0;13;*URL*
		0;15;
		0;13;*URL*
		0;13;*URL*
		0;8;
		0;1;1
		0;1;4
		0;1;2
		0;1;6

	the second semicolon delimited value contains the instruction type:
		1  - start new executable module, restart current executable module
		6  - Update webinjection configuration DAT file
		7  - Update reporting configuration DAT file
		8  - Update C2 configuration file
		13 - Download and execute an exe file

Request to: https://c2server/in.php?g=18&c=425BC8A089E65A9462&p=0&r=108&d=0 
Purpose of request: 
			 g=18: updating web injection configuration
			 The response is RC4 encoded and the format is well explained in 
			 the Crowdstrike article. The first 8 bytes of the response contains 
			 the prepended RC4 key. This format makes it easy to decode these 
			 responses. 
			 E.g. take the response with hash: e53c43b6c7df23abadb0bbbc273f9f03031f527d
			 (available in the server_data folder). The first 8 bytes in hex are:
			 04 FD 2C 92 DE E7 66 C3. Let's remove those bytes from the start of the file
		     and save the output. With the help of GCHQ's CyberChef we can easily decode the 
			 response. Drag the cropped file to the 'input' box, and choose the following recipes:
			 1) ToBase64
			 2) RC4. Passphrase: 04 FD 2C 92 DE E7 66 C3 (type: hex). Input format: base64.
			 Inside the 'output' box a 'save to file' button is available. Clicking this will enable
			 you to save the decoded file.
			 You will notice the decoded file starts with the following bytes: 7A 65 75 73 DD 2A 0F 00
			 The first four bytes form the word "zeus" (7A 65 75 73). The next four bytes contain the 
			 compressed data length (00 0F 2A DD - little endian) (+- 970KB).
			 If you remove those 8 prepended bytes from the decrypted file and save it to a new file 
			 (e.g. rc4_decoded_cropped), you can easily decompress the file with the following Python code snippet:
				import zlib
				with open("rc4_decoded_cropped", mode='rb') as file:
					print zlib.decompress(file.read(), -15)

Request to: https://c2server/in.php?g=19&c=425BC8A089E65A9462&p=0&r=108&d=0 
Purpose of request: g=19: updating reporting configuration

Request to: https://c2server/in.php?g=20&c=425BC8A089E65A9462&p=0&r=108&d=0 
Purpose of request: g=20: updating C2 server list

Requests to: https://c2server/in.php?g=33&c=425BC8A089E65A9462&p=0&r=108&d=0 
			 https://c2server/in.php?g=34&c=425BC8A089E65A9462&p=0&r=108&d=0 
			 https://c2server/in.php?g=36&c=425BC8A089E65A9462&p=0&r=108&d=0 
			 https://c2server/in.php?g=38&c=425BC8A089E65A9462&p=0&r=108&d=0 
Purpose of requests:
			 Download executable modules.
			 The responses are RC4 encoded. The first 8 bytes of the response 
			 contains the prepended RC4 key. This format makes it easy to decode 
			 these responses.
			 E.g. take the response with hash: 098d59614766d7d90b0a642040e39e4874b8bbf3
			 (available in the server_data folder). The first 8 bytes in hex are:
			 FA DD 46 5C 20 69 57 68. Let's remove those bytes from the start of the file
		     and save the output. With the help of GCHQ's CyberChef we can easily decode the 
			 response. Drag the cropped file to the 'input' box, and choose the following recipes:
			 1) ToBase64
			 2) RC4. Passphrase: FA DD 46 5C 20 69 57 68 (type: hex). Input format: base64.
			 Inside the 'output' box a 'save to file' button is available. Clicking this will enable
			 you to save the decoded file.

Requests to: https://c2server/in.php?g=4&c=425BC8A089E65A9462&p=1&r=108 
Request data: list of running processes
Purpose of request: g=4: process list.

Use Case prerequisites 
-----------------------
*This use case should be used in conjunction with the following Bokbot/IcedID sample:
	MD5: b747dd9e1b8698037569974bcc8fd7c6 
	SHA1: 6c3254c91f11d3f6168663e505edafc0bbba41e3
	SHA256: 5a5808c6c30fed4d884e2a45cc0e8ad277b8879afe789a4587d3a4044bd4fe42
*This use case could optionally be used in conjunction with the following unpacked Bokbot/IcedID sample:
	MD5: 82a2901606d3686040971e8118e4c66a 
	SHA1: 187fa2dd5788586f4d3897cc1d49dca13122470e
	SHA256: 35d058437d7f33481a4502136714f2f3241b4e1386798f6f59f9afc00cc80b5c
*This use case has been tested in a windows 7 SP1, 64-bit virtual machine, with python 2.7 installed.
*(Set the system clock to 1st August, 2019 for optimal results).

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*(Optionally: disable your network adapter, no internet connectivity is needed since Imaginary C2 simulates everything)
*Configure Imaginary C2 to use SSL and prevent it from stripping GET parameters in the request URL.
 Since BokBot sends data via GET parameters (e.g. the 'g' request type parameter), we need to be able to process them.
 You can do this by editing the following lines in imaginary_c2.py:
	1)	ssl_server = True
	2)	look for the following line:
			request_path_filtered = urlparse.urlparse(urllib.unquote(request_path[1:]))[2]
		replace it by the following line:
			request_path_filtered = urllib.unquote(request_path[1:]) #don't filter
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run Bokbot/IcedID (SHA1 above). You should see connections appearing in the imaginary C2's commmandline window.
*If all works correctly, you will see some additional svchost instances being spawned.
 An example screen capture of this simulation can be found in: media/imaginary_c2_bokbot_icedid_simulation.mp4