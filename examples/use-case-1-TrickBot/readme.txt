This use case aims to (partially) simulate the server side of TrickBot. 

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the hosting of TrickBot components and configuration files. Additionally, it can also be used to simulate the TrickBot web injection servers.

Upon execution, the TrickBot downloader connects to a set of hardcoded IPs to fetch a few configuration files. One of these configuration files contains the locations (IP addresses) 
of the TrickBot plugin servers (image one). The Trickbot downloader downloads and decrypts the plugins (modules) from these servers. The decrypted modules are injected into a svchost.exe instance. 

One of TrickBot's plugins is called "injectdll", a plugin which is responsible for TrickBot's webinjects. The "injectdll" regularly fetches an updated set of webinject configurations. For 
each targeted (banking) website in the configuration, the address of a "webfake server" is defined. When a victim browses to a (banking) website which is targeted by TrickBot, his browser 
gets redirected to the "webfake server", upon which he sees the web content defined by the attacker. 

Use Case prerequisites 
-----------------------

*This use case should be used in conjunction with the following TrickBot downloader:
	MD5: 4cb551de1658cc49235d73aa77bbe0ab 
	SHA1: 4389a7444599af894d2629ba1ef71908f0720f13
	SHA256: e04727ff07787c3447844dcd9a489faaf2f0dfe2fc33133a2977f16c5aed265f
*This use case could optionally be used in conjunction with the following unpacked TrickBot loader:
	MD5: dcd52decc37856c622e6c29bc8558f8e
	SHA1: 4dc5a4f59cda50c7185eb907439b678ef3185ebe
	SHA256: 58ca66e46dfb32ce91fce7b22e9e1a0e5543b8fde0add84dd1b61e117067cdec
*(Note that the above mentioned samples can be found inside the archive 'examples/use-case-samples.zip'. The archive password is: 'infected').
*The Trickbot downloader must run in a 64-bit sandbox as 32-bit module downloads are not simulated. 
*The virtual machine must be connected to the internet (TrickBot performs an HTTP request to retrieve the machine's public IP address).
 If you don't want to connect to the internet, you can simulate the HTTP response containing a fake IP easily with imaginary C2.
*(Set the system clock to July 2018 for optimal results). 
*This use case has been tested in a windows 7 SP1, 64-bit virtual machine, with python 2.7 installed.

Use Case contents
------------------
All files are extracted from the following network capture: trickbot.saz (Fiddler Session Archive). 

There are 32 IPs defined in the redirect configuration. These IP's correspond to hosting locations of:
-TrickBot's configfile server
-TrickBot's plugin server
-TrickBot's webinject (web fake) server

There are 8 requests defined in the request configuration. These requests are:
-encrypted TrickBot configuration files (location of pluginservers, webinjects, ...)
-encrypted modules (systeminfo and injectddl)

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder
*Configure Imaginary C2 to listen on ports 443,447,449 on SSL. You can do this by editing the following lines in imaginary_c2.py:
	https_multi_port = [443,447,449]
	ssl_server = True
	multiport = True
*Set system date to 11/20/2018
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run Trickbot downloader (SHA1 above). You should see connections appearing in the imaginary C2's commmandline window. (note: the first connection is to a public IP lookup service, all the other connections should be redirected to imaginary C2).
*Visit a website defined in the TrickBot static webinject configuration. (You can use trick_config_decoder.py created by hasherezade on the file: sinj.d197a72f43414697a3754caeaae814ca894da31e to find out which sites Trickbot targets)
*If all works correctly, TrickBot will redirect you to imaginary C2
