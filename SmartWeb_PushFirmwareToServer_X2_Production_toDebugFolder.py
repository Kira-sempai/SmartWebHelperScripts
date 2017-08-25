import sys

sys.path.insert(0, "C:\Users\dmitry\Desktop\FirmwarePacker\scripts")
import SmartWeb_PushFirmwareToServer_X

#################################################
#################################################
firmwareDestPath = "Z:/firmware/SmartWeb X2 debug"
projectName      = 'xhcc_s62'
production       = True
deviceName       = 'XHCC-S62'
board            = 'S62'
boardVariant     = '2'
#################################################
#################################################

SmartWeb_PushFirmwareToServer_X.do(firmwareDestPath, projectName, production, deviceName, board, boardVariant)