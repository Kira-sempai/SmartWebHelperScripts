import sys
import os
import colorama
from termcolor import colored
sys.path.insert(0, "./scripts")
import func
import build_project
import pack_project

colorama.init()

default_project_path = 'C:/development/xhcc/'

def getBuildProjectPath(project):
	return os.path.join(project['project_path'], 'build', project['projectName'], project['project'] + project['boardVariant'])

#=====================================#
datalogger     = dict(project_path = default_project_path, project = 'device', projectName = 'DataLogger', platform = 'device', production = '1', deviceName = 'DL'      , board = 'L30'             , boardVariant =  '', langkey = 'rom',)
SmartWeb_X     = dict(project_path = default_project_path, project = 'device', projectName = 'xhcc'      , platform = 'device', production = '1', deviceName = 'XHCC'    , board = 'S61'             , boardVariant = '2', langkey = 'west',)
SmartWeb_X2    = dict(project_path = default_project_path, project = 'device', projectName = 'xhcc_s62'  , platform = 'device', production = '1', deviceName = 'XHCC-S62', board = 'S62'             , boardVariant = '2', langkey = 'west',)
SmartWeb_Disco = dict(project_path = default_project_path, project = 'device', projectName = 'disco'     , platform = 'device', production = '1', deviceName = 'DISCO'   , board = '32F746GDISCOVERY', boardVariant = '1', langkey = 'west',)

#=====================================#


project = datalogger

buildProjectPath = getBuildProjectPath(project)
SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(project)

project['src_files_list'] = [
	os.path.join(project['project_path'], 'web/teplomonitor-server/server'),
	os.path.join(project['project_path'], 'web/teplomonitor-server/sitemenu.txt'),
	os.path.join(buildProjectPath, 'shared/platform/stm32/langs.sd'),
	os.path.join(buildProjectPath, 'shared/platform/stm32/dlparams.sd'),
	os.path.join(buildProjectPath, 'shared/platform/stm32/' + SDCardFirmwareFileName),
]

project['dest_files_list'] = [
	'WEB/',
	'sitemenu.txt',
	'langs.sd',
	'dlparams.sd',
	'firmware.bin',
]

#=====================================#
project = SmartWeb_X

buildProjectPath = getBuildProjectPath(project)
SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(project)

project['src_files_list'] = [
	project['project_path'] + 'web/teplomonitor-server/server',
	project['project_path'] + 'web/teplomonitor-server/sitemenu.txt',
	buildProjectPath + 'shared/platform/stm32/dlparams.sd',
	buildProjectPath + 'shared/platform/stm32/' + SDCardFirmwareFileName,
]

project['dest_files_list'] = [
	'WEB/',
	'sitemenu.txt',
	'dlparams.sd',
	'update/firmware.bin',
]

#=====================================#
project = SmartWeb_X2

buildProjectPath = getBuildProjectPath(project)
SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(project)

project['src_files_list'] = [
	project['project_path'] + 'web/teplomonitor-server/server',
	project['project_path'] + 'web/teplomonitor-server/sitemenu.txt',
	buildProjectPath + 'shared/platform/stm32/dlparams.sd',
	buildProjectPath + 'shared/platform/stm32/' + SDCardFirmwareFileName,
]

project['dest_files_list'] = [
	'WEB/',
	'sitemenu.txt',
	'dlparams.sd',
	'update/firmware.bin',
]
#=====================================#

project = SmartWeb_Disco

buildProjectPath = getBuildProjectPath(project)
SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(project)

project['src_files_list'] = [
	project['project_path'] + 'web/teplomonitor-server/server',
	project['project_path'] + 'web/teplomonitor-server/sitemenu.txt',
	buildProjectPath + 'shared/platform/stm32/dlparams.sd',
	buildProjectPath + 'shared/platform/stm32/' + SDCardFirmwareFileName,
]

project['dest_files_list'] = [
	'WEB/',
	'sitemenu.txt',
	'dlparams.sd',
	'update/firmware.bin',
]
#=====================================#

projects_array = [datalogger, SmartWeb_X, SmartWeb_X2, SmartWeb_Disco]

serverDir = "Z:/firmware"

for project in projects_array:
	build_project.do(project)
	pack_project.do(project)
	push_project_to_server(project, serverDir)
	clear_project.do(project)

