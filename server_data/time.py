import sys
import datetime
import urlparse
import urllib
import base64
#arg0: python file name
#arg1: request file path
#arg2: (optional:) post data

#The script output is passed via the commandline output.
#There is a risk of special characters being interpreted (processed) by the commandline,
#rather than just being passed. For this reason, pass the output in base64 format.
output = ""
now = datetime.datetime.now()
request_path = sys.argv[1][1:]
output = output + "Current path is: "+request_path+". "
parsed = urlparse.urlparse(request_path)
url_arguments = urlparse.parse_qs(parsed.query)
timestring = "Current time is: "+now.strftime("%H:%M:%S")
if "bold" in urlparse.parse_qs(parsed.query):
	if urlparse.parse_qs(parsed.query)['bold'][0] == "true":
		output = output +  "<strong>"+timestring+"</strong>"
	else:
		output = output +  timestring
else:
	output = output +  timestring
print base64.b64encode(output)