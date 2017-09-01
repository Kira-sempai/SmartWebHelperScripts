import pack_project, colorama, sys
sys.path.insert(0, "./scripts")
import func

project_path = r'C:/development/xhcc/'

#=====================================#
production = True
projectName = 'DataLogger'
deviceName = 'DL'
board = 'L30'
boardVariant = ''
langkey = 'rom'
#=====================================#

if production :
	projectName = projectName + '_production'


#=====================================#
buildProjectPath = project_path + 'build/' + projectName + '/device' + boardVariant + '/'
SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(deviceName, board, boardVariant, langkey)
src_files_list = [
	project_path + 'web/teplomonitor-server/server',
	project_path + 'web/teplomonitor-server/sitemenu.txt',
	buildProjectPath + 'shared/platform/stm32/langs.sd',
	buildProjectPath + 'shared/platform/stm32/dlparams.sd',
	buildProjectPath + 'shared/platform/stm32/' + SDCardFirmwareFileName,
]

dest_files_list = [
	'WEB/',
	'sitemenu.txt',
	'langs.sd',
	'dlparams.sd',
	'firmware.bin',
]
#=====================================#

colorama.init()

pack_project.do(project_path, projectName, deviceName, board, boardVariant, langkey, src_files_list, dest_files_list)
