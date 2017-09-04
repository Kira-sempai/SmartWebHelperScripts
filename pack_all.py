import pack_project, colorama, sys
sys.path.insert(0, "./scripts")
import func
from termcolor import colored

colorama.init()

default_project_path = 'C:/development/xhcc/'

production = True

project_postfix = '_production' if production else ''

def getBuildProjectPath(project):
	return project['project_path'] + 'build/' + project['projectName'] + '/device' + project['boardVariant'] + '/'

#=====================================#
datalogger     = dict(project_path = default_project_path, projectName = 'DataLogger' + project_postfix, deviceName = 'DL'      , board = 'L30'             , boardVariant =  '', langkey = 'rom',)
SmartWeb_X     = dict(project_path = default_project_path, projectName = 'xhcc'       + project_postfix, deviceName = 'XHCC'    , board = 'S61'             , boardVariant = '2', langkey = 'west',)
SmartWeb_X2    = dict(project_path = default_project_path, projectName = 'xhcc_s62'   + project_postfix, deviceName = 'XHCC-S62', board = 'S62'             , boardVariant = '2', langkey = 'west',)
SmartWeb_Disco = dict(project_path = default_project_path, projectName = 'disco'      + project_postfix, deviceName = 'DISCO'   , board = '32F746GDISCOVERY', boardVariant = '1', langkey = 'west',)

#=====================================#


project = datalogger

buildProjectPath = getBuildProjectPath(project)
SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(project)

project['src_files_list'] = [
	project['project_path'] + 'web/teplomonitor-server/server',
	project['project_path'] + 'web/teplomonitor-server/sitemenu.txt',
	buildProjectPath + 'shared/platform/stm32/langs.sd',
	buildProjectPath + 'shared/platform/stm32/dlparams.sd',
	buildProjectPath + 'shared/platform/stm32/' + SDCardFirmwareFileName,
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

for project in projects_array:
	print colored("Pack project: %s" % (project['projectName']), 'blue', 'on_green')
	pack_project.do(project)
