import configparser
config = configparser.RawConfigParser()
config.optionxform = str 
config['Directory'] = {'Location': '/Users/riley/Documents/Work/SFU/'}
config['CT Labels'] = {'ASB Tower': 'ABS Tower/ABS CT',
                       'TASC 1 CT-1': 'TASC Small CT/TASC 1 CT',
                       'TASC 1 CT-2': 'TASC Big CT/TASC 2 CT'}
config['CL Labels'] = {'ASB Chilled': 'ASB CHW',
                       'Main HW': 'Hot Water Htg',
                       'TASC CHW': 'TASC Chilled'}
with open('settings.ini', 'w') as configfile:
   config.write(configfile)