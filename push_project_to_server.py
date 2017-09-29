import sys
import shutil
import glob
import os
sys.path.insert(0, "./scripts")
import func
from func import SrcDestData

def copyProjectBinaryFiles(project, dest):
	firmwareSourcePath = project.getProjectFirmwareDir()
	sourceExtensionList = ['map','s19','hex','bin']
	for extension in sourceExtensionList:
		for item in glob.glob(firmwareSourcePath+'*.'+extension):
			project.addFirmwareData([SrcDestData(item, os.path.join(dest, os.path.basename(item)))])

def do(project, dest):
	buildDirPath = project.getDeviceBuildDir()

	versionFilePath =  os.path.join(buildDirPath, 'shared/include/versionInfo.h')

	firmwareFolderName  = func.parseVersionInfoFileToDestFolderName(versionFilePath)
	firmwareDestPath    = os.path.join(dest, firmwareFolderName)
	firmwareDestPathBin = os.path.join(firmwareDestPath, 'firmware/')

	copyProjectBinaryFiles(project, 'firmware/')
	
	for firmwareData in project.firmwareData:
		func.copytree(firmwareData.src, os.path.join(firmwareDestPath, firmwareData.dest))
	
