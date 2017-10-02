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
	items = []
	for extension in sourceExtensionList:
		items += [each for each in os.listdir(firmwareSourcePath) if each.endswith(extension)]
	
	for item in items:
		project.addFirmwareData([SrcDestData(os.path.join(firmwareSourcePath, item), os.path.join(dest, item))])

def do(project, dest):
	versionFilePath = project.getVersionInfoFilePath()

	firmwareFolderName  = func.parseVersionInfoFileToDestFolderName(versionFilePath)
	firmwareDestPath    = os.path.join(dest, firmwareFolderName)
	firmwareDestPathBin = os.path.join(firmwareDestPath, 'firmware/')

	copyProjectBinaryFiles(project, 'firmware/')
	
	for firmwareData in project.firmwareData:
		func.copytree(firmwareData.src, os.path.join(firmwareDestPath, firmwareData.dest))
	
