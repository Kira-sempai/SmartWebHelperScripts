import os
import shutil
import func

#################################################
#################################################

simulatorDestPath="Z:/simulator/SmartWeb X"

projectName = 'xhcc'
deviceName = 'qtsim2'

baseEnv = dict()
baseEnv['CFG_OEM_ID']			= 'OID_SOREL'
baseEnv['CFG_DEVICENAME']		= 'XHCC-S61v2'
baseEnv['TARGET_PLATFORM']		= 'QT'
baseEnv['BOARD']				= 'S61'
baseEnv['CFG_BOARD_REVISION']	= '1'
baseEnv['CFG_BOARD_VARIANT']	= '2'

#################################################
#################################################

buildDirPath	= "C:/development/xhcc/build/"
webDirPath		= 'C:/development/xhcc/web/teplomonitor-server/'

simulatorSourcePath = os.path.join(buildDirPath, projectName, deviceName, 'shared/platform/qtsim/')
print 'firmware source path: ' + simulatorSourcePath

versionFilePath =  os.path.join(buildDirPath, projectName, deviceName ,'shared/include/versionInfo.h')
print 'version file path: ' + versionFilePath

simulatorFolderName = func.parseVersionInfoFileToDestFolderName(versionFilePath)

simulatorFileName = func.MakeFilename(baseEnv, 'sim.exe')

simulatorSourceFilePath = os.path.join(simulatorSourcePath, simulatorFileName)
simulatorDestPath = os.path.join(simulatorDestPath, simulatorFolderName)

sourceSDCardFilesPath = 'C:/development/xhcc/web/teplomonitor-server/server'
destSDCardFilesPath = os.path.join(simulatorDestPath, 'WEB')

if not os.path.exists(simulatorDestPath):
	os.makedirs(simulatorDestPath)

if not os.path.exists(destSDCardFilesPath):
	os.makedirs(destSDCardFilesPath)

sourceSDCardFilesList = [	simulatorSourcePath	+ 'langs.sd',
							webDirPath			+ 'sitemenu.txt']

for sdFile in sourceSDCardFilesList:
	if os.path.isfile(sdFile):
		shutil.copy2(sdFile, simulatorDestPath)

shutil.copy2(simulatorSourceFilePath, simulatorDestPath)

func.copytree(sourceSDCardFilesPath, destSDCardFilesPath)