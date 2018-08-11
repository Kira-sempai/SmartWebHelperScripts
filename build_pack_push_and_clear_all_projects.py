# -*- coding: utf-8 -*-
import sys
import os
import colorama
from termcolor import colored
sys.path.insert(0, "./scripts")
from project import Project, Device
from func import SrcDestData
import pack_project
import push_project_to_server


def getProjectDestPathPostfix(project):
	return ' production' if project.production else ' debug'

def printAvailableProjectsList(projects_array):
	print 'Projects list:'
	for p in projects_array:
		l = len(p.workingName)
		space = 20 - l
		print p.workingName, ' '*space, '- ', p.name

def getAvailableProjectsList():
	default_project_path1 = 'E:/development/SmartWeb_v1/'
	default_project_path2 = 'E:/development/SmartWeb_v2/'
	default_project_path3 = 'E:/development/Caleon_clima/'
	default_project_path4 = 'E:/development/Caleon_brv/'
	default_project_path5 = 'E:/development/pdellwig/'
	
	return [
		Project(default_project_path1, 'device', 'stdc'        , 'SmartWeb S'    , 'device', Device('STDC'    , 'S20' , 3), 'rom'),
		Project(default_project_path1, 'device', 'stdc_lin'    , 'SmartWeb S LIN', 'device', Device('STDC_LIN', 'S28' , 3), 'rom'),
		Project(default_project_path1, 'device', 'ltdc'        , 'SmartWeb L'    , 'device', Device('LTDC'    , 'S40' , 3), 'rom'),
		Project(default_project_path1, 'device', 'ltdc_s45'    , 'SmartWeb L2'   , 'device', Device('LTDC_S45', 'S45' , 1), 'rom'),
		Project(default_project_path1, 'device', 'swndin'      , 'SmartWeb N'    , 'device', Device('SWNDIN'  , 'S41N', 1), 'rom'),
		
		Project(default_project_path2, 'device', 'DataLogger'   , 'DataLogger'    , 'device', Device('DL'    , 'L30', None, True), 'rom'),
		Project(default_project_path2, 'device', 'DataLoggerSW' , 'DataLogger SW' , 'device', Device('DL_SW' , 'L30', None, True), 'rom'),
		Project(default_project_path2, 'device', 'DataLoggerKSE', 'DataLogger KSE', 'device', Device('DL_KSE', 'L30', None, True), 'rom'),
		
		Project(default_project_path2, 'device', 'disco'       , 'SmartWeb Disco', 'device', Device('DISCO'   , '32F746GDISCOVERY',    1, True, 'stm32', 'stm32f4x.cfg')),
		Project(default_project_path2, 'device', 'xhcc'        , 'SmartWeb X'    , 'device', Device('XHCC'    , 'S61'             ,    2, True, 'stm32', 'stm32f2x.cfg')),
		Project(default_project_path2, 'device', 'xhcc_s62'    , 'SmartWeb X2'   , 'device', Device('XHCC-S62', 'S62'             ,    2, True, 'stm32', 'stm32f2x.cfg')),
		Project(default_project_path2, 'device', 'swk'         , 'SmartWeb K'    , 'device', Device('SWK'     , 'SW-N2'           ,    1, True, 'stm32', 'stm32f2x.cfg'), 'west', 'old', False, 'OID_HLOGO'),
		
		Project(default_project_path3, 'device', 'caleon_clima', 'Caleon'        , 'device', Device('caleon_clima', 'RC40',    1, False, 'stm32n'), 'rom', 'new'),
		Project(default_project_path4, 'device', 'caleon_brv'  , 'Caleon BRV'    , 'device', Device('caleon_brv'  , 'RC50', None, False, 'stm32n'), 'rom', 'new'),
		Project(default_project_path4, 'device', 'domus'       , 'Domus'         , 'device', Device('Domus'       , 'RC50', None, False, 'stm32n'), 'rom', 'new'),
		
		Project(default_project_path5, 'device', 'lfwc'        , 'LFWC', 'device', Device('LFWC'       , 'S40', None, False, 'stm32'), 'rom'),
		Project(default_project_path5, 'device', 'lfwc_mt_v01' , 'LFWC', 'device', Device('LFWC-MT-V01', 'S40', None, False, 'stm32'), 'rom'),
		Project(default_project_path5, 'device', 'lfwc_mt_v02' , 'LFWC', 'device', Device('LFWC-MT-V02', 'S40', None, False, 'stm32'), 'rom'),
	]

