import configparser
config = configparser.RawConfigParser()
config.optionxform = str 
config['Directory'] = {'Location': '/Users/riley/Documents/Work/AC/'}
config['CT Labels'] = {'737 CT': '737',
                       'DC10 CT': 'DC10',
                       'Air Comp. CT': 'Air Comp CT/Air CT',
                       'ABS CT': 'ABS/Absorber CT/Absorber',
                       'Steel Storage Tank': 'Steel/Steel ST/Steel Tank',
                       'Concrete Storage Tank': 'Concrete/Concrete ST/Concrete Tank'}
config['CL Labels'] = {'Chilled Loop': 'CHW/Chilled/CHW Loop',
                       'Hot Heating Loop': 'Hot Water Htg/HW/HW Loop'}
with open('settings.ini', 'w') as configfile:
   config.write(configfile)
