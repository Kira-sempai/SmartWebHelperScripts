import re
import shutil
import glob
import os
#################################################
#################################################
projectName = 'ltdc'
deviceName = 'qtsim3'

firmwareDestPath="Z:/simulator/SmartWeb L"
#################################################
#################################################

buildDirPath = "C:/development/stdc_clean/build/"


firmwareSourcePath = os.path.join(buildDirPath, projectName, deviceName, 'shared/platform/qtsim/')
versionFilePath =  os.path.join(buildDirPath, projectName, deviceName ,'shared/include/versionInfo.h')

sourceExtensionList = ['exe']

file = open(versionFilePath,'r')
text = file.read()
file.close()

versionGU  = re.search(r'SHORT_VERSION.*g(\w{7,7})',text).group(1)
versionDate = re.search(r'VERSION_DATE.*"(.*)"',text).group(1)
versionDate = versionDate.replace('/','_')

firmwareDestPath = os.path.join(firmwareDestPath, versionDate+'_'+versionGU)

if not os.path.exists(firmwareDestPath):
	os.makedirs(firmwareDestPath)

for extension in sourceExtensionList:
	for item in glob.glob(firmwareSourcePath+'*.'+extension):
		shutil.copy2(item,firmwareDestPath)