import sys
import os
import colorama
from termcolor import colored
sys.path.insert(0, "./scripts")
import func
import build_project
import pack_project
import push_project_to_server
import clear_project

import sd_card_files_DataLogger
import sd_card_files_SmartWeb_Disco
import sd_card_files_SmartWeb_X
import sd_card_files_SmartWeb_X2

colorama.init()

default_project_path = 'C:/development/xhcc/'

#=====================================#

DataLogger     = dict(project_path = default_project_path, project = 'device', projectName = 'DataLogger', workingName = 'DataLogger'    , platform = 'device', production = '1', deviceName = 'DL'      , board = 'L30'             , boardVariant =  '', langkey = 'rom',)
SmartWeb_Disco = dict(project_path = default_project_path, project = 'device', projectName = 'disco'     , workingName = 'SmartWeb Disco', platform = 'device', production = '1', deviceName = 'DISCO'   , board = '32F746GDISCOVERY', boardVariant = '1', langkey = 'west',)
SmartWeb_X     = dict(project_path = default_project_path, project = 'device', projectName = 'xhcc'      , workingName = 'SmartWeb X'    , platform = 'device', production = '1', deviceName = 'XHCC'    , board = 'S61'             , boardVariant = '2', langkey = 'west',)
SmartWeb_X2    = dict(project_path = default_project_path, project = 'device', projectName = 'xhcc_s62'  , workingName = 'SmartWeb X2'   , platform = 'device', production = '1', deviceName = 'XHCC-S62', board = 'S62'             , boardVariant = '2', langkey = 'west',)

#=====================================#

sd_card_files_DataLogger    .append(DataLogger)
sd_card_files_SmartWeb_Disco.append(SmartWeb_Disco)
sd_card_files_SmartWeb_X    .append(SmartWeb_X)
sd_card_files_SmartWeb_X2   .append(SmartWeb_X2)

#=====================================#

projects_array = [
	DataLogger,
	SmartWeb_Disco,
	SmartWeb_X,
	SmartWeb_X2,
]


serverDir = "Z:/firmware/"

for project in projects_array:
	build_project.do(project)
	pack_project.do(project)
	push_project_to_server.do(project, serverDir + project['workingName'])
#	clear_project.do(project)

