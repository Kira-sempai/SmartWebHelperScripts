import re
import shutil
import glob
import os
#################################################
#################################################
projectName = 'caleon_clima'
deviceName = 'device'

firmwareDestPath="Z:/firmware/Caleon production"
#################################################
#################################################

buildDirPath = "C:/development/caleon_smartweb/build/"


firmwareSourcePath = os.path.join(buildDirPath, projectName, deviceName, 'shared/sdk/platform/stm32n/')
versionFilePath =  os.path.join(buildDirPath, projectName, deviceName ,'shared/sdk/include/versionInfo.h')

sourceExtensionList = ['elf','map','s19','hex','bin']

file = open(versionFilePath,'r')
text = file.read()
file.close()

versionGU  = re.search(r'SHORT_VERSION.*"(.*)"',text).group(1)
versionDate = re.search(r'VERSION_DATE.*"(.*)"',text).group(1)
versionDate = versionDate.replace('/','_')

firmwareDestPath = os.path.join(firmwareDestPath, 'Caleon'+versionDate+'_'+versionGU)

if not os.path.exists(firmwareDestPath):
	os.makedirs(firmwareDestPath)

for extension in sourceExtensionList:
	for item in glob.glob(firmwareSourcePath+'*.'+extension):
		shutil.copy2(item,firmwareDestPath)