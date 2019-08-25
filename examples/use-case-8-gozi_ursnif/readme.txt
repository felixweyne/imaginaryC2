This use case aims to partially simulate the server side of Gozi/Ursnif. 

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the hosting of the encrypted Gozi DLLs, as well as the encrypted Gozi (injection) Powershell script.

The source of Gozi's C2 communication was found by a submission in the Any.Run sandbox: 
https://app.any.run/tasks/4af2c7d6-bab0-4ad4-9b3d-e2dc721753f2/

Gozi will contact legitimate domains upon execution (e.g. microsoft.com, avast.com), presumably in an effort to mislead analysts. 
It will perform this communication by making use of the Internet Explorer COM API, which will result in the launch of a new Internet Explorer instance.

After having generated decoy network traffic, Gozi will contact its C2 servers. This C2 behavior is documented well in the following blog from the Twitter user @0verfl0w_ :
https://0ffset.net/reverse-engineering/malware-analysis/analyzing-isfb-second-loader/. The information below is based on/cited from the writeup. An additional good background
reading on Gozi is the paper of M. Kotowicz, called: ISFB, Still Live and Kicking. 

Gozi will generate the following parameterized string for its communication to the C2 server:
	soft=[parameter1]&version=[parameter2]&user=%[parameter3]&server=[parameter4]&id=[parameter5]&crc=[parameter6]&uptime=[parameter7]

The string gets encrypted and encoded using Serpent CBC encryption and Base64 Encoding. Before doing so, a random string is prepended to the string so that there are no similarities in the data sent to different C2's.
To finalize the string before sending, the loader cleans it up a bit, removing values such as + and / and replacing them with _2B and _2F respectively. The equal signs are also removed. Finally, using the random value generator,
it adds slashes to the string in random places, before prepending '/images/' and appending '.avi'.

Below I have added the C2 URLs which were observed during a sample detonation in the Any.run sandbox. The encrypted data in the URL can be decrypted with the help of a tool published by Twitter user @matte_lodi : 
https://github.com/mlodic/ursnif_beacon_decryptor/. The data was encrypted with the following key: '10291029JSJUYNHG'.


URL1: xxxp://cdevinoucathrine[.]info/images/0yOLLn84H348X3R/pjaYrTYJc2fgcqqasS/sWT2yshBs/3rKD5LtrCBgFBNUPoG8y/isGlOl91EiyYYcRm_2F/xNWDGqOLy5_2FaMUuacsY8/Ndo27QMwaF_2B/AN5_2BBY/ouyNA_2FMgISNZVFitS14ze/0lUQVGQfJ2D/eJ.avi
	Decrypted data: ixyccvi=pdahs&soft=3&version=214082&user=dddf642e383b6c7bf19c4b2e52065d40&server=12&id=3386&crc=1&uptime=1530

URL2: xxxp://cdevinoucathrine[.]info/images/KCdujp248/LuXlq_2FnK82HO_2FWiL/gnwvdFkOuWz29SaiXqm/1_2Fu_2BnV1BjW0te6lLKR/75OQZ99IEfX5d/rZ5WEZZu/xAP3IYrZin0JGkmgh_2BDwp/b7qNJztq0D/fhAGPs848b0Zedgef/b11t9smmd0fo/87pq5tTBJOI/GKaoMpvb/muVn_2F82/lr.avi
	Decrypted data: svkicufnk=uphviarr&soft=3&version=214082&user=dddf642e383b6c7bf19c4b2e52065d40&server=12&id=3386&crc=2&uptime=1534

URL3: xxxp://cdevinoucathrine[.]info/images/72zWD5_2BxaBfow3y8/TnJtFQEVh/kU9_2Bs9hiIRtoRmoil3/m_2BUr11tKjHSOo7tip/U2iiLruEdzwOuTdygongk2/f5Kkea1yqFK81/N8WUfuI3/lVXDZLd_2Bh8MUWS1t9bGfO/I6SeQCJc1S/lBTXusqdy/Vdk4h_2B/U.avi
	Decrypted data: upodwl=hxaexd&soft=3&version=214082&user=dddf642e383b6c7bf19c4b2e52065d40&server=12&id=3386&crc=3&uptime=1537

All responses to those URL requests are base64 encoded. The first two URL requests (crc=1 & crc=2) are requests for the 32 and 64-bit DLLs which will be injected into explorer.
The third URL request (crc=3) contains the Powershell script which will be a part of the further execution chain. The response data will be stored in the following registry path:
	HKCU\Software\AppDataLow\Software\Microsoft\*random value*\

Use Case prerequisites 
-----------------------
*This use case should be used in conjunction with the following Gozi sample:
	MD5: 0dd4c46135076dd61d82abfd5cf70c51 
	SHA1: a3a5af1a73dacf702135f973b3ddda6fb03c8af9
	SHA256: c24767680d43627c124fa63f425e8a94ca54455318bd8b1c40897146e81b1c2a
*This use case could optionally be used in conjunction with the following unpacked Gozi/Ursnif sample:
	MD5: 384e23da881a675280ca46a123bca41b 
	SHA1: 3ca99d6877ce78a663844e6ca57fffe1125bc637
	SHA256: ca5063e4b887293007bb160acbdf8622c6ec95a68f559438a9f47f1f23304103
*This use case has been tested in a windows 7 SP1, 64-bit virtual machine, with python 2.7 installed.
*(Set the system clock to 25th July, 2019 for optimal results).

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder
 Note that we don't need to decrypt the GET requests. It seems like the three (encrypted) modules described above are always fetched in the same order.
 We can thus replay the traffic in the right order, we just need to keep track on how many times the 'images'-URI has already been called (see recurring-path.py).
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*Configure Imaginary C2 to use a timeout. In some of my test runs it seemed like the interaction between the simple HTTP server and Internet Explorer (used by Gozi for the C2
 communication) resulted in a connection which never got closed. To add a timeout, look for the following line inside "bin/imaginary_c2.py":
	"class RequestHandler(BaseHTTPRequestHandler):" 
 add the following line (without quotes) right below the RequestHandler class:
	timeout = 2
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run Gozi/Ursnif (SHA1 above). It could take some time before you see connections appearing in the Imaginary C2 console window (Gozi will first contact legitimate domains).
 You should see at least three incoming connections and registry keys being created on the following path: HKCU\Software\AppDataLow\Software\Microsoft\*random value*\
 