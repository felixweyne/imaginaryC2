This use case aims to partially simulate the server side of SmokeLoader. 

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the hosting of the encrypted Smokeloader modules.

Upon execution, Smokeloader injects itself into explorer via the PROPagate injection technique.
This behavior is documented well in an article by CERT PL: https://www.cert.pl/en/news/single/dissecting-smoke-loader/

Code injected into explorer will then check for internet connectivity by connecting to http://www.msftncsi.com/ncsi.txt.
The code will then continue by reaching out to the C2 to obtain modules. 
If successful, the C2 will respond with encrypted data which will result in Smokeloader spawning additional explorer.exe instances.

Use Case prerequisites 
-----------------------
*This use case should be used in conjunction with the following SmokeLoader sample:
	MD5: 89e5261944b2dac47ee050875937196c 
	SHA1: 2f14aecc10e83c18ee999bf3d1efda66e8fc9acf
	SHA256: 7af50bf45ac5d655f108641a4c67f90b5a71bd654dea168ce02817a31b506cd0
*This use case has been tested in a windows 7 SP1, 64-bit virtual machine, with python 2.7 installed.
*(Set the system clock to July 2019 for optimal results).

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*(Optionally: disable your network adapter, no internet connectivity is needed since Imaginary C2 simulates everything)
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run SmokeLoader (SHA1 above). You should see connections appearing in the imaginary C2's commmandline window.
*If all works correctly, you will see a lot of explorer instances being spawned.
 An example screen capture of this simulation can be found in: media/imaginary_c2_smokeloader_simulation.mp4