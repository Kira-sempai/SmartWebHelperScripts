import sys
import os
sys.path.insert(0, "./scripts")
import func
from func import SrcDestData

def copyProjectBinaryFiles(project, dest):
	firmwareSourcePath = project.getProjectFirmwareDir()
	
	for item in project.getProjectBinaries():
		project.addFirmwareData([SrcDestData(os.path.join(firmwareSourcePath, item), os.path.join(dest, item))])

def do(project, dest):
	versionFilePath = project.getVersionInfoFilePath()

	firmwareFolderName  = func.parseVersionInfoFileToDestFolderName(versionFilePath)
	firmwareDestPath    = os.path.join(dest, firmwareFolderName)

	copyProjectBinaryFiles(project, 'firmware/')
	
	for firmwareData in project.firmwareData:
		func.copytree(firmwareData.src, os.path.join(firmwareDestPath, firmwareData.dest))
	
