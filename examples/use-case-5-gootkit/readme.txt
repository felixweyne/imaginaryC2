This use case aims to partially simulate the server side of GootKit. 

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the hosting of the encrypted (nodeJS) Gootkit module.

Upon execution, Gootkit spawns a subprocess of itself (the subprocess contains the "--vwxyz" parameter). It then performs a request to the following URL structure:
https://c2-server.com/rbody320 
After this request, Gootkit downloads an encrypted module from the following URL structure:
https://c2-server.com/rbody32
At a fixed time interval, Gootkit checks for updates (or freshly packed variant of itself) on the following URL structure:
https://c2-server.com/rpersist4/*number*

The above behavior is documented well in the following articles:
from Kaspersky: https://securelist.com/inside-the-gootkit-cc-server/76433/
from Vitali Kremez: https://www.vkremez.com/2018/04/lets-learn-in-depth-dive-into-gootkit.html
from Certego: https://www.certego.net/en/news/malware-tales-gootkit/

This use case will give the expected C2 responses such that Gootkit will download and load the module. 
Additionally, the C2 simulation will respond with an update for the Gootkit exe when it is requested.

Use Case prerequisites 
-----------------------
*This use case should be used in conjunction with the following Gootkit sample.
	MD5: d1d809c1f831ed8e639102193482183d 
	SHA1: d5f2adb7f09b9377060b93077467766968b207e3
	SHA256: 5c2a4a97cc1b1aeb050b53697a058263864d2809da618e00f93f33d36612d46e
*Optionally, the unpacked version of the above sample can be used (in combination with a debugger):
	MD5: 21742a51187200f03e45f49eadddbec6 
	SHA1: f846284f085fdde164ecaa08ff38a7bf9f0f84b3
	SHA256: b4454dbfc0003f81e623ecdd7ecc8f6ca28a535f5aea8056704f3d05a3113a54
*This use case has been tested in a windows 7 SP1, 64-bit virtual machine, with python 2.7 installed.
*(Set the system clock to July 2019 for optimal results).

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder.
 Note that the response to 'rpersist4' (Gootkit update) is an unencrypted exe. 
 I have XOR-ed this EXE to be safe. The intermediate 'xor_decode.py' script is thus not necessary if you replay the original, non-XORed response.
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*Configure Imaginary C2 to use SSL, HTTP 1.1 and listen to ports 80 and 443. You can do this by editing the following lines in imaginary_c2.py:
	HTTP_oneDotOne_enabled=True
	https_multi_port = [80,443]
	ssl_server = True
	multiport = True
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run Gootkit (SHA1 above). You should see connections appearing in the imaginary C2's commmandline window.
*If all works correctly, you will see an additional DLL being mapped in the address space of the Gootkit process.