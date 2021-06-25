import sys
import os
import func
from func import SrcDestData
from termcolor import colored

def copyProjectBinaryFiles(project, dest):
	firmwareSourcePath = project.getProjectFirmwareDir()
	
	for item in project.getProjectBinaries():
		fileName = os.path.basename(item)
		destFile = os.path.join(dest, fileName)
		project.appendFirmwareData(SrcDestData(item, destFile))

def addVersionInfoFile(project, firmwareDestPath):
	fileName = os.path.join(firmwareDestPath, 'versionLog.txt')
	
	dirname = os.path.dirname(fileName)
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	
	f1 = open(fileName, 'w+')
	f1.write('List of changes:\n\n' + project.getVersionLog())
	f1.close()
	
def addBuildArgsListFile(project, firmwareDestPath):
	fileName = os.path.join(firmwareDestPath, 'buildArgs.txt')
	
	dirname = os.path.dirname(fileName)
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		
	f1 = open(fileName, 'w+')
	f1.write('Project built with following args:\n\n')
	for item in project.getSconsBuildArgs():
		f1.write("%s\n" % item)
	f1.close()
	

def do(project, dest):
	version = project.getVersion()
	
	firmwareFolderName = version.name
	if version.unstable:
		dest = dest + ' unstable'
		
	firmwareDestPath    = os.path.join(dest, firmwareFolderName)
	print(colored("pushing project to " + firmwareDestPath,
				'white',
				'on_green',
				attrs=['bold']))

	addVersionInfoFile(project, firmwareDestPath)
	addBuildArgsListFile(project, firmwareDestPath)
	
	copyProjectBinaryFiles(project, 'firmware')
	
	for firmwareData in project.firmwareData:
		src = firmwareData.src
		dst = os.path.join(firmwareDestPath, firmwareData.dest)
		
		if os.path.exists(src):
			func.copytree(src, dst)
		else:
			print("src not found: " + src)
	
