# -*- coding: utf-8 -*-

import sys
import os
import datetime
import subprocess
from subprocess import Popen
import datetime
import argparse

sys.path.insert(0, "./scripts")


try: input = raw_input
except NameError: pass

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

settingsPath      = 'settings.ini'
addressToLineFile = 'addrToLine.txt'

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

def initParser():
	parser = argparse.ArgumentParser(
		description='Build SW projects, Flash them, pack n push project archives to server and so on.',
		epilog='If any questions - ask Andreyka'
		)
	
	parser.add_argument('projects', metavar='Project name', nargs='*', help='Project to work with')
	parser.add_argument('-e', '--exit'      , action='store_true', help = 'Exit script')
	parser.add_argument('-l', '--list'      , action='store_true', help = 'List of available projects')
	parser.add_argument('-a', '--all'       , action='store_true', help = 'Select all projects (not recommended)')
	parser.add_argument('-P', '--production', action='store_true', help = 'Use production version of the project')
	parser.add_argument('-b', '--build'     , action='store_true', help = 'Build project')
	parser.add_argument('-B', '--Build'     , action='store_true', help = 'Build project using args in ' + settingsPath + ' file')
	parser.add_argument('-p', '--pack'      , action='store_true', help = 'Pack builded project and store it in server')
	parser.add_argument('-x', '--size'      , action='store_true', help = 'Print project binary size in Flash and RAM')
	parser.add_argument('-c', '--clear'     , action='store_true', help = 'Clear project directory')
	parser.add_argument('-C', '--clearCache', action='store_true', help = 'Clear SCons options cache file (setup.py)')
	parser.add_argument('-f', '--floader'   , action='store_true', help = 'Flash controller loader')
	parser.add_argument('-F', '--fdevice'   , action='store_true', help = 'Flash controller application')
	parser.add_argument('-s', '--simulator' , action='store_true', help = 'Use simulator version of the project')
	parser.add_argument('-S', '--Simulator' , action='store_true', help = 'Use simulator version of the project and Run it at the end')
	parser.add_argument('-m', '--map'       , action='store_true', help = 'Show binary map. Amap program called')
	parser.add_argument('-r', '--reboot'    , action='store_true', help = 'Reboot controller')
	parser.add_argument('-R', '--readElfLine', action='store_true', help = 'Read address lines stored in ' + addressToLineFile + ' file')
	
	return parser


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

def main():
	fixConsoleLang()
	os.system('color')
	colorama.init()
	
	if not os.path.exists(settingsPath):
		createConfig(settingsPath)
	
	parser = initParser()
	
	projects_array = getAvailableProjectsList()
	
	while True:	
		string_input = input(
			colored('Please enter commands to execute: ',
				'white',
				'on_green',
				attrs=['bold']))
		
		args = parser.parse_args(string_input.split())
		
		if args.exit:
			print('Exit')
			sys.exit()
		
		projects_to_work_with = []
		for p in projects_array:
			if (p.name  in args.projects or
			    p.group in args.projects):
				projects_to_work_with.append(p)
		
		configParserInstance.read(settingsPath)
		
		if args.list:
			printAvailableProjectsList(projects_array)
		
		printProjectsToWorkWith(projects_to_work_with)
		
		for projectItem in projects_to_work_with:
			projectItem.setPath(getProjectDir(projectItem.name))
			projectItem.production = args.production
			
			if args.clearCache:
				projectItem.clearSConsOptionsCacheFile()
			
			if args.simulator or args.Simulator:
				projectItem.platform = 'qtsim'
				projectItem.target   = 'qtsim'
				
			if args.build or args.Build:
				result = buildProjectItem(projectItem, args.Build)
				
				if result != 0:
					break
			
			if args.size     : projectItem.getFirmwareSize()
			if args.map      : projectItem.showFirmwareMap()
			if args.Simulator: projectItem.runSimulator(getSimulatorArgs(projectItem.name))
			if args.floader  : loadFirmwareToLoaderFlash(projectItem)
			if args.fdevice  : loadFirmwareToAppFlash(projectItem)
			if args.reboot   : rebootDevice(projectItem)
			if args.clear    : projectItem.clear()
			if args.pack     :
				result = packAndPushProjectToArchive(projectItem)
				if result != 0:
					break
			
			if args.readElfLine:
				addrFile = addressToLineFile
				if not os.path.exists(addrFile):
					open(addrFile, 'w').close()
				print(projectItem.elfAddrToLine(addrFile))
			
		
		print(colored(str(datetime.datetime.now()) + " Done", 'white', 'on_green'))
		print('\r\n\n')
		

if __name__ == "__main__":
	main()
