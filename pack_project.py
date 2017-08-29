import os, shutil, sys
sys.path.insert(0, "./scripts")
import func
from subprocess import Popen
from distutils.dir_util import copy_tree
from termcolor import colored


def clear_folder(folder):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
				print colored("clear file: " + file_path, 'green')
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
				print colored("clear path: " + file_path, 'green')
		except Exception as e:
			print(e)

def reset_folders(folders):
	print colored("/n/rReset working dirs", 'green')

	for folder in folders:
		if os.path.exists(folder):
			clear_folder(folder)
		else:
			os.makedirs(folder)
			print colored("make new dir: " + folder, 'green')

def copySDCardFiles(src_files_list, dest_files_list, tmp_folder):
	print colored("/n/rCopy SD-Card files to tmp folder", 'green')
	
	if len(src_files_list) > 0:
		for src, dest in zip(src_files_list, dest_files_list):
			dest = os.path.join(tmp_folder, dest)
			if os.path.isdir(src):
				func.copytree(src, dest)
			else:
				shutil.copy2(src, dest)

def generateFirmwareFileName(deviceName, board, boardVariant, langkey):
	baseEnv = dict()
	baseEnv['CFG_OEM_ID']			= 'OID_SOREL'
	baseEnv['CFG_DEVICENAME']		= deviceName
	baseEnv['TARGET_PLATFORM']		= 'STM32'
	baseEnv['BOARD']				= board
	baseEnv['CFG_BOARD_REVISION']	= '1'
	baseEnv['CFG_BOARD_VARIANT']	= boardVariant
	
	sdCardFirmwarePostfix = 'sdcard.bin'
	if not langkey == 'rom':
		sdCardFirmwarePostfix = langkey + '-' + sdCardFirmwarePostfix
		
	return func.MakeFilename(baseEnv, sdCardFirmwarePostfix)


def do(project_path, projectName, production, deviceName, board, boardVariant, langkey, src_files_list, dest_files_list):
	# prepare temp data folders
	data_folder = './data_files'
	firmware_folder = './install_files'
	output_folder = './archive'
	tmp_folder = './tmp'
	
	dest_folders = [
		data_folder,
		firmware_folder,
		output_folder,
		tmp_folder,
	]
	
	#clear working tree
	reset_folders(dest_folders)
	
	#copy sd-card data to tmp_folder
	copySDCardFiles(src_files_list, dest_files_list, tmp_folder)
	
	#convert file names
	print colored("/n/rRun hashren.exe script for tmp folder", 'green')
	p = Popen(["hashren.exe", tmp_folder])
	p.communicate()
	
	#copy data from tmp_folder to data_folder
	print colored("/n/rCopy tmp folder to data folder", 'green')
	copy_tree(tmp_folder, data_folder)
	
	#copy sd-card firmware file to firmware_folder
	if production :
		projectName = projectName + '_production'
	
	SDCardFirmwareFileName = generateFirmwareFileName(deviceName, board, boardVariant, langkey)
	
	firmwareSourcePath           = os.path.join(project_path, "build/", projectName, "device" + boardVariant, 'shared/platform/stm32/')
	SDCardFirmwareFileSourcePath = os.path.join(firmwareSourcePath, SDCardFirmwareFileName)
	SDCardFirmwareFileDestPath   = os.path.join(firmware_folder, 'firmware.bin')
	
	shutil.copy2(SDCardFirmwareFileSourcePath, SDCardFirmwareFileDestPath)
	
	#pack firmware in several ways
	fw_pack = deviceName + '_FW.bin'
	sd_pack = deviceName + '_SD.bin'
	fw_sd_pack = deviceName + '_FW_SD.bin'
	
	print colored("/n/rRun DLPack.exe script for firmware and data folders:", 'green')
	print colored("pack firmware", 'green')
	p = Popen(["DLPack.exe", firmware_folder, 'null', os.path.join(output_folder, fw_pack)])
	p.communicate()
	print colored("pack data", 'green')
	p = Popen(["DLPack.exe", data_folder, 'null', os.path.join(output_folder, sd_pack)])
	p.communicate()
	print colored("pack firmware and data", 'green')
	p = Popen(["DLPack.exe", firmware_folder, data_folder, os.path.join(output_folder, fw_sd_pack)])
	p.communicate()

	#pack bootloader
	bootloader_name = 'loader'
	SDCardBootloaderFileName = generateFirmwareFileName(bootloader_name, board, boardVariant, langkey)
	
	bootloaderSourcePath           = os.path.join(project_path, 'build/', projectName, bootloader_name, 'shared/platform/stm32/')
	SDCardBootloaderFileSourcePath = os.path.join(bootloaderSourcePath, SDCardBootloaderFileName)
	SDCardBootloaderFileDestPath   = os.path.join(firmware_folder, 'bootldr.bin')
	
	clear_folder(firmware_folder)
	
	shutil.copy2(SDCardBootloaderFileSourcePath, SDCardBootloaderFileDestPath)
	
	print colored("run DLPack.exe script for bootloader", 'green')
	bl_pack = deviceName + '_BL.bin'
	p = Popen(["DLPack.exe", firmware_folder, 'null', os.path.join(output_folder, bl_pack)])
	p.communicate()
	
	input = raw_input("Press ENTER to continue")
	
	
	
	