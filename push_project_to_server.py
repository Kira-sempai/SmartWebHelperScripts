import shutil
import glob
import os
import func

def copyProjectBinaryFiles(project, dest)
	firmwareSourcePath = funct.getProjectFirmwareDir(project)
	sourceExtensionList = ['map','s19','hex','bin']
	for extension in sourceExtensionList:
		for item in glob.glob(firmwareSourcePath+'*.'+extension):
			shutil.copy2(item,dest)

def do(project, dest):
	#################################################
	#################################################
	
	sourceWebArchiveList = [
		project['deviceName'] + '_BL.bin',
		project['deviceName'] + '_FW.bin',
		project['deviceName'] + '_SD.bin',
		project['deviceName'] + '_FW_SD.bin'
	]

	#################################################
	#################################################

	buildDirPath	= getDeviceBuildDir(project)
	webDirPath		= 'C:/development/xhcc/web/teplomonitor-server/'

	versionFilePath =  os.path.join(buildDirPath, 'shared/include/versionInfo.h')
	print 'version file path: ' + versionFilePath

	firmwareFolderName = func.parseVersionInfoFileToDestFolderName(versionFilePath)

	firmwareDestPath            = os.path.join(dest, getProjectDirName(project), firmwareFolderName)
	firmwareDestPathBin			= os.path.join(firmwareDestPath, 'firmware/')
	firmwareDestPathWeb			= os.path.join(firmwareDestPath, 'web_firmware/')
	firmwareDestPathSD			= os.path.join(firmwareDestPath, 'SD-card/')

	firmwareDestPathList	= [ 
								firmwareDestPathBin,
								firmwareDestPathWeb,
								firmwareDestPathSD,
								]

	for path in firmwareDestPathList:
		if not os.path.exists(path):
			os.makedirs(path)

	copyProjectBinaryFiles(project, firmwareDestPathBin)

	sourceWebArchivePath = './archive'

	for archive in sourceWebArchiveList:
		shutil.copy2(sourceWebArchivePath + archive, firmwareDestPathWeb)

	SDCardFirmwareFileName = func.MakeFilename(baseEnv, sdCardFirmwarePostfix)

	SDCardFirmwareFileDestPath		= os.path.join(firmwareDestPathSDUpdate	, SDCardFirmwareFileName)
	SDCardFirmwareFileSourcePath	= os.path.join(firmwareSourcePath		, SDCardFirmwareFileName)

	shutil.copy2(SDCardFirmwareFileSourcePath, SDCardFirmwareFileDestPath)

	sourceSDCardFilesPath = './data_files'
	func.copytree(sourceSDCardFilesPath, firmwareDestPathSD)