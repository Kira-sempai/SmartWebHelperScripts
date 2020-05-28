'''
Created on 28 sept. 2017.

@author: andrey.vinogradov
'''

import os
import re

import func
from subprocess import Popen
from termcolor import colored


class Version(object):
    '''
    classdocs
    '''
    
    def __init__(self, versionFilePath):
        self.date = '0000-00-00'
        self.name = 'undefined'
        self.modified = False
        self.unstable = False
        
        if not os.path.isfile(versionFilePath):
            func.print_warning('Version file %s not found' %(versionFilePath))
            return
        
        versionFile = open(versionFilePath, 'r', encoding='utf-8')
        text = versionFile.read()
       
        versionFile.close()
        
        versionGU   = re.search(r'SHORT_VERSION.*"(.*)"', text).group(1)
        versionDate = re.search(r'VERSION_DATE.*"(.*)"', text).group(1)
        versionDate = versionDate.replace('/', '_')
        
        self.date = versionDate
        self.name = self.date + '_' + versionGU
        self.modified = versionGU.endswith('m')
        self.unstable = (versionGU[-2:-1] == 'u') if self.modified else versionGU.endswith('u')


class Device(object):
    '''
    classdocs
    '''
    
    def __init__(self, name, board, boardVariant, sdCard = False, microcontroller = 'stm32', configFile = 'stm32f1x.cfg'):
        self.name         = name
        self.board        = board
        self.boardVariant = boardVariant
        self.sdCard       = sdCard
        self.microcontroller = microcontroller
        self.configFile   = configFile

