import build_project
import settings

projects = [
	'xhcc',
	'DataLogger',
	'xhcc_s62',
	'disco',
]

platform = 'device'
device = 'device'
production = '1'

for project in projects:
	build_project.do(settings.xhcc_dir_path, project, platform, device, production)
	print "\n\r\n\r"

input = raw_input("Press ENTER to continue")

