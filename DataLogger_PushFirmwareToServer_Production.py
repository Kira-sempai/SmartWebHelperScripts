import re
import shutil
import glob
import os
#################################################
#################################################
projectName = 'DataLogger_production'
deviceName = 'device'

firmwareDestPath="Z:/firmware/DataLogger production"

sourceWebArchiveList = ['DL_BL.bin', 'DL_FW.bin', 'DL_SD.bin', 'DL_FW_SD.bin']

baseEnv = dict()
baseEnv['CFG_OEM_ID']			= 'OID_SOREL'
baseEnv['CFG_DEVICENAME']		= 'DL'
baseEnv['TARGET_PLATFORM']		= 'STM32'
baseEnv['BOARD']				= 'L30'
baseEnv['CFG_BOARD_REVISION']	= '1'

#################################################
#################################################

buildDirPath = "C:/development/xhcc/build/"

firmwareSourcePath = os.path.join(buildDirPath, projectName, deviceName, 'shared/platform/stm32/')
print 'firmware source path: ' + firmwareSourcePath

versionFilePath =  os.path.join(buildDirPath, projectName, deviceName ,'shared/include/versionInfo.h')
print 'version file path: ' + versionFilePath

sourceExtensionList = ['map','s19','hex','bin']

file = open(versionFilePath,'r')

text = file.read()
print 'version file read: ' + text

file.close()
print 'file close'

versionGU  = re.search(r'SHORT_VERSION.*g(\w{7,7})',text).group(1)
versionDate = re.search(r'VERSION_DATE.*"(.*)"',text).group(1)
versionDate = versionDate.replace('/','_')

firmwareDestPath		= os.path.join(firmwareDestPath, versionDate+'_'+versionGU)
firmwareDestPathBin		= os.path.join(firmwareDestPath, 'firmware/')
firmwareDestPathWeb		= os.path.join(firmwareDestPath, 'web_firmware/')
firmwareDestPathSD		= os.path.join(firmwareDestPath, 'SD-card/')

if not os.path.exists(firmwareDestPath):
	os.makedirs(firmwareDestPath)

if not os.path.exists(firmwareDestPathBin):
	os.makedirs(firmwareDestPathBin)

if not os.path.exists(firmwareDestPathWeb):
	os.makedirs(firmwareDestPathWeb)

if not os.path.exists(firmwareDestPathSD):
	os.makedirs(firmwareDestPathSD)


for extension in sourceExtensionList:
	for item in glob.glob(firmwareSourcePath+'*.'+extension):
		shutil.copy2(item,firmwareDestPathBin)


sourceWebArchivePath		= 'C:/Users/dmitry/Desktop/FirmwarePacker/archive/'
sourceSDCardFilesPath		= 'C:/Users/dmitry/Desktop/FirmwarePacker/data_files/'

for archive in sourceWebArchiveList:
	shutil.copy2(sourceWebArchivePath + archive, firmwareDestPathWeb)


#took from Sorel code
def MakeFilename(env, postfix='', no_platform=False):
	"""Build a filename string with platform/board/etc with postfix appended"""
	# convert OEM id to string
	if env.has_key('CFG_OEM_ID'):
		oemstring = '-' + env['CFG_OEM_ID'][4:].title()
	else:
		oemstring = ''
	# get platform name
	if env.has_key('TARGET_PLATFORM_FRIENDLY_NAME'):
		platformstring = env['TARGET_PLATFORM_FRIENDLY_NAME']
	else:
		platformstring = env['TARGET_PLATFORM']

	subststring = env['CFG_DEVICENAME'] + oemstring
	if not no_platform:
		subststring = subststring + '-' + env['BOARD'] + 'v' + 'r' + env['CFG_BOARD_REVISION'] + '-' + platformstring
	return subststring + '-' + postfix

#copy /v /y C:\development\xhcc\build\DataLogger\device\shared\platform\stm32\DataLogger-Sorel-L30vr1-STM32-sdcard.bin    "Z:\firmware\DataLogger debug\SD-card\firmware.bin"

SDCardFirmwareFileName = MakeFilename(baseEnv, 'sdcard.bin')
SDCardFirmwareFileNameFormatted = 'firmware.bin'

SDCardFirmwareFileSource		= os.path.join(firmwareSourcePath, SDCardFirmwareFileName)
SDCardFirmwareFileDest			= os.path.join(firmwareDestPathSD, SDCardFirmwareFileNameFormatted)

shutil.copyfile(SDCardFirmwareFileSource, SDCardFirmwareFileDest)

sourceSDCardFilesList = ['langs.sd', 'dlparams.sd', 'sitemenu.txt']

for sdFile in sourceSDCardFilesList:
	if os.path.isfile(sourceSDCardFilesPath + sdFile):
		shutil.copy2(sourceSDCardFilesPath + sdFile, firmwareDestPathSD)

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)
				
				
copytree(sourceSDCardFilesPath + 'WEB', firmwareDestPathSD + 'WEB')