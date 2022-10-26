This use case aims to partially simulate the server side of Gozi/Ursnif. 
This usecase is a variant of this usecase: https://github.com/felixweyne/imaginaryC2/tree/master/examples/use-case-8-gozi_ursnif

**I believe this Gozi flavour is named Gozi RM3.** 

The last stage unpacked sample (see use-case-samples.zip) has been procuded thanks to the wonderful work here: https://github.com/hasherezade/funky_malware_formats/tree/master/isfb_parser

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the hosting of the responses to the Gozi loader. These responses contain the Gozi payload. More about this can be read on these resources:
https://github.com/felixweyne/imaginaryC2/tree/master/examples/use-case-8-gozi_ursnif
https://news.sophos.com/en-us/2019/12/24/gozi-v3-tracked-by-their-own-stealth/

This usecase has been added for "museum cataloguing" purposes, after seeing great recent Gozi writeups :-):
https://www.mandiant.com/resources/blog/rm3-ldr4-ursnif-banking-fraud
https://medium.com/csis-techblog/chapter-1-from-gozi-to-isfb-the-history-of-a-mythical-malware-family-82e592577fef


Use Case prerequisites 
-----------------------
*This use case should be used in conjunction with the following Gozi sample:
	SHA1: 79bb485824b9b3f365c1722e5ef5bbf0ae4ec677
*This use case could optionally be used in conjunction with the following unpacked Gozi/Ursnif sample:
	SHA1: a4c864076d6f56af1145cc4d36f524a3911c850e
	Since this is a DLL, you need to run it as follows on the commandline: rundll32 a4c864076d6f56af1145cc4d36f524a3911c850e,#2
*(Note that the above mentioned samples can be found inside the archive 'examples/use-case-samples.zip'. The archive password is: 'infected').
*This use case has been tested in a windows 10, 64-bit virtual machine, with python 2.7 installed.

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Ensure you run this on a PC that (still has) Internet Explorer. Gozi uses this browser for C2 communication.
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*Configure Imaginary C2 to use SSL. You can do this by editing the following lines in imaginary_c2.py:
	ssl_server = True
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run Gozi/Ursnif (SHA1 above). It could take some time before you see connections appearing in the Imaginary C2 console window.
