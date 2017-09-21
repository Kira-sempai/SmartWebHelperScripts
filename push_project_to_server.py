import sys
import shutil
import glob
import os
sys.path.insert(0, "./scripts")
import func

def copyProjectBinaryFiles(project, dest):
	firmwareSourcePath = func.getProjectFirmwareDir(project)
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

	buildDirPath	= func.getDeviceBuildDir(project)

	versionFilePath =  os.path.join(buildDirPath, 'shared/include/versionInfo.h')

	firmwareFolderName = func.parseVersionInfoFileToDestFolderName(versionFilePath)

	firmwareDestPath            = os.path.join(dest, firmwareFolderName)
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
			try:
				os.makedirs(path)
			except Exception as e:
				func.print_warning('%s \n\r%s' % (e, 'Probably server not available =('))
				sys.exit()

	copyProjectBinaryFiles(project, firmwareDestPathBin)

	sourceWebArchivePath = './archive'

	for archive in sourceWebArchiveList:
		shutil.copy2(os.path.join(sourceWebArchivePath, archive), firmwareDestPathWeb)

	SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(project)

	sourceSDCardFilesPath = './data_files'
	func.copytree(sourceSDCardFilesPath, firmwareDestPathSD)
	
