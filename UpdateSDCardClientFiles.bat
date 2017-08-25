::clear old files
rmdir /s /q "C:\Users\SmartWebProgrammer\Desktop\FirmwarePacker\SD-card\WEB"

::copy new files
xcopy /S /E "C:\development\teplomonitor-server\server" "C:\Users\SmartWebProgrammer\Desktop\FirmwarePacker\SD-card\WEB" /I

::convert file names
hashren.exe "C:\Users\SmartWebProgrammer\Desktop\FirmwarePacker\SD-card\WEB"
