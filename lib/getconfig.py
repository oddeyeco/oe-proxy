import os
import configparser
import glob

config = configparser.RawConfigParser()
config_files = (glob.glob(os.getcwd()+'/conf/*.ini'))
config.read(config_files)

def getparam (key, value):
    v = config.get(key, value)
    if v == 'True':
        v = True
    if v == 'False':
        return False
    else:
        return v
