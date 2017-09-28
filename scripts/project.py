'''
Created on 28 sept. 2017.

@author: andrey.vinogradov
'''

class Device():
    '''
    classdocs
    '''
    
    def __init__(self, name, board, boardVariant):
        self.name         = name
        self.board        = board
        self.boardVariant = boardVariant

class Project(object):
    '''
    classdocs
    '''
    
    def __init__(self, path, command, name, workingName, platform, production, deviceName, device, langkey):
        '''
        Constructor
        TODO: make projectName and workingName the same
        '''
        self.path         = path
        self.command      = command
        self.name         = name
        self.workingName  = workingName
        self.platform     = platform
        self.production   = production
        self.deviceName   = deviceName
        self.device       = device
        self.langkey      = langkey
        
        
        