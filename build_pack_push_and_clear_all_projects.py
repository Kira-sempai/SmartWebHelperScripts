# -*- coding: utf-8 -*-


try:
	import configparser
except ImportError:
	import ConfigParser as configparser

import sys
import os
import colorama
from subprocess import Popen
from termcolor import colored
sys.path.insert(0, "./scripts")
from project import Project, Device
from func import SrcDestData
import pack_project
import push_project_to_server


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
#		Project('SW2',            'DataLoggerCharlie', 'DataLogger Charlie', Device('DL_C'  , 'L30', None, True), 'rom'),
		
		Project('SW2', 'disco'       , 'SmartWeb Disco', Device('DISCO'   , '32F746GDISCOVERY',    1, True, 'stm32', 'stm32f4x.cfg')),
		Project('SW2', 'xhcc'        , 'SmartWeb X'    , Device('XHCC'    , 'S61'             ,    2, True, 'stm32', 'stm32f2x.cfg')),
		Project('SW2', 'xhcc_s62'    , 'SmartWeb X2'   , Device('XHCC-S62', 'S62'             ,    2, True, 'stm32', 'stm32f2x.cfg')),
		Project('SW2', 'swk'         , 'SmartWeb K'    , Device('SWK'     , 'SW-N2'           ,    1, True, 'stm32', 'stm32f2x.cfg'), 'west', 'old', False, 'OID_HLOGO'),
		
		Project('Caleon', 'caleon_clima', 'Caleon'        , Device('caleon_clima', 'RC40',    1, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'caleon_brv'  , 'Caleon BRV'    , Device('caleon_brv'  , 'RC50', None, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'domvs'       , 'Domvs'         , Device('Domvs'       , 'RC40', None, False, 'stm32n'), 'rom', 'new'),
		Project('Other',  'caleon_clima_smart_web_controller', 'Caleon SW', Device('caleon_clima_smart_web_controller', 'RC50', None, False, 'stm32n'), 'rom', 'new'),
		
		Project('Other', 'lfwc'                 , 'LFWC'              , Device('LFWC'       , 'S40', None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_v01'          , 'LFWC'              , Device('LFWC-MT-V01', 'S40', None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_v02'          , 'LFWC'              , Device('LFWC-MT-V02', 'S40', None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_s47'          , 'LFWC'              , Device('LFWC-MT-S47', 'S47', None, False, 'stm32'), 'rom'),
		Project('Other', 'lfwc_mt_s47_unitTest' , 'LFWC Unit Test'    , Device('LFWC-MT-S47', 'S47', None, False, 'stm32'), 'rom'),
		Project('Other', 'charlie'              , 'CHARLIE'           , Device('CHARLIE'    , 'S48',    1, False, 'stm32'), 'rom', 'old', False, 'OID_Kemper'),
		Project('Other', 'charlie_unitTest'     , 'CHARLIE Unit Test' , Device('CHARLIE'    , 'S48',    1, False, 'stm32'), 'rom', 'old', False, 'OID_Kemper'),

		Project('Other', 'DataLoggerCharlie'         , 'DataLogger Charlie'          , Device('DataLoggerCharlie' , 'L30', None, False, 'stm32'), 'rom', 'old', False, 'OID_SOREL'),
		Project('Other', 'DataLoggerCharlie_unitTest', 'DataLogger Charlie Unit Test', Device('DataLoggerCharlie' , 'L30', None, False, 'stm32'), 'rom', 'old', False, 'OID_SOREL'),
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
	programmingAdapterSerialNumber = None
	programmingAdapterVID_PID = None
	programmingAdapterDescription = None
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
		if s.count('--adapter_serial'):
			programmingAdapterSerialNumber = s[17:]
			if	programmingAdapterSerialNumber == '1':
				programmingAdapterSerialNumber = 'OLUUKDU둭'
		if s.count('--adapter_vid_pid'):
			programmingAdapterVID_PID = s[18:]
			if  programmingAdapterVID_PID == '1':
				programmingAdapterVID_PID = '0x15BA 0x002A'
			elif programmingAdapterVID_PID == '2':
				programmingAdapterVID_PID = '0x0403 0x6010'
		if s.count('--adapter_description'):
			programmingAdapterDescription  = s[22:23]
			if  programmingAdapterDescription == '1':
				programmingAdapterDescription = '"Olimex OpenOCD JTAG ARM-USB-TINY-H"'
			if  programmingAdapterDescription == '2':
				programmingAdapterDescription = '"Dual RS232-HS"'
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
		programmingAdapterSerialNumber,
		programmingAdapterVID_PID,
		programmingAdapterDescription,
		projects_to_build)

def createConfig(path):
	"""
	Create a config file
	"""
	config = configparser.ConfigParser()
	
	projects_array = getAvailableProjectsList()
	
	config.set('DEFAULT', 'path', 'E:/development/SmartWeb_v1/')
	
	for p in projects_array:
		config.add_section(p.name)
	
	
	with open(path, "w") as config_file:
		config.write(config_file)

	return config

if __name__ == "__main__":
	colorama.init()
	
	path = "settings.ini"
	
	if not os.path.exists(path):
		createConfig(path)
	
	config = configparser.ConfigParser()
	config.read(path)
	
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
		programmingAdapterSerialNumber,
		programmingAdapterVID_PID,
		programmingAdapterDescription,
		projects_to_work_with) = parseArguments(string_input, projects_array)
		
		
		print('Those projects will be used:')
		for p in projects_to_work_with:
			print(p.workingName)
			p.setPath(config.get(p.name, 'path'))
		
		
		for projectItem in projects_to_work_with:
			projectItem.production = production
			if clearCache: projectItem.clearSConsOptionsCacheFile()
			if simulator :
				projectItem.platform = 'qtsim'
				projectItem.target   = 'qtsim'
			if buildWithSpecialArgs :
				extraArgs = []
				extraArgsFile = 'setup.py'
				if os.path.isfile(extraArgsFile):
					for line in open(extraArgsFile, 'r'):
						extraArgs.append(line.rstrip())

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
			if flashLoader : projectItem.flashLoader(programmingAdapterVID_PID, programmingAdapterSerialNumber, programmingAdapterDescription)
			if flashDevice : projectItem.flashDevice(programmingAdapterVID_PID, programmingAdapterSerialNumber, programmingAdapterDescription)
			if pack_n_push:
				serverDir = "Z:/firmware/"
				
				if not os.path.exists(serverDir):
					print(colored("Can't find server: " + serverDir, 'white', 'on_red'))
					print('\r\n\n')
					break
					
				if projectItem.device.sdCard:
					projectItem.addSDCardData(getSDCardProjectFiles(projectItem))
					pack_project.do(projectItem)
				push_project_to_server.do(projectItem, serverDir + projectItem.workingName + getProjectDestPathPostfix(projectItem))
			if clear: projectItem.clear()
		
		print(colored("Done", 'white', 'on_green'))
		print('\r\n\n')
		

