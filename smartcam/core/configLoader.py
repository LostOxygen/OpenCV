import logging
import configparser
import os

class configReader():
'''
The configReader/Loader for the tcp-server. Should be handled as a semi-singleton implementation to work properly.
The Class creates a standard config file when no config file is found. Once a config file is found the configReader loads the file and provides it as a singleton.

'''
    config = configparser.ConfigParser()

    def __init__(cls):
        cls.path = ""
        pass

    @classmethod
    def loadConfig(cls, path):
        if os.path.exists(path):
            logging.debug('Config file found!')
            cls.path = path
            cls.config.read(path)
        else:
            logging.warning('Config file not found. A new config file will be generated..')
            cls.path = path
            cls.createConfigFile(path)

    @classmethod
    def createConfigFile(cls, path):
        try:
            cls.config['tcp'] = {'host' : '192.168.8.60',
                                'port' : 5005}
            cls.config['web'] = {'web_host' : '134.147.234.232',
                                'web_port' : 80}
            cls.config['conversion'] = {'distanceToObject' : 0,
                                        'mm_per_pixel' : 1,
                                        'scalingFactor' : 1}
            cls.config['edges1'] = {'edge_x1' : 0,
                                    'edge_x2' : 0,
                                    'edge_y1' : 0,
                                    'edge_y2' : 0}
            cls.config['image'] = {'width' : 0,
                                  'height' : 0}
            cls.config['points'] = {'min_x' : 0,
                                   'min_y' : 0,
                                   'max_x' : 0,
                                   'max_y' : 0}
            cls.config['calibration'] = {'realMeasurement' : 70,
                                         'mmPerPixel' : 1}
            cls.config['options'] = {'imagepath' : '/home/pi/.smartcam/images/'}
            cls.config['modules'] = {'circle' : True,
                                     'cable'  : True,
                                     'parts'  : True,
                                     'led'    : True,
                                     'iolink' : True,
                                     'schunk' : True
                                     }
            with open(path, 'w') as configFile:
                cls.config.write(configFile)
                cls.config.read(path)
                logging.info('Config file created and loaded')
        except Exception as e:
            logging.warning(str(e))
        return 0

    @classmethod
    def updateConfig(cls, section, key, newValue):
        cls.config[section] = {key : newValue}
        with open(cls.path, 'w') as configFile:
            cls.config.write(configFile)
        return 0

    @classmethod
    def returnEntry(cls, section, key):
        return cls.config[section][key]
