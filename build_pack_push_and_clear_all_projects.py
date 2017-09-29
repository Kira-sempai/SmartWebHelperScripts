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


colorama.init()

def getProjectDestPathPostfix(project):
	return ' production' if project.production else ' debug'


if __name__ == "__main__":
	default_project_path = 'C:/development/xhcc/'
	default_project_path2 = 'C:/development/stdc_clean/'
	
    
	#=====================================#
	dataLogger     = Project(default_project_path, 'device', 'DataLogger', 'DataLogger'    , 'device', True, Device('DL'      , 'L30'             , None, True), 'rom')
	smartWeb_Disco = Project(default_project_path, 'device', 'disco'     , 'SmartWeb Disco', 'device', True, Device('DISCO'   , '32F746GDISCOVERY',    1, True), 'west')
	smartWeb_X     = Project(default_project_path, 'device', 'xhcc'      , 'SmartWeb X'    , 'device', True, Device('XHCC'    , 'S61'             ,    2, True), 'west')
	smartWeb_X2    = Project(default_project_path, 'device', 'xhcc_s62'  , 'SmartWeb X2'   , 'device', True, Device('XHCC-S62', 'S62'             ,    2, True), 'west')
	
#    SmartWeb_S  = dict(project_path = default_project_path2, project = 'device', projectName = 'stdc'    , workingName = 'SmartWeb S' , platform = 'device', production = '1', deviceName = 'STDC'    , board = 'S20', boardVariant = '3', langkey = 'west',)
#   SmartWeb_L  = dict(project_path = default_project_path2, project = 'device', projectName = 'ltdc'    , workingName = 'SmartWeb L' , platform = 'device', production = '1', deviceName = 'LTDC'    , board = 'S40', boardVariant = '3', langkey = 'west',)
#	SmartWeb_L2 = dict(project_path = default_project_path2, project = 'device', projectName = 'ltdc_s45', workingName = 'SmartWeb L2', platform = 'device', production = '1', deviceName = 'LTDC_S45', board = 'S45', boardVariant = '3', langkey = 'west',)
#	SmartWeb_N  = dict(project_path = default_project_path2, project = 'device', projectName = 'swndin'  , workingName = 'SmartWeb N' , platform = 'device', production = '1', deviceName = 'SWNDIN'  , board = 'S41N', boardVariant = '1', langkey = 'west',)
	
    
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
	]
	
#	projects_array2 = [
#		SmartWeb_S,
#		SmartWeb_L,
#		SmartWeb_L2,
#   	SmartWeb_N,
#    ]
	
	serverDir = "Z:/firmware/"
	
	for projectItem in projects_array:
		projectItem.build()
		pack_project.do(projectItem)
		push_project_to_server.do(projectItem, serverDir + projectItem.name + getProjectDestPathPostfix(projectItem))
	#	projectItem.clear()
	
	#for project in projects_array2:
	#	build_project.do(project)
    
    