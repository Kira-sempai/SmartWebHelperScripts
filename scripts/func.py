import os
import sys
import shutil
from termcolor import colored
#################################################
#################################################

def print_warning(warning):
    warning = colored(warning, 'white', 'on_red')
    print warning
    raw_input(colored("Press ENTER to continue\r", 'red', 'on_white'))

#copy all files in dir and subdirs
def copytree(src, dst, symlinks=False, ignore=None):
    
    isDir = os.path.isdir(src)
    
    if isDir:
        if not os.path.exists(dst):
            try:
                os.makedirs(dst)
            except OSError as e:
                print_warning('Error %d: Can\'t create folder at "%s"' %(e.errno, dst))
                sys.exit()
                 
            
        
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copytree(s, d, symlinks, ignore)
            else:
                if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                    shutil.copy2(s, d)
    else:
        dstDir = os.path.dirname(dst)
        if not os.path.exists(dstDir):
            os.makedirs(dstDir)
        shutil.copy2(src, dst)
        


class SrcDestData(object):
    '''
    classdocs
    '''
    
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
