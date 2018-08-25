import sys
import datetime
import base64
#arg0: python file name
#arg1: request file path
#arg2: (optional:) post data

#The script output is passed via the commandline output.
#There is a risk of special characters being interpreted (processed) by the commandline,
#rather than just being passed. For this reason, pass the output in base64 format.
now = datetime.datetime.now()
print base64.b64encode("Received post request: "+sys.argv[2]+" on path: "+sys.argv[1])