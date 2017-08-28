import pack_project

project_path = r'C:\development\xhcc'
projectName = 'DataLogger'
production = True
deviceName = 'DL'
board = 'L30'
boardVariant = ''
src_files_list = [
	r'C:\development\xhcc\web\teplomonitor-server\server',
	r'C:\development\xhcc\build\DataLogger_production\device\shared\platform\stm32\langs.sd',
	r'C:\development\xhcc\web\teplomonitor-server\sitemenu.txt',
	r'C:\development\xhcc\build\DataLogger_production\device\shared\platform\stm32\dlparams.sd'
]

dest_files_list = [
	'WEB/',
	'langs.sd',
	'sitemenu.txt',
	'dlparams.sd',
]


pack_project.do(project_path, projectName, production, deviceName, board, boardVariant, src_files_list, dest_files_list)