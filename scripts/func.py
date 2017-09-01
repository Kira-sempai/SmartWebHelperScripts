import os
import re
import shutil
#################################################
#################################################

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
		subststring = subststring + '-' + env['BOARD'] + 'v' + env['CFG_BOARD_VARIANT'] + 'r' + env['CFG_BOARD_REVISION'] + '-' + platformstring
	return subststring + '-' + postfix

#copy all files in dir and subdirs
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

def parseVersionInfoFileToDestFolderName(versionFilePath):
	file = open(versionFilePath, 'r')
	text = file.read()
	print 'version file read: ' + text

	file.close()
	
	versionGU  = re.search(r'SHORT_VERSION.*g(\w{7,7})', text).group(1)
	versionDate = re.search(r'VERSION_DATE.*"(.*)"', text).group(1)
	versionDate = versionDate.replace('/', '_')
	
	return versionDate + '_' + versionGU

def generateSDCardFirmwareFileName(deviceName, board, boardVariant, langkey):
	baseEnv = dict()
	baseEnv['CFG_OEM_ID']			= 'OID_SOREL'
	baseEnv['CFG_DEVICENAME']		= deviceName
	baseEnv['TARGET_PLATFORM']		= 'STM32'
	baseEnv['BOARD']				= board
	baseEnv['CFG_BOARD_REVISION']	= '1'
	baseEnv['CFG_BOARD_VARIANT']	= boardVariant
	
	sdCardFirmwarePostfix = 'sdcard.bin'
	if not langkey == 'rom':
		sdCardFirmwarePostfix = langkey + '-' + sdCardFirmwarePostfix
		
	return MakeFilename(baseEnv, sdCardFirmwarePostfix)
