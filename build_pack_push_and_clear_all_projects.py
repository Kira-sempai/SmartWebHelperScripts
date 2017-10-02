import sys
import os
import colorama
from termcolor import colored
sys.path.insert(0, "./scripts")
import func
from project import Project, Device
from func import SrcDestData
import build_project
import pack_project
import push_project_to_server
import clear_project


def getProjectDestPathPostfix(project):
	return ' production' if project.production else ' debug'


if __name__ == "__main__":
	colorama.init()

	default_project_path = 'C:/development/xhcc/'
	default_project_path2 = 'C:/development/stdc_clean/'
	default_project_path3 = 'C:/development/ebielawski/'
	

	#=====================================#
	dataLogger     = Project(default_project_path, 'device', 'DataLogger', 'DataLogger'    , 'device', True, Device('DL'      , 'stm32', 'L30'             , None, True), 'rom' , 'old')
	smartWeb_Disco = Project(default_project_path, 'device', 'disco'     , 'SmartWeb Disco', 'device', True, Device('DISCO'   , 'stm32', '32F746GDISCOVERY',    1, True), 'west', 'old')
	smartWeb_X     = Project(default_project_path, 'device', 'xhcc'      , 'SmartWeb X'    , 'device', True, Device('XHCC'    , 'stm32', 'S61'             ,    2, True), 'west', 'old')
	smartWeb_X2    = Project(default_project_path, 'device', 'xhcc_s62'  , 'SmartWeb X2'   , 'device', True, Device('XHCC-S62', 'stm32', 'S62'             ,    2, True), 'west', 'old')

	smartWeb_S    = Project(default_project_path2, 'device', 'stdc'    , 'SmartWeb S' , 'device', True, Device('STDC'    , 'stm32', 'S20' , 3, False), 'west', 'old')
	smartWeb_L    = Project(default_project_path2, 'device', 'ltdc'    , 'SmartWeb L' , 'device', True, Device('LTDC'    , 'stm32', 'S40' , 3, False), 'west', 'old')
	smartWeb_L2   = Project(default_project_path2, 'device', 'ltdc_s45', 'SmartWeb L2', 'device', True, Device('LTDC_S45', 'stm32', 'S45' , 1, False), 'west', 'old')
	smartWeb_N    = Project(default_project_path2, 'device', 'swndin'  , 'SmartWeb N' , 'device', True, Device('SWNDIN'  , 'stm32', 'S41N', 1, False), 'west', 'old')
	
	caleon        = Project(default_project_path3, 'device', 'caleon_clima', 'Caleon', 'device', False, Device('caleon_clima', 'stm32n', 'RC40', None, False), 'rom', 'new')
	
	#=====================================#
	
	srcPath                = dataLogger.path
	buildPath              = dataLogger.getDeviceBuildDir()
	SDCardFirmwareFileName = dataLogger.generateSDCardFirmwareFileName()
	
	sdCardData = [
		SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/server')                , 'WEB/'),
		SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/sitemenu.txt')          , 'sitemenu.txt'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/langs.sd')                , 'langs.sd'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/dlparams.sd')             , 'dlparams.sd'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/', SDCardFirmwareFileName), 'firmware.bin')
	]
	
	dataLogger.addSDCardData(sdCardData)

	#=====================================#
	
	srcPath                = smartWeb_Disco.path
	buildPath              = smartWeb_Disco.getDeviceBuildDir()
	SDCardFirmwareFileName = smartWeb_Disco.generateSDCardFirmwareFileName()
	
	sdCardData = [
		SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/server')                , 'WEB/'),
		SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/sitemenu.txt')          , 'sitemenu.txt'),
		SrcDestData(os.path.join(srcPath  , 'sdcard/Disco/GUI')                              , 'GUI/'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/dlparams.sd')             , 'dlparams.sd'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/', SDCardFirmwareFileName), 'update/firmware.bin')
	]
		
	smartWeb_Disco.addSDCardData(sdCardData)
	#=====================================#
	
	srcPath                = smartWeb_X.path
	buildPath              = smartWeb_X.getDeviceBuildDir()
	SDCardFirmwareFileName = smartWeb_X.generateSDCardFirmwareFileName()
	
	sdCardData = [
		SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/server')                , 'WEB/'),
		SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/sitemenu.txt')          , 'sitemenu.txt'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/dlparams.sd')             , 'dlparams.sd'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/', SDCardFirmwareFileName), 'update/firmware.bin')
	]
		
	smartWeb_X.addSDCardData(sdCardData)
	#=====================================#
	
	srcPath                = smartWeb_X2.path
	buildPath              = smartWeb_X2.getDeviceBuildDir()
	SDCardFirmwareFileName = smartWeb_X2.generateSDCardFirmwareFileName()
	
	sdCardData = [
		SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/server')                , 'WEB/'),
		SrcDestData(os.path.join(srcPath  , 'web/teplomonitor-server/sitemenu.txt')          , 'sitemenu.txt'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/dlparams.sd')             , 'dlparams.sd'),
		SrcDestData(os.path.join(buildPath, 'shared/platform/stm32/', SDCardFirmwareFileName), 'update/firmware.bin')
	]
	
	smartWeb_X2.addSDCardData(sdCardData)
	
	#=====================================#
	
	
	projects_array = [
		dataLogger,
		smartWeb_Disco,
		smartWeb_X,
		smartWeb_X2,
		smartWeb_S,
		smartWeb_L,
		smartWeb_L2,
		smartWeb_N,
		caleon,
	]
	
	while True:
		print 'Projects list:'
		for p in projects_array:
			l = len(p.workingName)
			space = 20 - l
			print p.workingName, ' '*space, '- ', p.name
			
		
		string_input = raw_input('Please enter projects to build (a = All, e = exit): ')
		input_list = string_input.split() #splits the input string on spaces
		
		projects_to_build = []
		
		for s in input_list:
			if s == 'a':
				projects_to_build = projects_array
				break
			if s == 'e':
				Exit(1)
			for p in projects_array:
				if p.name == s:
					projects_to_build.extend([p])
					continue
		
		print 'Those projects will be build:'
		for p in projects_to_build:
			print p.workingName
		
		serverDir = "Z:/firmware/"
		
		for projectItem in projects_to_build:
			projectItem.build()
			pack_project.do(projectItem)
			push_project_to_server.do(projectItem, serverDir + projectItem.workingName + getProjectDestPathPostfix(projectItem))
		#	projectItem.clear()
		
        
		raw_input(colored("Done. Press ENTER to continue\r", 'white', 'on_green'))

