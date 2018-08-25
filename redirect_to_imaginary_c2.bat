@echo off
echo ze658f4z >> c:/ESPOFIJ.txt
if not exist c:/ESPOFIJ.txt goto noAdminPermission
del /q "c:/ESPOFIJ.txt"
python "%~dp0\bin\redirect_to_imaginary_c2.py"
goto end
:noAdminPermission
cls
color 4F
echo No permission. Please click with your right mouse button
echo on this program and select RUN AS ADMINISTRATOR
:end
pause
exit