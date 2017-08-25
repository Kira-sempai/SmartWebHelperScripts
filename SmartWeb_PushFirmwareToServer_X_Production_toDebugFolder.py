import sys
sys.path.insert(0, "C:\Users\dmitry\Desktop\FirmwarePacker\scripts")
from SmartWeb_PushFirmwareToServer_X import do

#################################################
#################################################
firmwareDestPath="Z:/firmware/SmartWeb X debug"
production = 1
#################################################
#################################################
do(firmwareDestPath, production)