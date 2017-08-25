
::clear old files
rmdir /s /q "data_files\WEB"
rmdir /s /q "data_files\GUI"
del install_files\*.bin
del data_files\langs.sd

::copy new files
xcopy /S /E "C:\development\xhcc\web\teplomonitor-server\server" "data_files\WEB" /I
xcopy /S /E "C:\development\xhcc\sdcard\Disco\GUI" "data_files\GUI" /I
copy /v /y C:\development\xhcc\build\disco\device1\shared\platform\stm32\DISCO-Sorel-32F746GDISCOVERYv1r1-STM32-west-sdcard.bin    install_files\firmware.bin
copy /v /y C:\development\xhcc\build\disco\device1\shared\platform\stm32\langs.sd                                    data_files\langs.sd
copy /v /y C:\development\xhcc\web\teplomonitor-server\sitemenu.txt                                                 data_files\sitemenu.txt

SET dlparams=C:\development\xhcc\build\disco\device1\shared\platform\stm32\dlparams.sd
if exist %dlparams% (
	copy /v /y %dlparams% data_files\dlparams.sd
)

::convert file names
hashren.exe "data_files\WEB"
hashren.exe "data_files\GUI"

::pack firmware in several ways
DLPack install_files null			archive\DISCO_FW.bin
DLPack data_files null				archive\DISCO_SD.bin
DLPack install_files data_files		archive\DISCO_FW_SD.bin

::pack bootloader separatly from the main project firmware
del install_files\*.bin
copy /v /y C:\development\xhcc\build\disco\loader\shared\platform\stm32\loader-Sorel-32F746GDISCOVERYv1r1-STM32-sdcard.bin  install_files\bootldr.bin
DLPack install_files null			archive/DISCO_BL.bin