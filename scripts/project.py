'''
Created on 28 sept. 2017.

@author: andrey.vinogradov
'''

import os
import re
import subprocess

from termcolor import colored

from subprocess import Popen

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
        
        #if self.sdk == 'new':
        #    postfix = '_production' if self.production else '_debug'
        
        return self.name + postfix
       
    def getTarget(self):
        target = self.target
        if self.sdk == 'old':
            target = target + self.boardVariantToString()
        
        return target
    
    def getBootloaderTarget(self):
        target = 'loader'
        if self.sdk == 'old':
            target = target + self.boardVariantToString()
        
        return target
    
    def getDeviceBuildDir    (self): return os.path.join(self.path, 'build', self.getProjectDirName(), self.getTarget())
    def getBootloaderBuildDir(self): return os.path.join(self.path, 'build', self.getProjectDirName(), self.getBootloaderTarget())
    def getDeviceBinDir      (self): return os.path.join(self.path, 'bin'  , self.getProjectDirName())
    
    def getSrcPath(self):
        if self.sdk == 'old':
            return 'shared'
        elif self.sdk == 'new':
            return 'shared/sdk'
    
    def getProjectFirmwareDir  (self): return os.path.join(self.getDeviceBuildDir()    , self.getSrcPath(), 'platform', self.device.microcontroller)
    def getProjectBootloaderDir(self): return os.path.join(self.getBootloaderBuildDir(), self.getSrcPath(), 'platform', self.device.microcontroller)
    def getVersionInfoFilePath (self): return os.path.join(self.getDeviceBuildDir()    , self.getSrcPath(), 'include/versionInfo.h')
    
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
        if 'TARGET_PLATFORM_FRIENDLY_NAME' not in env:
            if env['TARGET_PLATFORM'].lower() == "cubemx":
                env['TARGET_PLATFORM_FRIENDLY_NAME'] = "STM32C"
            else:
                env['TARGET_PLATFORM_FRIENDLY_NAME'] = env['TARGET_PLATFORM'].upper()
        
        platformstring = env['TARGET_PLATFORM_FRIENDLY_NAME']
        
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
        
    def generateFirmwareName(self, deviceName = None):
        if deviceName is None:
           deviceName = self.device.name
        
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
        
    def generateFirmwareFileName      (self): return self.generateFirmwareName() + 'app.s19'
    def generateMergedFirmwareFileName(self): return self.generateFirmwareName() + 'merged.s19'
    def generateSDCardFirmwareFileName(self): return self.generateFirmwareName() + 'sdcard.bin'
    def generateBootoaderFileName     (self): return self.generateFirmwareName('loader') + 'app.s19'
    def generateMapFileName           (self): return self.getFirmwareLangPostfix() + 'app.map'
    def generateElfFileName           (self): return self.getFirmwareLangPostfix() + 'app.elf'
    
    def getProjectBinaries(self):
        firmwareDir = self.getProjectFirmwareDir()
        bootldrDir  = self.getProjectBootloaderDir()
        
        firmwareFileName        = self.generateFirmwareFileName()
        mergedFirmwareFileName  = self.generateMergedFirmwareFileName()
        mapFileName             = self.generateMapFileName()
        elfFileName             = self.generateElfFileName()
        bootldrFirmwareFileName = self.generateBootoaderFileName()
        
        return [
            os.path.join(firmwareDir, firmwareFileName       ).replace("\\","/"),
            os.path.join(firmwareDir, mergedFirmwareFileName ).replace("\\","/"),
            os.path.join(firmwareDir, mapFileName            ).replace("\\","/"),
            os.path.join(firmwareDir, elfFileName            ).replace("\\","/"),
            os.path.join(bootldrDir , bootldrFirmwareFileName).replace("\\","/"),
        ]
    
    def clearSConsOptionsCacheFile(self):
        cache_setup_file = os.path.join(self.path, 'setup.py')
        if os.path.isfile(cache_setup_file):
            os.remove(cache_setup_file)
    
    def runSimulator(self, args):
        firmwareName = self.generateSimulatorName() + '.exe'
        simulator_file = os.path.join(self.getDeviceBinDir(), firmwareName)
        
        os.system('start '  + simulator_file + ' ' + args)
    
    def runSCons(self, args, path):
        from build_pack_push_and_clear_all_projects import getSconsDir, getPythonDir, getSconsJobsNum
        
        scons  = os.path.join(getSconsDir (self.name), 'scons')
        python = os.path.join(getPythonDir(self.name), 'python.exe')
        
        args.append('--jobs=' + getSconsJobsNum(self.name))
        
        print(args)
        
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
#           '--debug=pdb',
#           '--debug=time',
        ]
        
        
        if self.production:
            productionArgList = [
                'CFG_LOG_MASK=0',
            ]
            argList.extend(productionArgList)
        
        argList.extend(extraArgs)
        
        result = self.runSCons(argList, self.path)
        
        return result
       
    def getFirmwareSize(self):
        firmwareDir = self.getProjectFirmwareDir()
        elfFileName = self.generateElfFileName()
        elfFile = os.path.join(firmwareDir, elfFileName).replace("\\","/")
        
        sizeApp = 'E:/Tools/gcc_arm_none_eabi_10_2020-q4-major/bin/arm-none-eabi-size.exe'
       
        p = Popen([sizeApp, elfFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout, stderr = p.communicate()
        
        if stderr:
            print('File not found: %s'%(elfFile))
            return
        
        raw = stdout.split()
        
        text = int(raw[6])
        data = int(raw[7])
        bss  = int(raw[8])
        
        print('Flash\t: %d\n\rData\t: %d\n\rBSS\t: %d' % (text, data, bss))
        

    def showFirmwareMap(self):
        firmwareDir = self.getProjectFirmwareDir()
        mapFileName = self.generateMapFileName()
        mapFile = os.path.join(firmwareDir, mapFileName).replace("\\","/")
    	
    	
        firmwareName = self.generateSimulatorName() + '.exe'
        amap = 'F:/Tools/Amap/amap.exe'
                
        os.system('start '  + amap + ' ' + '-g ' + mapFile)
    	
    def clear(self):
        print( colored("Clearing project: %s" % (self.workingName), 'white', 'on_green', attrs=['bold']))
        
        argList = [
                self.getTarget(),
                'CFG_PROJECT='    + self.name,
                'CFG_PLATFORM='   + self.platform,
                'CFG_PRODUCTION=' + ('1' if self.production else '0'),
                '-c',
        ]
        
        self.runSCons(argList, self.path)
    
    def addSDCardData(self, sdCardData):
        if sdCardData is None:
            return;
        self.sdCardData.extend(sdCardData)
    
    def extendFirmwareData(self, firmwareData):
        self.firmwareData.extend(firmwareData)
        
    def appendFirmwareData(self, firmwareData):
        self.firmwareData.append(firmwareData)
    
    def getOpenOcdArgsCommon(self, programmingAdapter):
        from build_pack_push_and_clear_all_projects import getOpenOcdDir
        openOcdDir = getOpenOcdDir(self.name)
        settings = os.path.join(self.path, 'src', self.getSrcPath(), 'platform/stm32', 'flash_stm32.cfg').replace("\\","/")
        target	= self.device.configFile
        
        interfacePrefix  = 'ftdi/' if programmingAdapter['Ftdi'] else ''
        propertiesPrefix = 'ftdi_' if programmingAdapter['Ftdi'] else 'hla_'
        
        argList = [
            '-s', openOcdDir + 'scripts',
            '-f', 'interface/' + interfacePrefix + programmingAdapter['Interface'],
        ]
        
        
        if programmingAdapter['SerialNumber']: argList.extend(['-c', propertiesPrefix + 'serial '	  + programmingAdapter['SerialNumber']])
        if programmingAdapter['VID_PID']	 : argList.extend(['-c', propertiesPrefix + 'vid_pid '	 + programmingAdapter['VID_PID']])
        if programmingAdapter['Description'] : argList.extend(['-c', propertiesPrefix + 'device_desc ' + programmingAdapter['Description']])
        
        argList.extend([
                '-c', 'transport select ' + programmingAdapter['Transport'],
                '-f', 'target/' + target,
                '-c', 'adapter_nsrst_delay 1000',
                '-c', 'adapter_khz 4000',
                '-f', settings,
        ])
        
        return argList
    
    def callOpenOcd(self, argList):
        print("\n".join(argList))
        from build_pack_push_and_clear_all_projects import getOpenOcdDir
        openOcdDir = getOpenOcdDir(self.name)
        p = Popen([openOcdDir + "bin/openocd"] + argList, cwd = self.path)
        
        stdout, stderr = p.communicate()
        print(stdout, stderr)
    
    
    def flashCommon(self, firmware, programmingAdapter):
        argList = self.getOpenOcdArgsCommon(programmingAdapter)
        argList.extend(['-c', 'flash_and_quit ' + firmware])
        
        self.callOpenOcd(argList)
        
        
    def flashLoader(self, programmingAdapter):
        print(colored("Flashing loader: %s" % (self.workingName), 'white', 'on_green', attrs=['bold']))
        
        firmware = os.path.join(self.getProjectBootloaderDir(), self.generateBootoaderFileName()).replace("\\","/")
        
        self.flashCommon(firmware, programmingAdapter)
            
    
    def flashDevice(self, programmingAdapter):
        print(colored("Flashing device: %s" % (self.workingName), 'white', 'on_green', attrs=['bold']))
        
        firmware = os.path.join(self.getProjectFirmwareDir(), self.generateFirmwareFileName()).replace("\\","/")
        
        self.flashCommon(firmware, programmingAdapter)
        
    def rebootDevice(self, programmingAdapter):
        print(colored("Reboot device: %s" % (self.workingName), 'white', 'on_green', attrs=['bold']))
        
        argList = self.getOpenOcdArgsCommon(programmingAdapter)
        argList.extend(['-c', 'reboot'])
        
        self.callOpenOcd(argList)
        
        
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


