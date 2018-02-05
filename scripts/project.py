'''
Created on 28 sept. 2017.

@author: andrey.vinogradov
'''

import os
from subprocess import Popen
from termcolor import colored

def runSCons(args, path):
    print args
    
    p = Popen(["scons.bat"] + args,
        cwd = path
    )
    
    stdout, stderr = p.communicate()
    print stdout, stderr
    

class Device(object):
    '''
    classdocs
    '''
    
    def __init__(self, name, board, boardVariant, sdCard = False, microcontroller = 'stm32', olimex_target = 'stm32f1x.cfg'):
        self.name         = name
        self.board        = board
        self.boardVariant = boardVariant
        self.sdCard       = sdCard
        self.microcontroller = microcontroller
        self.olimex_target = olimex_target

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
        return self.name + postfix + '/'
    
    def getDeviceBuildDir(self):
        return os.path.join(self.path, "build/", self.getProjectDirName(), self.command + self.boardVariantToString()) + '/'
    
    def getSrcPath(self):
        if self.sdk == 'old':
            return 'shared/'
        elif self.sdk == 'new':
            return 'shared/sdk/'
    
    def getProjectFirmwareDir(self):
        return os.path.join(self.getDeviceBuildDir(), self.getSrcPath(), 'platform/', self.device.microcontroller) + '/'
    
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
    
    def getFirmwareLangPostfix(self):
        if not self.langkey == 'rom':
            return self.langkey + '-'
        return ''
        
    def generateFirmwareName(self):
        baseEnv = dict()
        baseEnv['CFG_OEM_ID']           = 'OID_SOREL'
        baseEnv['CFG_DEVICENAME']       = self.device.name
        baseEnv['TARGET_PLATFORM']      = self.device.microcontroller.upper()
        baseEnv['BOARD']                = self.device.board
        baseEnv['CFG_BOARD_REVISION']   = '1'
        baseEnv['CFG_BOARD_VARIANT']    = self.boardVariantToString()
        
        return self.MakeFilename(baseEnv, self.getFirmwareLangPostfix())
        
    def generateSDCardFirmwareFileName(self):
        firmwareFile = self.generateFirmwareName() + 'sdcard.bin'
        
        
        return firmwareFile
    
    def generateFirmwareFileName(self):
        firmwareName = self.generateFirmwareName()
        firmwareFile = firmwareName + 'merged.hex'
        firmwareDir  = self.getProjectFirmwareDir()
        
        firmwareFilePath = os.path.join(firmwareDir, firmwareFile)
        if not os.path.isfile(firmwareFilePath):
            firmwareFile = firmwareName + 'app.s19'
        
        return firmwareFile
    
    def getProjectBinaries(self):
        binaries = []
        
        firmwareFileName = self.generateFirmwareFileName()
        postfix = self.getFirmwareLangPostfix()
        
        binaries.append(firmwareFileName)
        binaries.append(postfix + 'app.map')
        binaries.append(postfix + 'app.elf')
        
        return binaries
    
    def clearSConsOptionsCacheFile(self):
        cache_setup_file = os.path.join(self.path, 'setup.py')
        if os.path.isfile(cache_setup_file):
            os.remove(cache_setup_file)
    
    def build(self, extraArgs = []):
        print colored("Building project: %s" % (self.workingName), 'white', 'on_green', attrs=['bold'])
        
        argList = [
            self.command      + self.boardVariantToString(),
            'CFG_PROJECT='    + self.name,
            'CFG_PLATFORM='   + self.platform,
            'CFG_PRODUCTION=' + ('1' if self.production else '0'),
            '--jobs=8',
#           '--debug=pdb',
        ]
        
        
        if self.production:
            productionArgList = [
                'CFG_LOG_MASK=0',
                'CFG_DEBUG_LOG_TM=0',
                'CFG_DEBUG_LOG_KSE=0',
            ]
            argList.extend(productionArgList)
        
        argList.extend(extraArgs)
        
        runSCons(argList, self.path)
    
    def clear(self):
        print colored("Clearing project: %s" % (self.workingName), 'white', 'on_green', attrs=['bold'])
        
        argList = [
                self.command      + self.boardVariantToString(),
                'CFG_PROJECT='    + self.name,
                'CFG_PLATFORM='   + self.platform,
                'CFG_PRODUCTION=' + ('1' if self.production else '0'),
                '--jobs=8',
                '-c',
        ]
        
        runSCons(argList, self.path)
    
    def addSDCardData(self, sdCardData):
        if sdCardData is None:
            return;
        self.sdCardData.extend(sdCardData)
    
    def addFirmwareData(self, firmwareData):
        self.firmwareData.extend(firmwareData)
    
    def flashLoader(self):
        print colored("Flashing loader: %s" % (self.workingName), 'white', 'on_green', attrs=['bold'])
        
        argList = [
                'flash_loader',
                'CFG_PROJECT='    + self.name,
                'CFG_PLATFORM='   + self.platform,
                'CFG_PRODUCTION=' + ('1' if self.production else '0'),
                '--jobs=1',
        ]
        
        runSCons(argList, self.path)
    
    def flashDevice(self):
        print colored("Flashing device: %s" % (self.workingName), 'white', 'on_green', attrs=['bold'])
        
        firmware = os.path.join(self.getProjectFirmwareDir(), self.generateFirmwareFileName())
        settings = os.path.join(self.path, 'src/', self.getSrcPath(), 'platform/stm32/', 'flash_stm32.cfg')
        interface = 'ftdi/olimex-arm-usb-tiny-h.cfg'
        target    = self.device.olimex_target
        #command = '-c "flash_and_quit %s"' % (firmware)
        #command = '-c "' + 'flash_and_quit ' + firmware + '"' 
        #OPENOCD_SCRIPTS = os.environ['OPENOCD_SCRIPTS']
        
        argList = [
                '-f', 'interface/' + interface,
                '-c', 'transport select jtag',
                '-f', 'target/' + target, 
                '-f', settings,
                '-c', 'flash_and_quit ' + firmware,
        ]
        
        print argList
        
        p = Popen(["openocd"] + argList,
        cwd = self.path)
        
        stdout, stderr = p.communicate()
        print stdout, stderr
        
    def getVersionLog(self):
        import subprocess
        VCS_PROGRAM = 'git'
        
        p = subprocess.Popen([VCS_PROGRAM, 'tag', '-l', '-n10', '--sort=-version:refname', '--merged'],
                             cwd = self.path,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        
        stdout, stderr = p.communicate()
        if p.returncode > 1:
            print 'git tag failed:'+stderr
            return 1

        return stdout
    
    def getSconsBuildArgs(self):
        setupFile = os.path.join(self.path, 'setup.py')
        
        with open(setupFile) as f:
            content = f.readlines()
        
        content = [x.strip() for x in content] 
        return content


