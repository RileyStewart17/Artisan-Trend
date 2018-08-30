import configparser
config = configparser.RawConfigParser()
config.optionxform = str 
config['Directory'] = {'Location': 'C:/Users/Riley/Documents/work/Artisan-Trend-master/AC/'}
config['CT Labels'] = {'T1 CT': 'T1',
                       'T2 CT': 'T2',
                       'T3 Main CT': 'T3 Main/T3/T3 M CT',
                       'T3 Closed Loop CT': 'T3 CL CT/T3 Closed CT',
                       'T4 Main CT': 'T4 Main/T4/T4 M CTk',
                       'BCAC CT': 'BCAC'}
config['CL Labels'] = {'T1 HW': 'T1/T1 Hot Water',
                       'T1 CHW': 'T1 Chilled Water/T1 Chilled/T1 Chilled Loop',
                       'T1 Closed Loop': 'T1 CL/T1 Closed',
                       'T2 HW': 'T1/T1 Hot Water',
                       'T2 CHW': 'T2 Chilled Water/T2 Chilled/T2 Chilled Loop',
                       'T2 Closed Loop': 'T2 CL/T2 Closed',
                       'T3 HW': 'T3/T3 Hot Water',
                       'T3 CHW': 'T3 Chilled Water/T3 Chilled/T3 Chilled Loop',
                       'T3 Closed Loop': 'T3 CL/T3 Closed',
                       'T4 HW': 'T4/T4 Hot Water',
                       'T4 CHW': 'T4 Chilled Water/T4 Chilled/T4 Chilled Loop',
                       'T4 Closed Loop': 'T4 CL/T4 Closed',
                       'BCAC CHW': 'BCAC Chilled/BCAC Chilled Water'}
with open('settings.ini', 'w') as configfile:
   config.write(configfile)
