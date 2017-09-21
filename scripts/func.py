import os
import re
import shutil
from termcolor import colored
#################################################
#################################################

def print_warning(warning):
	warning = colored(warning, 'white', 'on_red')
	print warning
	input = raw_input(colored("Press ENTER to continue\r", 'red', 'on_white'))

def getProjectDirName(project):
	postfix = ''
	if project['production'] == '1':
		postfix = '_production'
	
	return project['projectName'] + postfix

def getDeviceBuildDir(project):
	return os.path.join(project['project_path'], "build", getProjectDirName(project), project['project'] + project['boardVariant'])
	
def getProjectFirmwareDir(project):
	return os.path.join(getDeviceBuildDir(project), 'shared/platform/stm32/')

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
	
	versionGU  = re.search(r'SHORT_VERSION.*"(.*)"', text).group(1)
	versionDate = re.search(r'VERSION_DATE.*"(.*)"', text).group(1)
	versionDate = versionDate.replace('/', '_')
	
	return versionDate + '_' + versionGU

def generateSDCardFirmwareFileName(project):
	baseEnv = dict()
	baseEnv['CFG_OEM_ID']			= 'OID_SOREL'
	baseEnv['CFG_DEVICENAME']		= project['deviceName']
	baseEnv['TARGET_PLATFORM']		= 'STM32'
	baseEnv['BOARD']				= project['board']
	baseEnv['CFG_BOARD_REVISION']	= '1'
	baseEnv['CFG_BOARD_VARIANT']	= project['boardVariant']
	
	sdCardFirmwarePostfix = 'sdcard.bin'
	if not project['langkey'] == 'rom':
		sdCardFirmwarePostfix = project['langkey'] + '-' + sdCardFirmwarePostfix
		
	return MakeFilename(baseEnv, sdCardFirmwarePostfix)
