import configparser
config = configparser.RawConfigParser()
config.optionxform = str 
config['Directory'] = {'Location': '/Users/riley/Documents/Work/SFU/'}
config['CT Labels'] = {'CT 1': 'CT-1/CT1',
                       'CT 2': 'CT-2/CT2'}
config['CL Labels'] = {'Chilled Loop': 'CHW/Chilled Water'}
with open('settings.ini', 'w') as configfile:
   config.write(configfile)