import pack_project, colorama

project_path = r'C:\development\xhcc'
projectName = 'DataLogger'
production = True
deviceName = 'DL'
board = 'L30'
boardVariant = ''
langkey = 'rom'

src_files_list = [
	r'C:\development\xhcc\web\teplomonitor-server\server',
	r'C:\development\xhcc\build\DataLogger_production\device\shared\platform\stm32\langs.sd',
	r'C:\development\xhcc\web\teplomonitor-server\sitemenu.txt',
	r'C:\development\xhcc\build\DataLogger_production\device\shared\platform\stm32\dlparams.sd',
	r'C:\development\xhcc\build\DataLogger_production\device\shared\platform\stm32\DL-Sorel-L30vr1-STM32-sdcard.bin',
]

dest_files_list = [
	'WEB/',
	'langs.sd',
	'sitemenu.txt',
	'dlparams.sd',
	'firmware.bin',
]

colorama.init()

pack_project.do(project_path, projectName, production, deviceName, board, boardVariant, langkey, src_files_list, dest_files_list)