import os
import sys
from subprocess import Popen
import colorama
from termcolor import colored
sys.path.insert(0, "./scripts")
import func


def do(project):
	print colored("Clearing project: %s" % (func.getProjectDirName(project)), 'white', 'on_green', attrs=['bold'])
	
	p = Popen(
		[
			"scons.bat",
			project['project'],
			'CFG_PROJECT=' + project['projectName'],
			'CFG_PLATFORM=' + project['platform'],
			'CFG_PRODUCTION=' + project['production'],
			'--jobs=8',
			'-c',
		],
		cwd = project['project_path']
	)

	stdout, stderr = p.communicate()