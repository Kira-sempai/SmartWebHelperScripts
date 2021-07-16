# -*- coding: utf-8 -*-

import sys
import os
import datetime
import subprocess
from subprocess import Popen
import datetime

sys.path.insert(0, "./scripts")

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
	import termcolor
	from termcolor import colored
except ImportError:
	from scripts import termcolor
	print('termcolor is missing: use "pip install termcolor" to add it to Python')

import scripts.func
from scripts.func import SrcDestData
from scripts.project import Project, Device
import pack_project
import push_project_to_server

from projectsList import getAvailableProjectsList

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

def projectWithCodeOnSdCard(project):
	name = project.name
	return ((name == 'DataLogger'   ) or
			(name == 'DataLoggerKSE') or
			(name == 'DataLoggerSW' ))
		
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
	platformPath = os.path.join(buildPath, 'shared/platform/stm32/')
	files = [
		SrcDestData(os.path.join(webPagesPath, webPagesSrcFolder), 'WEB/'),
		SrcDestData(os.path.join(webPagesPath, 'sitemenu.txt'), 'sitemenu.txt'),
		SrcDestData(os.path.join(platformPath, SDCardFirmwareFileName), firmwarePathOnSdCard)
	]
	
	name = project.name
	
	if projectWithCodeOnSdCard(project):
		extraFiles = [
			os.path.join(platformPath, 'langs.sd'),
			os.path.join(platformPath, 'dlparams.sd'),
		]
		for extraFile in extraFiles:
			if os.path.exists(extraFile):
				head, tail = os.path.split(extraFile)
				files.append(SrcDestData(extraFile, tail))
				
	if name == 'disco':
		files.append(SrcDestData(os.path.join(srcPath, 'sdcard/Disco/GUI'), 'GUI/'))
	
	return files

def parseArguments(string_input, projects_array):
	args = string_input.split() #splits the input string on spaces
	
	projects_to_build = []
	
	parsedArgs = {}
	
	for s in args:
		if s == '-e':
			print('Exit')
			sys.exit()
		if s == '-l': parsedArgs['show_projects_list'] = True; continue
		if s == '-a': parsedArgs['projects_to_build'] = projects_array; continue
		if s == '-P': parsedArgs['production']  = True; continue
		if s == '-b': parsedArgs['build']       = True; continue
		if s == '-B': 
					parsedArgs['build']       = True
					parsedArgs['buildWithSpecialArgs'] = True
					continue
		if s == '-p': parsedArgs['pack_n_push'] = True; continue
		if s == '-x': parsedArgs['printSize']   = True; continue
		if s == '-c': parsedArgs['clear']       = True; continue
		if s == '-C': parsedArgs['clearCache']  = True; continue
		if s == '-f': parsedArgs['flashLoader'] = True; continue
		if s == '-F': parsedArgs['flashDevice'] = True; continue
		if s == '-s': parsedArgs['simulator']   = True; continue
		if s == '-m': parsedArgs['showFwMap']   = True; continue
		if s == '-r': parsedArgs['reboot']      = True; continue
		if s == '-S':
			parsedArgs['simulator']    = True
			parsedArgs['runSimulator'] = True
			continue
		
		if s == '--rel': parsedArgs['readElfLine'] = True; continue
		
		for p in projects_array:
			if p.name == s or p.group == s:
				projects_to_build.append(p)
				continue
		
	return (parsedArgs, projects_to_build)

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
	configParserInstance.set('DEFAULT', 'simulator_args') # can be any string
	
	configParserInstance.set('DEFAULT', 'programming_Adapter_Ftdi'         , 'yes')            # 'yes', 'no', 'true', 'false' 
	configParserInstance.set('DEFAULT', 'programming_Adapter_Serial_Number', 'OLUUKDU둭')       # 'OLUUKDU둭', 'OLYKF0UM' or 'OLZ4APP8' for known Olimex adapters
	configParserInstance.set('DEFAULT', 'programming_Adapter_VID_PID'      , '0x15BA 0x002A')  # '0x15BA 0x002A', '0x0403 0x6010' for known Olimex adapters
	configParserInstance.set('DEFAULT', 'programming_Adapter_Description'  , '"Olimex OpenOCD JTAG ARM-USB-TINY-H"')
	configParserInstance.set('DEFAULT', 'programming_Adapter_Interface'    , 'olimex-arm-usb-tiny-h.cfg')
	configParserInstance.set('DEFAULT', 'programming_Adapter_Transport'    , 'jtag') # 'jtag', 'swd' and so on
	configParserInstance.set('DEFAULT', 'programming_Adapter_speed'        , '4000') # 4000kHz
	
	projects_array = getAvailableProjectsList()
	for p in projects_array:
		configParserInstance.add_section(p.name)
	
	with open(path, "w", encoding='utf-8') as config_file:
		configParserInstance.write(config_file)

	return configParserInstance

def getSettingsFileParameterValue(projectName, parameter):
	configParserInstance.read(settingsPath)

	if not configParserInstance.has_section(projectName):
		configParserInstance.add_section(projectName)
		with open(settingsPath, "w", encoding='utf-8') as config_file:
			configParserInstance.write(config_file)
	
	return configParserInstance.get(projectName, parameter)

def getSconsDir     (projectName): return getSettingsFileParameterValue(projectName, 'sconsDir')
def getPythonDir    (projectName): return getSettingsFileParameterValue(projectName, 'pythonDir')
def getOpenOcdDir   (projectName): return getSettingsFileParameterValue(projectName, 'openOcdDir')
def getProjectDir   (projectName): return getSettingsFileParameterValue(projectName, 'projectDir')
def getSconsJobsNum (projectName): return getSettingsFileParameterValue(projectName, 'sconsJobsNum')
def getSimulatorArgs(projectName): return getSettingsFileParameterValue(projectName, 'simulator_args')

