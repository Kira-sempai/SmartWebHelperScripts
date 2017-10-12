'''
Created on 28 sept. 2017.

@author: andrey.vinogradov
'''

import os
from subprocess import Popen
from termcolor import colored

class Device(object):
    '''
    classdocs
    '''
    
    def __init__(self, name, board, boardVariant, sdCard = False, microcontroller = 'stm32'):
        self.name         = name
        self.board        = board
        self.boardVariant = boardVariant
        self.sdCard       = sdCard
        self.microcontroller = microcontroller

class Project(object):
    '''
    classdocs
    '''
    
    def __init__(self, path, command, name, workingName, platform, device, langkey = 'west', sdk = 'old', production = False):
        '''
        Constructor
        TODO: make projectName and workingName the same
        '''
        self.path         = path
        self.command      = command
        self.name         = name
        self.workingName  = workingName
        self.platform     = platform
        self.production   = production
        self.device       = device
        self.langkey      = langkey
        self.sdk          = sdk
        self.sdCardData   = []
        self.firmwareData = []
        
    def boardVariantToString(self):
        if self.device.boardVariant is None:
            return ''
        else:
            return str(self.device.boardVariant)
        
    def getProjectDirName(self):
        postfix = ''
        #postfix = '_production' if self.production else ''
        return self.name + postfix
    
    def getDeviceBuildDir(self):
        return os.path.join(self.path, "build", self.getProjectDirName(), self.command + self.boardVariantToString())
        
    def getSrcPath(self):
        if self.sdk == 'old':
            return 'shared/'
        elif self.sdk == 'new':
            return 'shared/sdk/'
        
    def getProjectFirmwareDir(self):
        return os.path.join(self.getDeviceBuildDir(), self.getSrcPath(), 'platform/', self.device.microcontroller)
        
    def getVersionInfoFilePath(self):
        return os.path.join(self.getDeviceBuildDir(), self.getSrcPath(), 'include/versionInfo.h')
            
    
    #took from Sorel code
    def MakeFilename(self, env, postfix='', no_platform=False):
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
    
    def generateSDCardFirmwareFileName(self):
        baseEnv = dict()
        baseEnv['CFG_OEM_ID']           = 'OID_SOREL'
        baseEnv['CFG_DEVICENAME']       = self.device.name
        baseEnv['TARGET_PLATFORM']      = 'STM32'
        baseEnv['BOARD']                = self.device.board
        baseEnv['CFG_BOARD_REVISION']   = '1'
        baseEnv['CFG_BOARD_VARIANT']    = self.boardVariantToString()
        
        sdCardFirmwarePostfix = 'sdcard.bin'
        if not self.langkey == 'rom':
            sdCardFirmwarePostfix = self.langkey + '-' + sdCardFirmwarePostfix
            
        return self.MakeFilename(baseEnv, sdCardFirmwarePostfix)
        
    def clearSConsOptionsCacheFile(self):
        cache_setup_file = os.path.join(self.path, 'setup.py')
        if os.path.isfile(cache_setup_file):
            os.remove(cache_setup_file)
        
    def build(self):
        print colored("Building project: %s" % (self.getProjectDirName()), 'white', 'on_green', attrs=['bold'])

        argList = [
            self.command      + self.boardVariantToString(),
            'CFG_PROJECT='    + self.name,
            'CFG_PLATFORM='   + self.platform,
            'CFG_PRODUCTION=' + ('1' if self.production else '0'),
            '--jobs=8',
        ]

        print argList

        p = Popen(["scons.bat"] + argList,
            cwd = self.path
        )
      
        stdout, stderr = p.communicate()
        print stdout, stderr
    
    def clear(self):
        print colored("Clearing project: %s" % (self.getProjectDirName()), 'white', 'on_green', attrs=['bold'])
        
        p = Popen(
            [
                "scons.bat",
                self.command      + self.boardVariantToString(),
                'CFG_PROJECT='    + self.name,
                'CFG_PLATFORM='   + self.platform,
                'CFG_PRODUCTION=' + '1' if self.production else '0',
                '--jobs=8',
                '-c',
            ],
            cwd = self.path
        )
    
        stdout, stderr = p.communicate()
        print stdout, stderr
        
    def addSDCardData(self, sdCardData):
        if sdCardData is None:
            return;
        self.sdCardData.extend(sdCardData)
    
    def addFirmwareData(self, firmwareData):
        self.firmwareData.extend(firmwareData)
            