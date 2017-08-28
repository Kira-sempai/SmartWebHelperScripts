import os, shutil
import sys
sys.path.insert(0, "./scripts")
import func
from subprocess import Popen

def clear_folder(folder):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)

def reset_folders(folders):
	for folder in folders:
		if os.path.exists(folder):
			clear_folder(folder)
		else:
			os.makedirs(folder)
	
			
def do(project_path, projectName, production, deviceName, board, boardVariant, src_files_list, dest_files_list):
	
	if production :
		projectName = projectName + '_production'

	buildDirPath	= os.path.join(project_path, "build/", projectName, "device" + boardVariant)
	
	baseEnv = dict()
	baseEnv['CFG_OEM_ID']			= 'OID_SOREL'
	baseEnv['CFG_DEVICENAME']		= deviceName
	baseEnv['TARGET_PLATFORM']		= 'STM32'
	baseEnv['BOARD']				= board
	baseEnv['CFG_BOARD_REVISION']	= '1'
	baseEnv['CFG_BOARD_VARIANT']	= boardVariant
	
	sdCardFirmwarePostfix			= 'west-sdcard.bin'
	
	SDCardFirmwareFileName = func.MakeFilename(baseEnv, sdCardFirmwarePostfix)
	
	# prepare temp data folders
	data_folder = './data_files'
	firmware_folder = './install_files'
	output_folder = './archive'
	
	dest_folders = [
		data_folder,
		firmware_folder,
		output_folder,
	]
	
	reset_folders(dest_folders)
	
	#copy sd-card data to data_folder
	if len(src_files_list) > 0:
		for src, dest in zip(src_files_list, dest_files_list):
			dest = os.path.join(data_folder, dest)
			if os.path.isdir(src):
				func.copytree(src, dest)
			else:
				shutil.copy2(src, dest)
	
	#copy sd-card firmware file to firmware_folder
	firmwareSourcePath           = os.path.join(buildDirPath, 'shared/platform/stm32/')
	SDCardFirmwareFileSourcePath = os.path.join(firmwareSourcePath, SDCardFirmwareFileName)
	SDCardFirmwareFileDestPath   = os.path.join(firmware_folder, 'firmware.bin')
	
	shutil.copy2(SDCardFirmwareFileSourcePath, SDCardFirmwareFileDestPath)
	
	
	#convert file names
	p = Popen(["hashren.exe", data_folder])
	stdout, stderr = p.communicate()
	
	
	#pack firmware in several ways
	fw_pack = deviceName + '_FW.bin'
	sd_pack = deviceName + '_SD.bin'
	fw_sd_pack = deviceName + '_FW_SD.bin'
	
	p = Popen(["DLPack.exe", firmware_folder, 'null', os.path.join(output_folder, fw_pack)])
	stdout, stderr = p.communicate()
	p = Popen(["DLPack.exe", data_folder, 'null', os.path.join(output_folder, sd_pack)])
	stdout, stderr = p.communicate()
	p = Popen(["DLPack.exe", firmware_folder, data_folder, os.path.join(output_folder, fw_sd_pack)])
	stdout, stderr = p.communicate()
	
	
	#pack bootloader
	bl_pack = deviceName + '_BL.bin'
	baseEnv['CFG_DEVICENAME'] = 'loader'
	sdCardBootloaderPostfix = 'sdcard.bin'
	SDCardBootloaderFileName = func.MakeFilename(baseEnv, sdCardBootloaderPostfix)
	
	bootloaderSourcePath           = os.path.join(project_path, 'build/', projectName, 'loader/shared/platform/stm32/')
	SDCardBootloaderFileSourcePath = os.path.join(bootloaderSourcePath, SDCardBootloaderFileName)
	SDCardBootloaderFileDestPath   = os.path.join(firmware_folder, 'bootldr.bin')
	
	clear_folder(firmware_folder)
	
	shutil.copy2(SDCardBootloaderFileSourcePath, SDCardBootloaderFileDestPath)
	
	p = Popen(["DLPack.exe", firmware_folder, 'null', os.path.join(output_folder, bl_pack)])
	stdout, stderr = p.communicate()
	
	
	
	
	