class Project(object):
    '''
    classdocs
    '''
    
    def __init__(self, group, name, workingName, device, langkey = 'west', sdk = 'old', production = False, oem_id = 'OID_SOREL'):
        '''
        Constructor
        '''
        self.group        = group
        self.name         = name
        self.workingName  = workingName
        self.platform     = 'device'
        self.production   = production
        self.device       = device
        self.langkey      = langkey
        self.sdk          = sdk
        self.sdCardData   = []
        self.firmwareData = []
        self.oem_id       = oem_id
        self.target       = 'device'
    
    def setPath(self, path):
        self.path = path
    
    def boardVariantToString(self):
        if self.device.boardVariant is None:
            return ''
        else:
            return str(self.device.boardVariant)
    
    def getProjectDirName(self):
        #postfix = ''
        postfix = '_production' if self.production else ''
        return self.name + postfix
       
    def getTarget(self):
        target = self.target
        target = target + self.boardVariantToString()
        
        return target
    
    def getBootloaderTarget(self):
        target = 'loader'
        target = target + self.boardVariantToString()
        
        return target
    
    def getDeviceBuildDir(self):
        return os.path.join(self.path, 'build', self.getProjectDirName(), self.getTarget())
    
    def getBootloaderBuildDir(self):
        return os.path.join(self.path, 'build', self.getProjectDirName(), self.getBootloaderTarget())
    
    def getDeviceBinDir(self):
        return os.path.join(self.path, 'bin', self.getProjectDirName())
    
    
    def getSrcPath(self):
        if self.sdk == 'old':
            return 'shared'
        elif self.sdk == 'new':
            return 'shared/sdk'
    
    def getProjectFirmwareDir(self):
        return os.path.join(self.getDeviceBuildDir(), self.getSrcPath(), 'platform', self.device.microcontroller)
    
    def getProjectBootloaderDir(self):
        return os.path.join(self.getBootloaderBuildDir(), self.getSrcPath(), 'platform', self.device.microcontroller)
    
    def getVersionInfoFilePath(self):
        return os.path.join(self.getDeviceBuildDir(), self.getSrcPath(), 'include/versionInfo.h')
    
    def getVersion(self):
        return Version(self.getVersionInfoFilePath())
    
    #took from Sorel code
    def MakeFilename(self, env, postfix='', no_platform=False):
        """Build a filename string with platform/board/etc with postfix appended"""
        # convert OEM id to string
        if 'CFG_OEM_ID' in env:
            oemstring = '-' + env['CFG_OEM_ID'][4:].title()
        else:
            oemstring = ''
        # get platform name
        if 'TARGET_PLATFORM_FRIENDLY_NAME' in env:
            platformstring = env['TARGET_PLATFORM_FRIENDLY_NAME']
        else:
            platformstring = env['TARGET_PLATFORM']
            
        subststring = env['CFG_DEVICENAME'] + oemstring
        if not no_platform:
            subststring = subststring + '-' + env['BOARD'] + 'v' + env['CFG_BOARD_VARIANT'] + 'r' + env['CFG_BOARD_REVISION'] + '-' + platformstring
        return subststring + '-' + postfix
    
    def getFirmwareLangPostfix(self, noLangs = False):
        if noLangs:
            return ''
        
        if not self.langkey == 'rom':
            return self.langkey + '-'
        return ''
        
    def generateFirmwareName(self, deviceName):
        baseEnv = dict()
        baseEnv['CFG_OEM_ID']           = self.oem_id
        baseEnv['CFG_DEVICENAME']       = deviceName
        baseEnv['TARGET_PLATFORM']      = self.device.microcontroller.upper()
        baseEnv['BOARD']                = self.device.board
        baseEnv['CFG_BOARD_REVISION']   = '1'
        baseEnv['CFG_BOARD_VARIANT']    = self.boardVariantToString()
        
        #work around
        noLangs = deviceName == 'loader'
        
        return self.MakeFilename(baseEnv, self.getFirmwareLangPostfix(noLangs))
        
    def generateSimulatorName(self):
        baseEnv = dict()
        baseEnv['CFG_OEM_ID']           = self.oem_id
        baseEnv['CFG_DEVICENAME']       = self.device.name
        baseEnv['TARGET_PLATFORM']      = 'QT'
        baseEnv['BOARD']                = self.device.board
        baseEnv['CFG_BOARD_REVISION']   = '1'
        baseEnv['CFG_BOARD_VARIANT']    = self.boardVariantToString()
        
        prefix = ''
        
        return self.MakeFilename(baseEnv, prefix+'sim')
        
    def generateSDCardFirmwareFileName(self):
        firmwareFile = self.generateFirmwareName(self.device.name) + 'sdcard.bin'
        
        
        return firmwareFile
    
    def generateFirmwareFileName(self, deviceName):
        firmwareName = self.generateFirmwareName(deviceName)
        firmwareFile = firmwareName+ 'app.s19'

        return firmwareFile
    
    def getProjectBinaries(self):
        binaries = []
        
        firmwareFileName = self.generateFirmwareFileName(self.device.name)
        postfix = self.getFirmwareLangPostfix()
        
        binaries.append(firmwareFileName)
        binaries.append(postfix + 'app.map')
        binaries.append(postfix + 'app.elf')
        
        return binaries
    
    def clearSConsOptionsCacheFile(self):
        cache_setup_file = os.path.join(self.path, 'setup.py')
        if os.path.isfile(cache_setup_file):
            os.remove(cache_setup_file)
    
    def runSimulator(self):
        firmwareName = self.generateSimulatorName() + '.exe'
        simulator_file = os.path.join(self.getDeviceBinDir(), firmwareName)
        
        os.system('start '  + simulator_file)
    
    def runSCons(self, args, path):
        from build_pack_push_and_clear_all_projects import getSconsDir
        from build_pack_push_and_clear_all_projects import getPythonDir
        print(args)
        
        scons  = os.path.join(getSconsDir (self.name), 'scons')
        python = os.path.join(getPythonDir(self.name), 'python.exe')
        
        try:
            p = Popen([python, scons] + args,
                cwd = path
            )
        except FileNotFoundError:
            scons = 'scons.bat'
            p = Popen([scons] + args,
                cwd = path
            )
        
        stdout, stderr = p.communicate()
        print(stdout, stderr)
        
        result = p.returncode
        
        if result:
            print( colored('Scons failed: ' + str(result), 'white', 'on_red', attrs=['bold']))
        
        return result
    
    
    def build(self, extraArgs = []):
        print( colored("\n\rBuilding project: %s" % (self.workingName), 'white', 'on_green', attrs=['bold']))
        
        argList = [
            self.getTarget(),
            'CFG_PROJECT='    + self.name,
            'CFG_PLATFORM='   + self.platform,
            'CFG_PRODUCTION=' + ('1' if self.production else '0'),
#            'features=dbgmcu',
            '--jobs=8',
#           '--debug=pdb',
#           '--debug=time',
        ]
        
        
        if self.production:
            productionArgList = [
                'CFG_LOG_MASK=0',
                'CFG_DEBUG_LOG_TM=0',
                'CFG_DEBUG_LOG_KSE=0',
            ]
            argList.extend(productionArgList)
        
        argList.extend(extraArgs)
        
        result = self.runSCons(argList, self.path)
        
        return result
    
    def clear(self):
        print( colored("Clearing project: %s" % (self.workingName), 'white', 'on_green', attrs=['bold']))
        
        argList = [
                self.getTarget(),
                'CFG_PROJECT='    + self.name,
                'CFG_PLATFORM='   + self.platform,
                'CFG_PRODUCTION=' + ('1' if self.production else '0'),
                '--jobs=8',
                '-c',
        ]
        
        self.runSCons(argList, self.path)
    
    def addSDCardData(self, sdCardData):
        if sdCardData is None:
            return;
        self.sdCardData.extend(sdCardData)
    
    def addFirmwareData(self, firmwareData):
        self.firmwareData.extend(firmwareData)
    
    def flashCommon(self,
            firmware,
            programmingAdapterFtdi,
            programmingAdapterVID_PID,
            programmingAdapterSerialNumber,
            programmingAdapterDescription,
            programmingAdapterInterface,
            programmingAdapterTransport):
    
        from build_pack_push_and_clear_all_projects import getOpenOcdDir
        openOcdDir = getOpenOcdDir(self.name)
        settings = os.path.join(self.path, 'src', self.getSrcPath(), 'platform/stm32', 'flash_stm32.cfg').replace("\\","/")
        interface = programmingAdapterInterface
        target	= self.device.configFile
        transport = programmingAdapterTransport
        
        interfacePrefix = 'ftdi/' if programmingAdapterFtdi else ''
        
        argList = [
            '-s', openOcdDir + 'scripts',
            '-f', 'interface/' + interfacePrefix + programmingAdapterInterface,
            ]
        
        propertiesPrefix = 'ftdi_' if programmingAdapterFtdi else 'hla_'
        
        if programmingAdapterSerialNumber:   argList.extend(['-c', propertiesPrefix + 'serial '      + programmingAdapterSerialNumber])
        if programmingAdapterVID_PID	 :   argList.extend(['-c', propertiesPrefix + 'vid_pid '     + programmingAdapterVID_PID])
        if programmingAdapterDescription :   argList.extend(['-c', propertiesPrefix + 'device_desc ' + programmingAdapterDescription])
        
        argList.extend([
                '-c', 'transport select ' + programmingAdapterTransport,
                '-f', 'target/' + target,
                '-c', 'adapter_nsrst_delay 1000',
                '-f', settings,
                '-c', 'flash_and_quit ' + firmware,
        ])
        
        print("\n".join(argList))
        
        
        p = Popen([openOcdDir + "bin/openocd"] + argList,
        cwd = self.path)
        
        stdout, stderr = p.communicate()
        print(stdout, stderr)
        
        
    def flashLoader(self,
            programmingAdapterFtdi,
            programmingAdapterVID_PID,
            programmingAdapterSerialNumber,
            programmingAdapterDescription,
            programmingAdapterInterface,
            programmingAdapterTransport):
        print(colored("Flashing loader: %s" % (self.workingName), 'white', 'on_green', attrs=['bold']))
        
        firmware = os.path.join(self.getProjectBootloaderDir(), self.generateFirmwareFileName('loader')).replace("\\","/")
        
        self.flashCommon(
            firmware,
            programmingAdapterFtdi,
            programmingAdapterVID_PID,
            programmingAdapterSerialNumber,
            programmingAdapterDescription,
            programmingAdapterInterface,
            programmingAdapterTransport)
            
    
    def flashDevice(self,
            programmingAdapterFtdi,
            programmingAdapterVID_PID,
            programmingAdapterSerialNumber,
            programmingAdapterDescription,
            programmingAdapterInterface,
            programmingAdapterTransport):
        print(colored("Flashing device: %s" % (self.workingName), 'white', 'on_green', attrs=['bold']))
        
        firmware = os.path.join(self.getProjectFirmwareDir(), self.generateFirmwareFileName(self.device.name)).replace("\\","/")
        
        self.flashCommon(
            firmware,
            programmingAdapterFtdi,
            programmingAdapterVID_PID,
            programmingAdapterSerialNumber,
            programmingAdapterDescription,
            programmingAdapterInterface,
            programmingAdapterTransport)
        
        
    def getVersionLog(self):
        import subprocess
        VCS_PROGRAM = 'git'
        
        p = subprocess.Popen([VCS_PROGRAM, 'tag', '-l', '-n40', '--sort=-version:refname', '--merged'],
                             cwd = self.path,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        
        stdout, stderr = p.communicate()
        if p.returncode > 1:
            print('git tag failed:'+stderr)
            return 1

        return stdout.decode('utf-8')
    
    def getSconsBuildArgs(self):
        setupFile = os.path.join(self.path, 'setup.py')
        
        with open(setupFile, 'r', encoding='utf-8') as f:
            content = f.readlines()
        
        content = [x.strip() for x in content] 
        return content


