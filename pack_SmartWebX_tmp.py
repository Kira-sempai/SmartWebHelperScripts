import pack_project, colorama, sys
sys.path.insert(0, "./scripts")
import func

project_path = r'C:/development/xhcc/'
production = True
projectName = 'xhcc'
deviceName = 'XHCC'
board = 'S61'
boardVariant = '2'
langkey = 'west'

projectTmpName = projectName + '_production' if production else projectName
buildProjectPath = project_path + 'build/' + projectTmpName + '/device' + boardVariant + '/'
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
	'update/' + SDCardFirmwareFileName,
#	SDCardFirmwareFileName,
]

colorama.init()

pack_project.do(project_path, projectName, production, deviceName, board, boardVariant, langkey, src_files_list, dest_files_list)