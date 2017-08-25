import sys
sys.path.insert(0, "C:\Users\dmitry\Desktop\FirmwarePacker\scripts")
from SmartWeb_PushFirmwareToServer_Disco import do
#################################################
#################################################
firmwareDestPath="Z:/firmware/SmartWeb Disco debug"
production = False
#################################################
#################################################
do(firmwareDestPath, production)