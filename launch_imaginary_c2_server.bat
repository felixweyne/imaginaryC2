@echo off
echo Launching imaginary C2 HTTP server
WMIC path win32_process get Commandline | find "python" | find "imaginary_c2" >NUL
echo.
if "%ERRORLEVEL%"=="0" goto skip
echo Go to http(s)://localhost in your browser
echo.
python "%~dp0\bin\imaginary_c2.py"
goto end
:skip
color 4F
echo imaginary C2 HTTP server is already running!
:end
pause