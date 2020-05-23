This use case aims to partially simulate the server side of Zloader. 

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the hosting of the encrypted Zloader modules and to replay encrypted C2 instructions.

Upon execution, Zloader injects itself into msiexec. It then executes some evasive CPU-intensive junk code before it connects to the C2 server.

The first request to the C2 server is a check-in request, the second request fetches the main bot DLL. The responses are encoded via RC4 and XOR.
These and other C2 requests performed by Zloader are documented really well in a writeup of Twitter user @hasherezade:
https://resources.malwarebytes.com/files/2020/05/The-Silent-Night-Zloader-Zbot_Final.pdf
Another writeup which discusses the C2 communication and modules is the following one of Proofpoint:
https://www.proofpoint.com/us/blog/threat-insight/zloader-loads-again-new-zloader-variant-returns

After having received the main bot (via the response to the second request), the loader transfers execution towards it. The main bot then launches parallel threads to fetch additional modules. The order of these requests can change per execution, I have added the extracted C2 responses for the additional modules in the 'server_data' folder. An overview of their decrypted contents can be found below:

	*2nd request (encrypted: 738e0c5096005c09f397a9feba932707e42d1c50) -> 0631cf33c3c0915934a61f728da86b19f6302115: main bot
	*3th request (encrypted: 06c0ef826d727b5226149b9363ccaeb85e9d6963) -> fb76a718899e5252d2b8ab56bdbbcc033d9c41d8: unknown
	*4th request (encrypted: 3e40be7aded41a0252b40bc531c9ab30f3b27a55) -> b784599c82bb90d5267fd70aaa42acc0c614b5d2: zlib
	*5th request (encrypted: d617ad74dd081912476e0c31e19afc1f14b438b3) -> 4ced2186426da52184a0e3d52c452dc64e0fa110: hiddenVNC 32-bit
	*6th request (encrypted: 94490a892acfe6efbb1e203057fff26458b53fb1) -> 677224e14aac9dd35f367d5eb1704b36e69356b8: SQLite3
	*7th request (encrypted: c7a10cdb3b98c62c0f003d6f6eaca0479eeb03bd) -> c6fb15ff133974eb9fb90a06f5878647ccc43427: webinject config
	*9th request (encrypted: 7d44bd7d83dace54b68f93ef16b7a70173dc9ccf) -> 7d44bd7d83dace54b68f93ef16b7a70173dc9ccf: loader
	*11th request (encrypted: c0b4aafc9ade1afe236c60bdad13868f0996d68a)-> 44199ee158365ce2419c6675deb29805462826ce: libSSL
	*13th request (encrypted: 7b217ac76871ae02284b184f4c34d87651bfb6b6)-> 49b2b6bacab396cae449e6a6d3ca92c73b2da30a: hiddenVNC 64-bit
	*49b2b6bacab396cae449e6a6d3ca92c73b2da30a: hiddenVNC 64-bit

The decrypted modules can be found on Virustotal, the encrypted responses can be found in the 'server_data' folder. 
The communication flow can be found in the packet capture inside the folder 'traffic-capture-Fiddler'. 

![Zloader example](../../media/imaginary_c2_zloader_simulation.png)  

Use Case prerequisites 
-----------------------
*This use case should be used in conjunction with the following Zloader sample:
	MD5: 9d32cc86f7791185dec921fbc7b3be78 
	SHA1: 65764ac0f8cd50d3c0e2d74f789e702a6353c26c
	SHA256: 6576da1f0d0e8c2d7457c2898d0b8d2d7ad40527c60473910f86da6cf39c0951
*This use case could optionally be used in conjunction with the following unpacked Zloader sample:
	MD5: e4a1506fbd5e36db0fbe53bbd4b4087d 
	SHA1: 9b0798319ae62556cb2a943da5a2c3ac3fd34f6d
	SHA256: af3aeeeefdff558bcb79985165efd3b66e883b9efc3d57191618ceaca52f460a
*This use case has been tested in a windows 7 SP1, 64-bit virtual machine, with python 2.7 installed.
*(Set the system clock to 29th April, 2020 for optimal results).

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*(Optionally: disable your network adapter, no internet connectivity is needed since Imaginary C2 simulates everything)
*Configure Imaginary C2 to use SSL. You can do this by editing the following line in imaginary_c2.py:
	ssl_server = True
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run Zloader (SHA1 above). As this file is a DLL file, you can't just double click on it. You can run it via the following cmdline:
    rundl32.exe c:\path_to_dll\zbot.dll,#1
 After running the commandline you should see connections appearing in the imaginary C2's commmandline window.
*If all works correctly, you will see some additional processes being spawned by msiexec (in which the retrieved main module runs). An example spawned process is "net.exe" with the corresponding commandline: "net view /all /domain".
