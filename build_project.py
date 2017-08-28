import os 
from subprocess import Popen


def do(project_path, project_name, platform, device, production):
	os.chdir(project_path)
	print os.getcwd()
	
	p = Popen(
		[
			"scons.bat",
			'CFG_PROJECT=' + project_name,
			'CFG_PLATFORM=' + platform,
			device,
			'CFG_PRODUCTION=' + production,
			'--jobs=8'
		]
	)

	stdout, stderr = p.communicate()