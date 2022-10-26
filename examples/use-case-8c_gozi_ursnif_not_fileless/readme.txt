This use case aims to partially simulate the server side of Gozi/Ursnif. 
This usecase is a variant of this usecase: https://github.com/felixweyne/imaginaryC2/tree/master/examples/use-case-8-gozi_ursnif

**Not sure on the common name used for this Gozi flavour, but this might be named 'GoziAT' by Checkpoint and others?**

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the hosting of the responses to the Gozi loader. These responses contain the Gozi payload. More about this can be read on these resources:
https://github.com/felixweyne/imaginaryC2/tree/master/examples/use-case-8-gozi_ursnif
https://app.any.run/tasks/debba356-df73-46c1-8b84-f8c5c1881424/

This usecase has been added for "museum cataloguing" purposes, after seeing great recent Gozi writeups :-):
https://www.mandiant.com/resources/blog/rm3-ldr4-ursnif-banking-fraud
https://medium.com/csis-techblog/chapter-1-from-gozi-to-isfb-the-history-of-a-mythical-malware-family-82e592577fef
https://research.checkpoint.com/2020/gozi-the-malware-with-a-thousand-faces/


Use Case prerequisites 
-----------------------
*This use case should be used in conjunction with the following Gozi sample:
	SHA1: b4b3455b1960413460bd401156c1f166d3ae5632
*This use case could optionally be used in conjunction with the following unpacked Gozi/Ursnif sample:
	SHA1: add07960e8f808c7da6fe0be6ab9fbb939dda0e9
*(Note that the above mentioned samples can be found inside the archive 'examples/use-case-samples.zip'. The archive password is: 'infected').
*This use case has been tested in a windows 10, 64-bit virtual machine, with python 2.7 installed.

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Ensure you run this on a PC that (still has) Internet Explorer. Gozi uses this browser for C2 communication.
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*Configure Imaginary C2 to use a timeout. In some of my test runs it seemed like the interaction between the simple HTTP server and Internet Explorer (used by Gozi for the C2
 communication) resulted in a connection which never got closed. To add a timeout, look for the following line inside "bin/imaginary_c2.py":
	"class RequestHandler(BaseHTTPRequestHandler):" 
 add the following line (without quotes) right below the RequestHandler class:
	timeout = 2
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run Gozi/Ursnif (SHA1 above). It could take some time before you see connections appearing in the Imaginary C2 console window.