def getSDCardProjectFiles(project):
	srcPath                = project.path
	buildPath              = project.getDeviceBuildDir()
	SDCardFirmwareFileName = project.generateSDCardFirmwareFileName()
	
	if  ((project.name == 'DataLogger')   or
		(project.name == 'DataLoggerKSE') or
		(project.name == 'DataLoggerSW')):
		return [
			SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/server')                , 'WEB/'),
			SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/sitemenu.txt')          , 'sitemenu.txt'),
			SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/langs.sd')                , 'langs.sd'),
			SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/', SDCardFirmwareFileName), 'firmware.bin')
		]
	elif project.name == 'disco':
		return [
			SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/server')                , 'WEB/'),
			SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/sitemenu.txt')          , 'sitemenu.txt'),
			SrcDestData(os.path.join(srcPath  , 'sdcard/Disco/GUI')                              , 'GUI/'),
			SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/', SDCardFirmwareFileName), 'update/firmware.bin')
		]
	elif ((project.name == 'xhcc') or
		(project.name == 'xhcc_s62') or
		(project.name == 'swk')):
		return [
			SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/server')                , 'WEB/'),
			SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/sitemenu.txt')          , 'sitemenu.txt'),
			SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/', SDCardFirmwareFileName), 'update/firmware.bin')
		]

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
	buildWithSpecialArgs = False
	programmingAdapterSerialNumber = None
	programmingAdapterVID_PID = None
	programmingAdapterDescription = None
	projects_to_build = []
	
	for s in args:
		if s == '-e':
			print 'Exit'
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
			if p.name == s:
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
		buildWithSpecialArgs,
		programmingAdapterSerialNumber,
		programmingAdapterVID_PID,
		programmingAdapterDescription,
		projects_to_build)

if __name__ == "__main__":
	colorama.init()
	
	while True:
		projects_array = getAvailableProjectsList()
		printAvailableProjectsList(projects_array)
		
		string_input = raw_input(
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
		buildWithSpecialArgs,
		programmingAdapterSerialNumber,
		programmingAdapterVID_PID,
		programmingAdapterDescription,
		projects_to_build) = parseArguments(string_input, projects_array)
		
		
		print 'Those projects will be used:'
		for p in projects_to_build:
			print p.workingName
		
		
		for projectItem in projects_to_build:
			projectItem.production = production
			if clearCache: projectItem.clearSConsOptionsCacheFile()
			if simulator :
				projectItem.command = 'qtsim'
				projectItem.platform = 'qtsim'
			if buildWithSpecialArgs :
				extraArgs = []
				extraArgsFile = 'setup.py'
				if os.path.isfile(extraArgsFile):
					for line in open(extraArgsFile, 'r'):
						extraArgs.append(line.rstrip())

				projectItem.build(extraArgs)
			else:
				if build     : projectItem.build()
			if flashLoader : projectItem.flashLoader(programmingAdapterVID_PID, programmingAdapterSerialNumber, programmingAdapterDescription)
			if flashDevice : projectItem.flashDevice(programmingAdapterVID_PID, programmingAdapterSerialNumber, programmingAdapterDescription)
			if pack_n_push:
				serverDir = "Z:/firmware/"
				if projectItem.device.sdCard:
					projectItem.addSDCardData(getSDCardProjectFiles(projectItem))
					pack_project.do(projectItem)
				push_project_to_server.do(projectItem, serverDir + projectItem.workingName + getProjectDestPathPostfix(projectItem))
			if clear: projectItem.clear()
		
		print(colored("Done", 'white', 'on_green'))
		print '\r\n\n'
		

