import shutil
import glob
import os
import func

def do(firmwareDestPath, production):
	#################################################
	#################################################
	if production :
		projectName = 'disco_production'
	else :
		projectName = 'disco'

	deviceName = 'device1'

	baseEnv = dict()
	baseEnv['CFG_OEM_ID']			= 'OID_SOREL'
	baseEnv['CFG_DEVICENAME']		= 'DISCO'
	baseEnv['TARGET_PLATFORM']		= 'STM32'
	baseEnv['BOARD']				= '32F746GDISCOVERY'
	baseEnv['CFG_BOARD_REVISION']	= '1'
	baseEnv['CFG_BOARD_VARIANT']	= '1'

	sourceWebArchiveList = [baseEnv['CFG_DEVICENAME'] + '_BL.bin',
							baseEnv['CFG_DEVICENAME'] + '_FW.bin',
							baseEnv['CFG_DEVICENAME'] + '_SD.bin',
							baseEnv['CFG_DEVICENAME'] + '_FW_SD.bin'
							]

	sdCardFirmwarePostfix			= 'west-sdcard.bin'
	#################################################
	#################################################

	buildDirPath	= os.path.join("C:/development/xhcc/build/", projectName, deviceName)
	webDirPath		= 'C:/development/xhcc/web/teplomonitor-server/'

	firmwareSourcePath = os.path.join(buildDirPath, 'shared/platform/stm32/')
	print 'firmware source path: ' + firmwareSourcePath

	versionFilePath =  os.path.join(buildDirPath, 'shared/include/versionInfo.h')
	print 'version file path: ' + versionFilePath

	firmwareFolderName = func.parseVersionInfoFileToDestFolderName(versionFilePath)

	firmwareDestPath			= os.path.join(firmwareDestPath, firmwareFolderName)
	firmwareDestPathBin			= os.path.join(firmwareDestPath, 'firmware/')
	firmwareDestPathWeb			= os.path.join(firmwareDestPath, 'web_firmware/')
	firmwareDestPathSD			= os.path.join(firmwareDestPath, 'SD-card/')
	firmwareDestPathSDUpdate	= os.path.join(firmwareDestPathSD, 'update/')

	firmwareDestPathList	= [ firmwareDestPath,
								firmwareDestPathBin,
								firmwareDestPathWeb,
								firmwareDestPathSD,
								firmwareDestPathSDUpdate
								]

	for path in firmwareDestPathList:
		if not os.path.exists(path):
			os.makedirs(path)


	sourceExtensionList = ['map','s19','hex','bin']
	for extension in sourceExtensionList:
		for item in glob.glob(firmwareSourcePath+'*.'+extension):
			shutil.copy2(item,firmwareDestPathBin)


	sourceWebArchivePath = 'C:/Users/dmitry/Desktop/FirmwarePacker/archive/'

	for archive in sourceWebArchiveList:
		shutil.copy2(sourceWebArchivePath + archive, firmwareDestPathWeb)

	SDCardFirmwareFileName = func.MakeFilename(baseEnv, sdCardFirmwarePostfix)

	SDCardFirmwareFileDestPath		= os.path.join(firmwareDestPathSDUpdate	, SDCardFirmwareFileName)
	SDCardFirmwareFileSourcePath	= os.path.join(firmwareSourcePath		, SDCardFirmwareFileName)

	shutil.copy2(SDCardFirmwareFileSourcePath, SDCardFirmwareFileDestPath)

	sourceSDCardFilesList = [	firmwareSourcePath	+ 'langs.sd',
								firmwareSourcePath	+ 'dlparams.sd',
								webDirPath			+ 'sitemenu.txt']

	for sdFile in sourceSDCardFilesList:
		if os.path.isfile(sdFile):
			shutil.copy2(sdFile, firmwareDestPathSD)

	sourceSDCardFilesPath = 'C:/Users/dmitry/Desktop/FirmwarePacker/data_files/'
	func.copytree(sourceSDCardFilesPath + 'WEB', firmwareDestPathSD + 'WEB')
	func.copytree(sourceSDCardFilesPath + 'GUI', firmwareDestPathSD + 'GUI')