import os, shutil, sys
sys.path.insert(0, "./scripts")
import func
from subprocess import Popen
from termcolor import colored

WarningList = []

def print_warning(warning):
	warning = colored(warning, 'white', 'on_red')
	print warning
	WarningList.append(warning)
	input = raw_input(colored("Press ENTER to continue\r", 'red', 'on_white'))

def clear_folder(folder):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
				print colored("clear file: " + file_path, 'yellow')
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
				print colored("clear path: " + file_path, 'yellow')
		except Exception as e:
			print(e)

def reset_folders(folders):
	print colored("Reset working dirs", 'magenta', 'on_green')
	for folder in folders:
		if os.path.exists(folder):
			clear_folder(folder)
		else:
			os.makedirs(folder)
			print colored("make new dir: " + folder, 'magenta', 'on_green')

def reduceFileNames(path):
	print colored("Run hashren.exe script for %s" % (path) , 'blue', 'on_green')
	p = Popen(["tools/hashren.exe", path])
	p.communicate()
	print colored("Done", 'blue', 'on_green')

def copySDCardFiles(src_files_list, dest_files_list, tmp_folder):
	print colored("Copy SD-Card files to %s" % (tmp_folder), 'green')
	
	if len(src_files_list) > 0:
		for src, dest in zip(src_files_list, dest_files_list):
			dest = os.path.join(tmp_folder, dest)
			if os.path.isdir(src):
				func.copytree(src, dest)
			elif os.path.isfile(src):
				dest_path = os.path.dirname(os.path.abspath(dest))
				if not os.path.exists(dest_path):
					os.makedirs(dest_path)
				shutil.copy2(src, dest)
			else:
				print_warning("SD-Card file not found: " + src)

def printEndMessage():
	warningListLen = len(WarningList)
	endColor = 'green'
	
	if warningListLen > 0:
		endColor = 'red'
		print colored("You have %d warning/s!!" % (warningListLen), 'red')
		input = raw_input(colored("Want to see it? (y/n) ", 'red', 'on_white'))
		if input != 'n':
			for warning in WarningList:
				print warning
				input = raw_input(colored("Press ENTER to continue\r", endColor, 'on_white'))
	

def do(project):
	print colored("Packing project: %s" % (project['projectName']), 'white', 'on_green', attrs=['bold'])
	
	# prepare temp data folders
	data_folder     = './data_files'
	firmware_folder = './install_files'
	output_folder   = './archive'
	tmp_folder      = './tmp'
	
	dest_folders = [
		data_folder,
		firmware_folder,
		output_folder,
		tmp_folder,
	]
	
	#clear working tree
	reset_folders(dest_folders)
	
	#copy sd-card data to tmp_folder
	copySDCardFiles(project['src_files_list'], project['dest_files_list'], tmp_folder)
	
	#convert file names
	reduceFileNames(tmp_folder)
	
	#copy data from tmp_folder to data_folder
	print colored("Copy tmp folder to data folder", 'green')
	func.copytree(tmp_folder, data_folder)
	
	#copy sd-card firmware file to firmware_folder
	SDCardFirmwareFileName = func.generateSDCardFirmwareFileName(project)
	
	firmwareSourcePath           = func.getProjectFirmwareDir(project)
	SDCardFirmwareFileSourcePath = os.path.join(firmwareSourcePath, SDCardFirmwareFileName)
	SDCardFirmwareFileDestPath   = os.path.join(firmware_folder, 'firmware.bin')
	
	shutil.copy2(SDCardFirmwareFileSourcePath, SDCardFirmwareFileDestPath)
	
	#pack firmware in several ways
	fw_pack = project['deviceName'] + '_FW.bin'
	sd_pack = project['deviceName'] + '_SD.bin'
	fw_sd_pack = project['deviceName'] + '_FW_SD.bin'
	
	print colored("Run DLPack.exe script for firmware and data folders:", 'white', 'on_green')
	print colored("pack firmware", 'white', 'on_green')
	p = Popen(["tools/DLPack.exe", firmware_folder, 'null', os.path.join(output_folder, fw_pack)])
	p.communicate()
	print colored("pack data", 'white', 'on_green')
	p = Popen(["tools/DLPack.exe", data_folder, 'null', os.path.join(output_folder, sd_pack)])
	p.communicate()
	print colored("pack firmware and data", 'white', 'on_green')
	p = Popen(["tools/DLPack.exe", firmware_folder, data_folder, os.path.join(output_folder, fw_sd_pack)])
	p.communicate()
	
	#pack bootloader
	bootloader_project = project.copy()
	bootloader_project['project'] = 'loader'
	bootloader_project['deviceName'] = 'loader'
	bootloader_project['boardVariant'] = ''
	bootloader_project['langkey'] = 'rom'
	SDCardBootloaderFileName = func.generateSDCardFirmwareFileName(bootloader_project)
	
	bootloaderSourcePath           = func.getProjectFirmwareDir(bootloader_project)
	SDCardBootloaderFileSourcePath = os.path.join(bootloaderSourcePath, SDCardBootloaderFileName)
	SDCardBootloaderFileDestPath   = os.path.join(firmware_folder, 'bootldr.bin')
	
	clear_folder(firmware_folder)
	
	shutil.copy2(SDCardBootloaderFileSourcePath, SDCardBootloaderFileDestPath)
	
	print colored("Run DLPack.exe script for bootloader", 'white', 'on_green')
	bl_pack = project['deviceName'] + '_BL.bin'
	p = Popen(["tools/DLPack.exe", firmware_folder, 'null', os.path.join(output_folder, bl_pack)])
	p.communicate()
	
	printEndMessage()
	
