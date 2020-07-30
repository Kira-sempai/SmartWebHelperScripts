# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from subprocess import Popen

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(PROJECT_DIR)

sys.path.insert(0, PROJECT_DIR + "/scripts")

try:
	import configparser
except ImportError:
	import ConfigParser as configparser

try:
	import colorama
except ImportError:
	from scripts import colorama 
	print('colorama is missing: use "pip install colorama" to add it to Python')

try:
	from termcolor import colored
except ImportError:
	from scripts import termcolor
	print('termcolor is missing: use "pip install termcolor" to add it to Python')


from project import Project, Device
from func import SrcDestData
import pack_project
import push_project_to_server

settingsPath = 'settings.ini'
configParserInstance = configparser.ConfigParser()

def getProjectDestPathPostfix(project):
	return ' production' if project.production else ' debug'

def printAvailableProjectsList(projects_array):
	print('Projects list:')
	for p in projects_array:
		l = len(p.workingName)
		l2 = len(p.name)
		space = 15 - l
		space2 = 20 - l2
		print (p.workingName + ' '*space + '- ' + p.name + ' '*space2 + '(' + p.group + ')')

def getAvailableProjectsList():
	return [
		Project('SW1',         'stdc'        , 'SmartWeb S'    , Device('STDC'    , 'S20' , 3), 'rom'),
		Project('SW1_special', 'stdc_lin'    , 'SmartWeb S LIN', Device('STDC_LIN', 'S28' , 3), 'rom'),
		Project('SW1',         'ltdc'        , 'SmartWeb L'    , Device('LTDC'    , 'S40' , 3), 'rom'),
		Project('SW1',         'ltdc_s45'    , 'SmartWeb L2'   , Device('LTDC_S45', 'S45' , 1), 'rom'),
		Project('SW1',         'swndin'      , 'SmartWeb N'    , Device('SWNDIN'  , 'S41N', 1), 'rom'),
		
		Project('SW2_deprecated', 'DataLogger'       , 'DataLogger'        , Device('DL'    , 'L30', None, True), 'rom'),
		Project('SW2',            'DataLoggerSW'     , 'DataLogger SW'     , Device('DL_SW' , 'L30', None, True), 'rom'),
		Project('SW2',            'DataLoggerKSE'    , 'DataLogger KSE'    , Device('DL_KSE', 'L30', None, True), 'rom'),
		
		Project('SW2', 'disco'       , 'SmartWeb Disco', Device('DISCO'   , '32F746GDISCOVERY',    1, True, 'stm32', 'stm32f7x.cfg')),
		Project('SW2', 'xhcc'        , 'SmartWeb X'    , Device('XHCC'    , 'S61'             ,    2, True, 'stm32', 'stm32f2x.cfg')),
		Project('SW2', 'xhcc_s62'    , 'SmartWeb X2'   , Device('XHCC-S62', 'S62'             ,    2, True, 'stm32', 'stm32f2x.cfg')),
		Project('Other', 'xhcc_s62_unitTest', 'SmartWeb X2 Unit Test', Device('XHCC-S62', 'S62',   2, True, 'stm32', 'stm32f2x.cfg')),
		Project('SW2', 'swk'         , 'SmartWeb K'    , Device('SWK'     , 'SW-N2'           ,    1, True, 'stm32', 'stm32f2x.cfg'), 'west', 'old', False, 'OID_HLOGO'),
		
		Project('Caleon', 'caleon_clima', 'Caleon'        , Device('caleon_clima', 'RC40',    1, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'caleon_brv'  , 'Caleon BRV'    , Device('caleon_brv'  , 'RC50', None, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'domvs'       , 'Domvs'         , Device('Domvs'       , 'RC40', None, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'caleon_clima_smart_controller'    , 'Caleon SW', Device('caleon_clima_smart_controller'    , 'RC50', None, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'caleon_clima_smart_web_controller', 'Caleon SW', Device('caleon_clima_smart_web_controller', 'RC50', None, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'tece_floor', 'Caleon TECE', Device('tece_floor', 'RC50', None, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'tece_floor_clima_smart', 'Caleon TECE Clima', Device('tece_floor', 'RC50', None, False, 'stm32n'), 'rom', 'new'),
		
		Project('Other', 'lfwc'                 , 'LFWC'              , Device('LFWC'       , 'S40', None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_v01'          , 'LFWC'              , Device('LFWC-MT-V01', 'S40', None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_v02'          , 'LFWC'              , Device('LFWC-MT-V02', 'S40', None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_s47'          , 'LFWC'              , Device('LFWC-MT-S47', 'S47', None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_s47_unitTest' , 'LFWC Unit Test'    , Device('LFWC-MT-S47', 'S47', None, False, 'stm32'), 'rom'),
		Project('Other', 'charlie'              , 'CHARLIE'           , Device('CHARLIE'    , 'S48',    1, False, 'stm32'), 'rom', 'old', False, 'OID_Kemper'),
		Project('Other', 'charlie_runTimeTest'  , 'CHARLIE Runtime Test', Device('CHARLIE'    , 'S48',    1, False, 'stm32'), 'rom', 'old', False, 'OID_Kemper'),
		Project('Other', 'charlie_unitTest'     , 'CHARLIE Unit Test' , Device('CHARLIE'    , 'S48',    1, False, 'stm32'), 'rom', 'old', False, 'OID_Kemper'),

		Project('Other', 'DataLoggerCharlie'            , 'DataLogger Charlie'             , Device('DataLoggerCharlie' , 'L30', None, False, 'stm32'), 'rom', 'old', False, 'OID_SOREL'),
		Project('Other', 'DataLoggerCharlie_unitTest'   , 'DataLogger Charlie Unit Test'   , Device('DataLoggerCharlie' , 'L30', None, False, 'stm32'), 'rom', 'old', False, 'OID_SOREL'),
		Project('Other', 'DataLoggerCharlie_runTimeTest', 'DataLogger Charlie Runtime Test', Device('DataLoggerCharlie' , 'L30', None, False, 'stm32'), 'rom', 'old', False, 'OID_SOREL'),
	]

def getSDCardFirmwarePath(project):
	name = project.name
	
	if ((name == 'xhcc')   or
		(name == 'xhcc_s62') or
		(name == 'disco') or
		(name == 'swk')):
		return 'update'
	
	return ''
	
class cd:
	"""Context manager for changing the current working directory"""
	def __init__(self, newPath):
		self.newPath = os.path.expanduser(newPath)

	def __enter__(self):
		self.savedPath = os.getcwd()
		os.chdir(self.newPath)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.savedPath)

def buildWebPages(webPagesPath):
	packerPath = os.path.join(webPagesPath, 'less')
	
	if not os.path.exists(os.path.join(packerPath, 'build.py')):
		return False
	
	with cd(packerPath):
		p = Popen(['python', 'build.py', 'datalogger'])
		p.communicate()
	
	return True

def getSDCardProjectFiles(project):
	if not projectItem.device.sdCard:
		return
	
	srcPath                = project.path
	buildPath              = project.getDeviceBuildDir()
	SDCardFirmwareFileName = project.generateSDCardFirmwareFileName()
	webPagesPath           = os.path.join(srcPath, 'web/teplomonitor-server')
	
	if buildWebPages(webPagesPath):
		
		webPagesSrcFolder = 'dist'
	else:
		webPagesSrcFolder = 'server'
	
	firmwarePathOnSdCard = os.path.join(getSDCardFirmwarePath(project), 'firmware.bin')
	
	files = [
		SrcDestData(os.path.join(webPagesPath, webPagesSrcFolder), 'WEB/'),
		SrcDestData(os.path.join(webPagesPath, 'sitemenu.txt'), 'sitemenu.txt'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/', SDCardFirmwareFileName), firmwarePathOnSdCard)
	]
	
	name = project.name
	
	if ((name == 'DataLogger')    or
		(name == 'DataLoggerKSE') or
		(name == 'DataLoggerSW')):
		files.append(SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/langs.sd'), 'langs.sd'))
	elif name == 'disco':
		files.append(SrcDestData(os.path.join(srcPath, 'sdcard/Disco/GUI'), 'GUI/'))
	
	return files

def parseArguments(string_input, projects_array):
	args = string_input.split() #splits the input string on spaces
	
	production  = False
	build       = False
	pack_n_push = False
	clear       = False
	clearCache  = False
	flashLoader = False
	flashDevice = False
	simulator   = False
	runSimulator = False
	buildWithSpecialArgs = False
	projects_to_build = []
	
	for s in args:
		if s == '-e':
			print('Exit')
			sys.exit()
		if s == '-a': projects_to_build = projects_array
		if s == '-P': production  = True
		if s == '-b': build       = True
		if s == '-B': buildWithSpecialArgs = True
		if s == '-p': pack_n_push = True
		if s == '-c': clear       = True
		if s == '-C': clearCache  = True
		if s == '-f': flashLoader = True
		if s == '-F': flashDevice = True
		if s == '-s': simulator   = True
		if s == '-S':
			simulator    = True
			runSimulator = True
		for p in projects_array:
			if p.name == s or p.group == s:
				projects_to_build.append(p)
				continue
		
	return (
		production,
		build,
		pack_n_push,
		clear,
		clearCache,
		flashLoader,
		flashDevice,
		simulator,
		runSimulator,
		buildWithSpecialArgs,
		projects_to_build)

def createConfig(path):
	"""
	Create a config file
	"""
	
	configParserInstance.set('DEFAULT', 'projectDir', 'E:/development/SmartWeb_v1/')
	configParserInstance.set('DEFAULT', 'archiveDir', 'Z:/firmware/')
	configParserInstance.set('DEFAULT', 'pythonDir' , 'C:/Python/')
	configParserInstance.set('DEFAULT', 'sconsDir'  , 'C:/Python/Scripts/')
	configParserInstance.set('DEFAULT', 'openOcdDir', 'C:/OpenOCD/')
	configParserInstance.set('DEFAULT', 'sconsJobsNum', '8')
	configParserInstance.set('DEFAULT', 'scons_extra_args') # can be any string args, separated by ','
	
	configParserInstance.set('DEFAULT', 'programming_Adapter_Ftdi'         , 'yes')            # 'yes', 'no', 'true', 'false' 
	configParserInstance.set('DEFAULT', 'programming_Adapter_Serial_Number', 'OLUUKDU둭')       # 'OLUUKDU둭', 'OLYKF0UM' or 'OLZ4APP8' for known Olimex adapters
	configParserInstance.set('DEFAULT', 'programming_Adapter_VID_PID'      , '0x15BA 0x002A')  # '0x15BA 0x002A', '0x0403 0x6010' for known Olimex adapters
	configParserInstance.set('DEFAULT', 'programming_Adapter_Description'  , '"Olimex OpenOCD JTAG ARM-USB-TINY-H"')
	configParserInstance.set('DEFAULT', 'programming_Adapter_Interface'    , 'olimex-arm-usb-tiny-h.cfg')
	configParserInstance.set('DEFAULT', 'programming_Adapter_Transport'    , 'jtag') # 'jtag', 'swd' and so on
	
	projects_array = getAvailableProjectsList()
	for p in projects_array:
		configParserInstance.add_section(p.name)
	
	with open(path, "w", encoding='utf-8') as config_file:
		configParserInstance.write(config_file)

	return configParserInstance

def getSettingsFileParameterValue(projectName, parameter):
	configParserInstance.read(settingsPath)
	return configParserInstance.get(projectName, parameter)

def getSconsDir    (projectName): return getSettingsFileParameterValue(projectName, 'sconsDir')
def getPythonDir   (projectName): return getSettingsFileParameterValue(projectName, 'pythonDir')
def getOpenOcdDir  (projectName): return getSettingsFileParameterValue(projectName, 'openOcdDir')
def getProjectDir  (projectName): return getSettingsFileParameterValue(projectName, 'projectDir')
def getSconsJobsNum(projectName): return getSettingsFileParameterValue(projectName, 'sconsJobsNum')

def getSconsExtraArgs(projectName):
	args_str = getSettingsFileParameterValue(projectName, 'scons_extra_args')
	args_str = args_str.translate(str.maketrans('', '', ' \n\t\r'))
	return args_str.split(',')


def fixConsoleLang():
	subprocess.run([os.path.join('C:\Windows\system32','chcp.com'), '437'])

if __name__ == "__main__":
	
	fixConsoleLang()
	os.system('color')
	colorama.init()
		
	if not os.path.exists(settingsPath):
		createConfig(settingsPath)
	
	while True:
		projects_array = getAvailableProjectsList()
		printAvailableProjectsList(projects_array)
		
		try: input = raw_input
		except NameError: pass
		string_input = input(
			colored('Please enter projects to build (-a = All, -e = exit, -P = production and so on): ',
				'white',
				'on_green',
				attrs=['bold']))
		#TODO: add "real" console
		
		(
		production  ,
		build       ,
		pack_n_push ,
		clear       ,
		clearCache  ,
		flashLoader ,
		flashDevice ,
		simulator   ,
		runSimulator,
		buildWithSpecialArgs,
		projects_to_work_with) = parseArguments(string_input, projects_array)
		
		configParserInstance.read(settingsPath)
		
		print('Those projects will be used:')
		for p in projects_to_work_with:
			print(p.workingName)
			p.setPath(getProjectDir(p.name))
		
		for projectItem in projects_to_work_with:
			projectItem.production = production
			if clearCache: projectItem.clearSConsOptionsCacheFile()
			if simulator :
				projectItem.platform = 'qtsim'
				projectItem.target   = 'qtsim'
			if buildWithSpecialArgs :
				extraArgs = getSconsExtraArgs(p.name)

				result = projectItem.build(extraArgs)
				if result != 0:
					break
			else:
				if build     :
					result =  projectItem.build()
					if result != 0:
						break
			if runSimulator:
				projectItem.runSimulator()
			if flashLoader or flashDevice:
				Ftdi         = configParserInstance.getboolean(p.name, 'programming_Adapter_Ftdi')
				VID_PID      = configParserInstance.get       (p.name, 'programming_Adapter_VID_PID')
				SerialNumber = configParserInstance.get       (p.name, 'programming_Adapter_Serial_Number')
				Description  = configParserInstance.get       (p.name, 'programming_Adapter_Description')
				Interface    = configParserInstance.get       (p.name, 'programming_Adapter_Interface')
				Transport    = configParserInstance.get       (p.name, 'programming_Adapter_Transport')
				
				if flashLoader: projectItem.flashLoader(Ftdi, VID_PID, SerialNumber, Description, Interface, Transport)
				if flashDevice: projectItem.flashDevice(Ftdi, VID_PID, SerialNumber, Description, Interface, Transport)

			if pack_n_push:
				archiveDir = configParserInstance.get(p.name, 'archiveDir')
				
				if not os.path.exists(archiveDir):
					try:
						os.makedirs(archiveDir)
					except OSError as e:
						func.print_warning('Error %d: Can\'t create folder for archive dir at "%s"' %(e.errno, archiveDir))
						print('\r\n\n')
						break

				if projectItem.device.sdCard:
					projectItem.addSDCardData(getSDCardProjectFiles(projectItem))
					pack_project.do(projectItem)
				push_project_to_server.do(projectItem, archiveDir + projectItem.workingName + getProjectDestPathPostfix(projectItem))
			if clear: projectItem.clear()
		
		print(colored("Done", 'white', 'on_green'))
		print('\r\n\n')
		

