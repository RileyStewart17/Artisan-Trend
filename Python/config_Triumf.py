import configparser
config = configparser.RawConfigParser()
config.optionxform = str 
config['Directory'] = {'Location': '/Users/riley/Documents/Work/SFU/'}
config['CT Labels'] = {'Cyclotron CT': 'Cyclotron Cooling Tower',
                       'ISAC CT': 'ISAC Cooling Tower'}
config['CL Labels'] = {'ASB Chilled': 'ASB CHW',
                       'Main HW': 'Hot Water Htg',
                       'TASC CHW': 'TASC Chilled'}
with open('settings.ini', 'w') as configfile:
   config.write(configfile)