
::clear old files
rmdir /s /q "data_files\WEB"
del install_files\*.bin

::copy new files
xcopy /S /E "C:\development\xhcc\web\teplomonitor-server\server" "data_files\WEB" /I
copy /v /y C:\development\xhcc\build\DataLogger_production\device\shared\platform\stm32\DL-Sorel-L30vr1-STM32-sdcard.bin     install_files\firmware.bin
copy /v /y C:\development\xhcc\build\DataLogger_production\device\shared\platform\stm32\langs.sd                             data_files\langs.sd
copy /v /y C:\development\xhcc\web\teplomonitor-server\sitemenu.txt                                               data_files\sitemenu.txt

set dlparams=C:\development\xhcc\build\DataLogger_production\device\shared\platform\stm32\dlparams.sd
if exist %dlparams% (
	copy /v /y %dlparams% data_files\dlparams.sd
)

::convert file names
hashren.exe "data_files\WEB"

::pack firmware in several ways
DLPack install_files null			archive\DL_FW.bin
DLPack data_files null				archive\DL_SD.bin
DLPack install_files data_files		archive\DL_FW_SD.bin

::pack bootloader separatly from the main project firmware
del install_files\*.bin
copy /v /y C:\development\xhcc\build\DataLogger_production\loader\shared\platform\stm32\loader-Sorel-L30vr1-STM32-sdcard.bin         install_files\bootldr.bin
DLPack install_files null archive/DL_BL.bin
