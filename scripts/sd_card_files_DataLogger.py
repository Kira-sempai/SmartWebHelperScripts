import func, os

def append(project):
	buildProjectPath = func.getDeviceBuildDir(project)
	SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(project)

	project['sd_card_src_files_list'] = [
		os.path.join(project['project_path'], 'web/teplomonitor-server/server'),
		os.path.join(project['project_path'], 'web/teplomonitor-server/sitemenu.txt'),
		os.path.join(buildProjectPath, 'shared/platform/stm32/langs.sd'),
		os.path.join(buildProjectPath, 'shared/platform/stm32/dlparams.sd'),
		os.path.join(buildProjectPath, 'shared/platform/stm32/', SDCardFirmwareFileName),
	]

	project['sd_card_dest_files_list'] = [
		'WEB/',
		'sitemenu.txt',
		'langs.sd',
		'dlparams.sd',
		'update/firmware.bin',
	]
