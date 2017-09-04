import os 
from subprocess import Popen


def do(project):
	print colored("Clearing project: %s" % (project['projectName']), 'white', 'on_green', attrs=['bold'])
	
	p = Popen(
		[
			"scons.bat",
			'CFG_PROJECT=' + project['project_name'],
			'CFG_PLATFORM=' + project['platform'],
			project['device'],
			'CFG_PRODUCTION=' + project['production'],
			'--jobs=8'
			'-c'
		],
		cwd = project['project_path']
	)

	stdout, stderr = p.communicate()