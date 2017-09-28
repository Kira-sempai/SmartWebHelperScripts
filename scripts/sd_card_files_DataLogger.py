import func, os
from func import SDCardData

buildProjectPath = func.getDeviceBuildDir(project)
SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(project)

src = [
	os.path.join(project['project_path'], 'web/teplomonitor-server/server'),
	os.path.join(project['project_path'], 'web/teplomonitor-server/sitemenu.txt'),
	os.path.join(buildProjectPath, 'shared/platform/stm32/langs.sd'),
	os.path.join(buildProjectPath, 'shared/platform/stm32/dlparams.sd'),
	os.path.join(buildProjectPath, 'shared/platform/stm32/', SDCardFirmwareFileName),
]

dest = [
	'WEB/',
	'sitemenu.txt',
	'langs.sd',
	'dlparams.sd',
	'firmware.bin',
]
