This use case aims to partially simulate the server side of Dridex. 

!!!This simulation involves running malware. Only do this in a sandbox environment and if you know what you are doing!!!

Use Case description
---------------------
Imaginary C2 can be used to simulate the hosting of the encrypted Dridex V4 payload module.

Upon execution, DridexLoader fingerprints the system (machine id, installed programs, etc.) and sends this information to the C2.
Based on this fingerprint, the C2 decides if the requesting machine is an 'interesting machine' to infect (e.g. doesn't contain obvious 
analysis tools). Additionally, a payload is only send when the requests happens within a short time window of a new spam campaign. 

If the requesting machine is deemed 'an interesting' machine, the C2 provides the Dridex loader with the Dridex payload. The Dridex payload
will be injected into explorer. The Dridex payload (DLL) will be saved on disk in conjunction with a copy of a legitimate windows binary.
This behavior is documented well in a report by Panda Security: https://www.pandasecurity.com/mediacenter/pandalabs/dridex_version_4/

Use Case prerequisites 
-----------------------
*This use case *could* be used in conjunction with the following DridexLoader sample.
 This is the original spammed Dridex sample. This is the packed Dridex Loader and will sleep for a few minutes before it starts its evil. 
	MD5: 53b4636562f66648184e0c871bc4f4ed 
	SHA1: 766fc1c76018df0ab19b13a545356dd505a8585d
	SHA256: 135b84d148c481ec5284c79c20011125fe3fc1df311f1e30861e0b014893aec4
*This use case *should* be used in conjunction with the following 'nosleep' DridexLoader sample. This is the unpacked 
 spammed DridexLoader sample, which I have patched such that the long sleep-loop is skipped ( saves you time :-) ).
	MD5: 8714fcaad97d781bd5234b087853b61e 
	SHA1: ec6633b54e8eed8c67bd2fcba1addf56b44d876a
	SHA256: 9c3994c5ee5ce6bd94a17e66b7a88714d566ee99381b83d13ff1037654a780b5
*The imaginary C2 response provides a 64-bit DLL and the DridexLoader sample should thus be run on a 64-bit machine.
*This use case has been tested in a windows 7 SP1, 64-bit virtual machine, with python 2.7 installed.
*(Set the system clock to June 2019 for optimal results).

How to run
----------
*Ensure you are in a sandbox environment (e.g. virtual throwaway machine) and have python 2.7 installed
*Copy the redirect_config.txt and requests_config.txt to imaginary C2's folder
*Copy the files in server_data to imaginary C2's server_data folder.
 Note that the DridexLoader sends different requests to the same URI. We can simply replay the original responses 
 in the right order. We just need to keep track on how many times the URI has already been called (see recurring-path.py).
*Run imaginary C2's redirect_to_imaginary_c2.bat file (as administrator)
*Configure Imaginary C2 to use SSL and HTTP 1.1. You can do this by editing the following lines in imaginary_c2.py:
	ssl_server = True
	HTTP_oneDotOne_enabled=True
*Run imaginary C2's launch_imaginary_c2_server.bat
*Run DridexLoader (SHA1 above). You should see connections appearing in the imaginary C2's commmandline window.
*If all works correctly, you will see explorer writing a DLL and EXE file in a subfolder of the windows folder.
 An example screen capture of this simulation can be found in: media/imaginary_c2_dridex_simulation.mp4