def getSconsExtraArgs(projectName):
	args_str = getSettingsFileParameterValue(projectName, 'scons_extra_args')
#	args_str = args_str.translate(str.maketrans('', '', ' \n\t\r'))
	return args_str.split(', ')

def printProjectsToWorkWith(projects_to_work_with):
	print('Those projects will be used:')
	for projectItem in projects_to_work_with:
		print(projectItem.workingName)

def fixConsoleLang():
	subprocess.run([os.path.join('C:\Windows\system32','chcp.com'), '437'])

def buildProjectItem(projectItem, buildWithSpecialArgs):
	extraArgs = []
	if buildWithSpecialArgs :
		extraArgs = getSconsExtraArgs(projectItem.name)
		
	start   = datetime.datetime.now()
	result  = projectItem.build(extraArgs)
	stop    = datetime.datetime.now()
	elapsed = stop - start
	
	print('Build time: %s seconds' % elapsed.seconds)
	
	return result
	
def getProjectAdapter(projectItem):
	return {
		'Ftdi'         : configParserInstance.getboolean(projectItem.name, 'programming_Adapter_Ftdi'),
		'VID_PID'      : configParserInstance.get       (projectItem.name, 'programming_Adapter_VID_PID'),
		'SerialNumber' : configParserInstance.get       (projectItem.name, 'programming_Adapter_Serial_Number'),
		'Description'  : configParserInstance.get       (projectItem.name, 'programming_Adapter_Description'),
		'Interface'    : configParserInstance.get       (projectItem.name, 'programming_Adapter_Interface'),
		'Transport'    : configParserInstance.get       (projectItem.name, 'programming_Adapter_Transport'),
		'Speed'        : configParserInstance.get       (projectItem.name, 'programming_Adapter_speed'),
	}
	
def loadFirmwareToLoaderFlash(projectItem):
	adapter = getProjectAdapter(projectItem)
	projectItem.flashLoader(adapter)
	
def loadFirmwareToAppFlash(projectItem):
	adapter = getProjectAdapter(projectItem)
	projectItem.flashDevice(adapter)

def rebootDevice(projectItem):
	adapter = getProjectAdapter(projectItem)
	projectItem.rebootDevice(adapter)
	

def packAndPushProjectToArchive(projectItem):
	archiveDir = configParserInstance.get(projectItem.name, 'archiveDir')
	
	if not os.path.exists(archiveDir):
		try:
			os.makedirs(archiveDir)
		except OSError as e:
			func.print_warning('Error %d: Can\'t create folder for archive dir at "%s"' %(e.errno, archiveDir))
			print('\r\n\n')
			return 1

	if projectItem.device.sdCard:
		projectItem.addSDCardData(getSDCardProjectFiles(projectItem))
		pack_project.do(projectItem)
	push_project_to_server.do(projectItem, archiveDir + projectItem.workingName + getProjectDestPathPostfix(projectItem))
	
	return 0

if __name__ == "__main__":
	
	fixConsoleLang()
	os.system('color')
	colorama.init()
	
	if not os.path.exists(settingsPath):
		createConfig(settingsPath)
	
	while True:
		projects_array = getAvailableProjectsList()
		
		try: input = raw_input
		except NameError: pass
		string_input = input(
			colored('Please enter projects to build (-a = All, -e = exit, -P = production and so on): ',
				'white',
				'on_green',
				attrs=['bold']))
		#TODO: add "real" console
		
		(parsedArgs, projects_to_work_with) = parseArguments(string_input, projects_array)
		
		configParserInstance.read(settingsPath)
		
		if 'show_projects_list' in parsedArgs:
			printAvailableProjectsList(projects_array)
		
		printProjectsToWorkWith(projects_to_work_with)
		
		for projectItem in projects_to_work_with:
			projectItem.setPath(getProjectDir(projectItem.name))
			projectItem.production = 'production' in parsedArgs
			
			if 'clearCache' in parsedArgs:
				projectItem.clearSConsOptionsCacheFile()
			
			if 'simulator' in parsedArgs:
				projectItem.platform = 'qtsim'
				projectItem.target   = 'qtsim'
				
			if 'build' in parsedArgs:
				result = buildProjectItem(projectItem, 'buildWithSpecialArgs' in parsedArgs)
				
				if result != 0:
					break
			
			if 'printSize'    in parsedArgs: projectItem.getFirmwareSize()
			if 'showFwMap'    in parsedArgs: projectItem.showFirmwareMap()
			if 'runSimulator' in parsedArgs: projectItem.runSimulator(getSimulatorArgs(projectItem.name))
			if 'flashLoader'  in parsedArgs: loadFirmwareToLoaderFlash(projectItem)
			if 'flashDevice'  in parsedArgs: loadFirmwareToAppFlash(projectItem)
			if 'reboot'       in parsedArgs: rebootDevice(projectItem)
			if 'clear'        in parsedArgs: projectItem.clear()
			if 'pack_n_push'  in parsedArgs:
				result = packAndPushProjectToArchive(projectItem)
				if result != 0:
					break
			
			if 'readElfLine' in parsedArgs:
				addrFile = 'addrToLine.txt'
				if not os.path.exists(addrFile):
					open(addrFile, 'w').close()
				print(projectItem.elfAddrToLine(addrFile))
			
		
		print(colored(str(datetime.datetime.now()) + " Done", 'white', 'on_green'))
		print('\r\n\n')
		

