@ECHO OFF
setlocal enabledelayedexpansion
set file="%~1"
if [%1]==[] goto blank
echo %file%
python "%~dp0\bin\unpack_pcap.py" "%~1"
pause
exit
:blank
echo Please drag and drop a PCAP on this batchfile.
pause