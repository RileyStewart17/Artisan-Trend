import plotly as py2
import plotly.graph_objs as go
import numpy as np
from os import listdir
from os.path import isfile, join
import configparser as configparser
from difflib import get_close_matches
# Created by Riley Stewart for Artisan Engineering.
# Not to be copied, used, or revised without explicit written 
# permission from the author and Artisan Engineering.

import xlrd
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter.filedialog import askdirectory
from tkinter import messagebox

## prompt user if new sample found
## Append to CTdata/CLdata if only one table present
## Load sample names from somewhere + have menu to change names

#----------------------------------------------------------------------

# This loads the directory of the files + the sample names for future use. The
# script first trys to open the 'settings.txt' file to pull the directory; if
# such a file doesn't exist, the user is prompted to select directory using a menu.
# The 'settings.txt' file is then created with the directory stored. The labels
# for the samples are then pulled from the settings file. 


try:
    config = configparser.RawConfigParser()
    config.optionxform = str 
    config.read('settings.ini')
    dirname = config['Directory']['Location']
    
except:
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo('Air Canada Trends', 'Please select the folder that contains the excel report files.')
    dirname = askdirectory(parent=root,initialdir="/",title='Please select a directory')+'/'
    root.destroy()
    if dirname != '/':
        config = configparser.RawConfigParser()
        config.optionxform = str 
        config.set('Directory', 'Location', dirname)
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

labels = []
alt_labels = []
labels_sub = [] # First three letters of each sample name (for sorting)

cl_labels = []
alt_cl_labels = []
cl_labels_sub = []

try:
    for key in config['CT Labels']:
        labels.append(key)
        labels_sub.append(key[:3].lower())
        temp = config['CT Labels'][key].split('/')
        alt_labels.append(temp)
            
    for key in config['CL Labels']:
        cl_labels.append(key)
        cl_labels_sub.append(key[:3].lower())
        temp = config['CL Labels'][key].split('/')
        alt_cl_labels.append(temp)
        
except:
    pass

ACdir = dirname
labels = sorted(labels, key = lambda x: x[:3].lower())
labels_sub = sorted(labels_sub, key = lambda x: x[:3].lower())
alt_labels = sorted(alt_labels, key = lambda x: x[0][:3].lower()) 
cl_labels = sorted(cl_labels, key = lambda x: x[:3].lower())  
cl_labels_sub = sorted(cl_labels_sub, key = lambda x: x[:3].lower())
alt_cl_labels = sorted(alt_cl_labels, key = lambda x: x[0][:3].lower())

try:
    onlyfilesAC = [f for f in listdir(ACdir) if isfile(join(ACdir, f))] # List of files present in directory
    onlyfilesAC = [i for i in onlyfilesAC if 'xlsx' in i[-4:]] # grabs list of files present in directory that are excel worksheets
except:
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo('Air Canada Trends', 'Error loading files. Please re-select the folder that contains the excel report files.')
    dirname = askdirectory(parent=root,initialdir="/",title='Please select a directory')+'/'
    root.destroy()
    if dirname != '/':
        config = configparser.RawConfigParser()
        config.optionxform = str 
        config.set('Directory', 'Location', dirname)
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
    onlyfilesAC = [f for f in listdir(ACdir) if isfile(join(ACdir, f))] # List of files present in directory
    onlyfilesAC = [i for i in onlyfilesAC if 'xlsx' in i[-4:]] # grabs list of files present in directory that are excel worksheets


#----------------------------------------------------------------------

# This function simply loads the first sheet of an excel file, of which
# one may pull specific columns or rows.

def open_file(path):
    book = xlrd.open_workbook(path)
    first_sheet = book.sheet_by_index(0)
    return first_sheet

# Creates a list of the loaded excel files from the directory, opening the
# first sheet of each file.

AClist = []
for i in range(len(onlyfilesAC)):
    AClist.append(open_file(ACdir + onlyfilesAC[i]))
    
#----------------------------------------------------------------------
    
# This function takes a open sheet ('file') and parses through the sheet,
# pulling the data from the worksheet and organizing it into 4 lists:
# 1. CTvariables, which contains all of the test names for the CTs 
#    (ex. 'TDS', 'ORP', etc.)
# 2. CTdata, which contains the data for each of the CT samples, organized by 
#    sample name in the first element, followed by the test values in the 
#    same order as the test names present in CTvariables
# 3. CLvariables, which contains all the test names for the CL samples
# 4. CLdata, which contains the data for each of the CL samples, organized similarly
#    to CTdata

def pulldata(file):
    global labels, labels_sub, cl_labels, cl_labels_sub
    labels_loc = []    # List to contain sample names in file
    labels_loc_3 = []  # List to contain first three letters of sample names (for sorting)
    cl_labels_loc = []
    cl_labels_loc_3 = []     
    
    data = {}
    
    CTdata = []
    CLdata = []
    CTvariables = []
    CLvariables = []
    
    ct_tests = ['tds', 'orp', 'cond', 'fe', 'cu', 'mg', 'ca', 'fatp', 'f', 't', 'tatp', 'zn', 'm. alk', 'm alk']
    cl_tests = ['tds', 'cond', 'fe', 'cu', 'nit', 'nitrite', 'mo', 'molybdenum']
    
    try:
        for i in range(100):
            temp = []
            x = file.row_values(i)
            if 'Sample' in x:
                temp.append(x)
                for t in range(10):
                    y = file.row_values(t+i)
                    if y[0].lower() == 'target':
                        break
                    if y[0] not in ['', 'target', 'Target', 'Sample']:
                        temp.append(y)
            if len(temp) != 0:
                data['data{0}'.format(len(data))] = temp
            
    except IndexError:
        if len(temp) != 0:
            data['data{0}'.format(len(data))] = temp
        pass
    
    
#    for i in range(len(data)):
#        if labels_loc_3[i] in labels_sub:
#            CTdata.append(data[i])
#        else:
#            CLdata.append(data[i])
#            
    for i in range(len(data)):
        try:
            temp_list = data['data{0}'.format(i)][1:]
            temp_list2 = data['data{0}'.format(i+1)][1:]
            labels_list = [item[0][:3].lower() for item in temp_list]
            labels_list2 = [item[0][:3].lower() for item in temp_list2]
            if set(labels_list) == set(labels_list2):
                temp = []
                temp.append(list(np.concatenate((data['data{0}'.format(i)][0],data['data{0}'.format(i+1)][0][1:]))))
                for t in range(len(temp_list)):
                    temp.append(list(np.concatenate((temp_list[t], temp_list2[t][1:]))))
                data['data{0}'.format(i)] = temp
                data.pop('data{0}'.format(i+1), None)
            
          
        except KeyError:
            pass               
    for i in range(len(data)+1):
        try:
            temp_list = data['data{0}'.format(i)][1:]
            temp_variables = data['data{0}'.format(i)][0]
            temp_ct_var = [i for i in temp_variables if i.lower() in ct_tests]
            temp_cl_var = [i for i in temp_variables if i.lower() in cl_tests]
            labels_list_3 = [item[0][:3].lower() for item in temp_list]
            labels_list = [item[0] for item in temp_list]
            if len(temp_ct_var) > len(temp_cl_var):
                if len(CTvariables) == 0:
                    CTvariables = data['data{0}'.format(i)][0]
                else:
                    missing_tests = np.setdiff1d(data['data{0}'.format(i)][0], CTvariables)[0]
                    variables2 = data['data{0}'.format(i)][0]
                    data2 = temp_list
                    if len(missing_tests) != 0:
                        for t in range(len(missing_tests)):
                            CTvariables.append(missing_tests[t])
                            for v in range(len(CTdata)):
                                CTdata[v].append('')
                    for l in range(5):
                        for o in range(len(CTvariables)):
                            if variables2[o] != CTvariables[o]:
                                ind_sort = np.where(np.array(CTvariables) == variables2[o])[0]
                                if len(ind_sort) == 0:
                                    if variables2[o] != '':
                                        CTvariables = list(np.append(CTvariables, variables2[o]))
                                        variables2 = list(np.append(variables2, ''))
                                        for p in range(len(CTdata)):
                                            CTdata[p] = list(np.append(CTdata[p], ''))
                                        for p in range(len(data2)):
                                            data2[p] = list(np.append(data2[p], ''))
                                else:
                                    variables2[o], variables2[ind_sort[0]] = variables2[ind_sort[0]], variables2[o]
                                    for v in range(len(data2)):
                                        data2[v][o], data2[v][ind_sort[0]] = data2[v][ind_sort[0]], data2[v][o]
                    temp_list = data2
                if len(labels_loc) == 0:
                    labels_loc = labels_list
                    labels_loc_3 = labels_list_3
                else:
                    missing_samples=[el for el in labels_list_3 if el not in labels_loc]
                    if len(missing_samples) != 0:
                        for t in range(len(missing_samples)):
                            ind_temp = np.where(np.array(labels_list_3) == missing_samples[t])[0][0]
                            labels_loc.append(labels_list[ind_temp])
                            labels_loc_3.append(labels_list[ind_temp][:3].lower())
                for item in temp_list:
                    CTdata.append(item)
            if len(temp_cl_var) > len(temp_ct_var):
                for item in temp_list:
                    CLdata.append(item)
                if len(CLvariables) == 0:
                    CLvariables = data['data{0}'.format(i)][0]
                else:
                    missing_tests = np.setdiff1d(data['data{0}'.format(i)][0], CLvariables)[0]
                    if len(missing_tests) != 0:
                        for t in range(len(missing_tests)):
                            CLvariables.append(missing_tests[t])
                            for v in range(len(CLdata)):
                                CLdata[v].append('')
                if len(cl_labels_loc) == 0:
                    cl_labels_loc = labels_list
                    cl_labels_loc_3 = labels_list_3
                else:
                    missing_samples = np.setdiff1d(labels_list_3, cl_labels_loc)
                    if len(missing_samples) != 0:
                        for t in range(len(missing_samples)):
                            ind_temp = np.where(np.array(labels_list_3) == missing_samples[t])[0][0]
                            cl_labels_loc.append(labels_list[ind_temp])
                            cl_labels_loc_3.append(missing_samples[t])
        except KeyError:
            pass
    if len(labels) != 0: 
        if set(labels) != set(labels_loc):
            full_label_list = labels  + [item for sublist in alt_labels for item in sublist]
            for i in range(len(labels_loc)):
                try:
                    result = get_close_matches(labels_loc[i], full_label_list)[0]
                    if result not in labels:
                            for v in range(len(alt_labels)):
                                if result in alt_labels[v]:
                                    result = labels[v]
                    labels_loc[i] = result
                    CTdata[i][0] = result
                except:
                    print(labels_loc[i])
            if set(labels) != (labels_loc):
                missing_samples = [i for i in labels if i not in labels_loc]
                for i in range(len(missing_samples)):
                    if CTvariables != []:
                        fill = ['' for x in range(len(CTvariables))]
                    else:
                        fill = ['' for x in range(10)]
                    fill[0] = missing_samples[i]
                    labels_loc.append(missing_samples[i])
                    CTdata.append(fill)
    
    together = zip(labels_loc, CTdata)
    sorted_together =  sorted(together, key=lambda x: x[0].lower())     
    labels_loc = [x[0] for x in sorted_together]
    CTdata = [x[1] for x in sorted_together]
    
    if len(cl_labels) != 0: 
        if set(cl_labels) != set(cl_labels_loc):
            full_label_list = cl_labels  + [item for sublist in alt_cl_labels for item in sublist]
            for i in range(len(labels_loc)):
                try:
                    result = get_close_matches(cl_labels_loc[i], full_label_list)[0]
                    if result not in cl_labels:
                            for v in range(len(alt_cl_labels)):
                                if result in alt_cl_labels[v]:
                                    result = cl_labels[v]
                    cl_labels_loc[i] = result
                    CLdata[i][0] = result
                except:
                    pass
                    #print(cl_labels_loc[i])
            if set(cl_labels) != (cl_labels_loc):
                missing_samples = [i for i in cl_labels if i not in cl_labels_loc]
                if len(missing_samples) != 0:
                    for i in range(len(missing_samples)):
                        if CLvariables != []:
                            fill = ['' for x in range(len(CLvariables))]
                        else:
                            fill = ['' for x in range(10)]
                        fill[0] = missing_samples[i]
                        cl_labels_loc.append(missing_samples[i])
                        CLdata.append(fill)
#    if len(cl_labels_sub) != 0:
#        if set(cl_labels) != set(cl_labels_loc):
#            if set(cl_labels_sub) != set(cl_labels_loc_3):
#                missing_samples = np.setdiff1d(cl_labels_sub,cl_labels_loc_3)
#                for v in range(len(missing_samples)):
#                    ind_lab = np.where(np.array(cl_labels_sub) == missing_samples[v])[0][0]
#                    cl_labels_loc_3.append(missing_samples[v])
#                    fill = ['' for x in range(len(CLvariables))]
#                    fill[0] = cl_labels[ind_lab]
#                    cl_labels_loc.append(cl_labels[ind_lab])
#                    CLdata.append(fill)
#                if set(cl_labels) != set(cl_labels_loc):
#                    wrong_names = np.setdiff1d(cl_labels_loc, cl_labels)
#                    diff_names = np.setdiff1d(cl_labels, cl_labels_loc)
#                    for v in range(len(wrong_names)):
#                        ind_lab = np.where(np.array(cl_labels_loc) == wrong_names[v])[0][0]
#                        #CLdata = [i[0].replace(wrong_names[v], diff_names[v]) + i[1:] for i in CLdata]
#                        CLdata[ind_lab][0] = diff_names[v]
#                        cl_labels_loc[ind_lab] = diff_names[v]
#            else:
#                wrong_names = np.setdiff1d(cl_labels_loc, cl_labels)
#                diff_names = np.setdiff1d(cl_labels, cl_labels_loc)
#                for v in range(len(wrong_names)):
#                    ind_lab = np.where(np.array(cl_labels_loc) == wrong_names[v])[0][0]
#                    #CLdata = [i[0].replace(wrong_names[v], diff_names[v]) + i[1:] for i in CLdata]
#                    CLdata[ind_lab][0] = diff_names[v]
#                    cl_labels_loc[ind_lab] = diff_names[v]                 
    together = zip(cl_labels_loc, CLdata)
    sorted_together =  sorted(together, key=lambda x: x[0].lower())     
    cl_labels_loc = [x[0] for x in sorted_together]
    CLdata = [x[1] for x in sorted_together]
            
        


    return CTvariables, CTdata, CLvariables, CLdata


colors = ['#4285F4', '#FBBC05', '#34A853', '#EA4335', '#964f8e', '#33cccc']
colors_alt = ['#b7d1fb', '#feebb4', '#c4edcf', '#f8bfba', '#e5cde2', '#c2f0f0']    
        
def tryinteger(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
def str_search(string, substring_list):
    for substring in substring_list:
        if substring in string:
            return substring
    return False
            
def date(filename):  #filename is a string
    long = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December']
    short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
             'Oct', 'Nov', 'Dec']
    if tryinteger(filename[0]):
        datestr = filename[:10]
        return datestr
    elif 'Report' in filename:
        date_str = filename.split('Report')[1][:-5]
        ban = str_search(date_str, long)
        if not ban:
            datetime_object = datetime.strptime(date_str, '%b%d%Y')
        else:
            ind = np.where(ban  == np.array(long))[0][0]
            date_str = date_str.replace(long[ind], short[ind])
            datetime_object = datetime.strptime(date_str, '%b%d%Y')
        datestr = datetime_object.strftime('%Y-%m-%d')
        return datestr
    else:
        for i in range(len(short)):
            if short[i] in filename:
                date_str = short[i] + filename.split(short[i])[1][:-5]
                ban = str_search(date_str, long)
                if not ban:
                    datetime_object = datetime.strptime(date_str, '%b%d%Y')
                else:
                    ind = np.where(ban  == np.array(long))[0][0]
                    date_str = date_str.replace(long[ind], short[ind])
                    datetime_object = datetime.strptime(date_str, '%b%d%Y')
                datestr = datetime_object.strftime('%Y-%m-%d')
                return datestr
                
                
        

dates = []
            
for i in range(len(onlyfilesAC)):
    dates.append(date(onlyfilesAC[i]))
date_temp = zip(dates, AClist)
date_temp_sorted =  sorted(date_temp, key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))
dates = [x[0] for x in date_temp_sorted]
AClist = [x[1] for x in date_temp_sorted]
dates_title = [dates[0], dates[len(dates)-1]]
dates_title = [datetime.strptime(item, '%Y-%m-%d').strftime('%B %Y') for item in dates_title]

def change_directory_variable(updated_variable):
    global dirname
    dirname = updated_variable
    

def change_directory():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo('Air Canada Trends', 'Please select the folder that contains the excel report files.')
    dirname2 = askdirectory(parent=root,initialdir="/",title='Please select a directory')+'/'
    root.destroy()
    if dirname2 != '/':
        config.set('Directory', 'Location', dirname2)
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
    change_directory_variable(dirname2)

choice = None
def change_samples(arg):
    global choice
    choice = arg
    listbox_app = listbox()
    listbox_app.window.mainloop()


def on_exit(window):
    window.destroy()
    window.quit()

def plotter(system, test):
    global labels, cl_labels
    datadict = {}
    datadict2 = {}
    
    ban = ('', 'system drained', '-', 'drained', 'drained for winter')
    ban2 = ('>', '<')
#    ban3 = ('', ' ', 'sample', 'target')
#    ban4 = ('sample', 'target')
    keysnom = ('TDS', 'ORP', 'Cu', 'Zn', 'pH')
    
    if system == 'CT':
#        labels = []
#        labels_sub = []
#        for i in range(len(AClist)):
#            for v in range(100):
#                x = AClist[i].cell(v,0)
#                if x == 'Sample':
#                    sample_ind = v
#                    break
#            for v in range(10):
#                x = AClist[i].cell(sample_ind+v+1)
#                if x.lower() not in ban3:
#                    if x[:3].lower() not in labels_sub:
#                        labels.append(x)
#                        labels_sub.append(x[:3].lower())
#                if x.lower() == 'target':
        labels_local = labels
        NCT = len(labels_local)
        
        for i in range(NCT):
            data = []
            data2 = []

            if test in keysnom:
                name = test
                for t in range(len(AClist)):  
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where(np.array(pulldata(AClist[t])[0]) == test)[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except IndexError:
                        data.append(np.nan)
                        pass
        
            if test.lower() == 'cl':
                name = 'Cl'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((np.array(pulldata(AClist[t])[0]) == 'Free Cl') | (np.array(pulldata(AClist[t])[0]) == 'Cl'))[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
            
            if test.lower() == 'malk':
                name = 'M. Alk'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((np.array(pulldata(AClist[t])[0]) == 'M. Alk') | (np.array(pulldata(AClist[t])[0]) == 'Alkalinity') | (np.array(pulldata(AClist[t])[0]) == 'Alk.') | (np.array(pulldata(AClist[t])[0]) == 'M.Alk'))[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
            
            if test.lower() in ('po4', 'phosphate', 'pho4', 'orthophosphate'):
                name = 'PO4'
                name2 = 'PhO4'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where(np.array(pulldata(AClist[t])[0]) == 'PO4')[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                for t in range(len(AClist)):
                    try:
                        d2 = pulldata(AClist[t])[1][i]
                        ind = np.where(np.array(pulldata(AClist[t])[0]) == 'PhO4')[0][0]
                        u2 = str(d2[ind])
                        if u2 in ban:
                            u2 = np.nan
                        elif u2[0] in ban2:
                            u2 = u1[1:]
                            if u2[-1] in ban2:
                                u2 = u2[:-1]
                        data2.append(float(u2))
                    except:
                        data2.append(np.nan)
                        pass    
                    
            if test.lower() in ('fe', 'iron'):
                name = 'Fe'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((np.array(pulldata(AClist[t])[0]) == 'Fe') | (np.array(pulldata(AClist[t])[0]) == 'Iron'))[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                    
            if test.lower() == 'cond':
                name = 'Conductivity'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((np.array(pulldata(AClist[t])[0]) == 'Cond') | (np.array(pulldata(AClist[t])[0]) == 'Cond.'))[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                    
            if test.lower() in ('hardness', 'ca', 'ca hardness', 'mg hardness', 'total hardness'):
                name = 'Ca Hardness'
                name2 = 'Mg Hardness'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((np.array(pulldata(AClist[t])[0]) == 'Ca Hardness') | (np.array(pulldata(AClist[t])[0]) == 'Ca'))[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                for t in range(len(AClist)):
                    try:
                        d2 = pulldata(AClist[t])[1][i]
                        ind = np.where((np.array(pulldata(AClist[t])[0]) == 'Mg Hardness') | (np.array(pulldata(AClist[t])[0]) == 'Mg'))[0][0]
                        u2 = str(d2[ind])
                        if u2 in ban:
                            u2 = np.nan
                        elif u2[0] in ban2:
                            u2 = u1[1:]
                            if u2[-1] in ban2:
                                u2 = u2[:-1]
                        data2.append(float(u2))
                    except:
                        data2.append(np.nan)
                        pass
                    
            if test.lower() in ('atp'):
                name = 'FATP'
                name2 = 'TATP'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((np.array(pulldata(AClist[t])[0]) == 'FATP') | (np.array(pulldata(AClist[t])[0]) == 'F') | (np.array(pulldata(AClist[t])[0]) == 'Free ATP'))[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                for t in range(len(AClist)):
                    try:
                        d2 = pulldata(AClist[t])[1][i]
                        ind = np.where((np.array(pulldata(AClist[t])[0]) == 'TATP') | (np.array(pulldata(AClist[t])[0]) == 'T') | (np.array(pulldata(AClist[t])) == 'Total ATP'))[0][0]
                        u2 = str(d2[ind])
                        if u2 in ban:
                            u2 = np.nan
                        elif u2[0] in ban2:
                            u2 = u1[1:]
                            if u2[-1] in ban2:
                                u2 = u2[:-1]
                        data2.append(float(u2))
                    except:
                        data2.append(np.nan)
                        pass
            

            datadict["data{0}".format(i)] = np.array(data)
            if len(data2) != 0:
                datadict2["data{0}".format(i)] = np.array(data2)
            
                

    if system == 'CL':
        labels_local = cl_labels
        NCT = len(labels_local)

        for i in range(NCT):
            data = []
            data2 = []
            if test.lower() in ('nitrite'):
                name = 'Closed Loop Nitrite'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[3][i]
                        ind = np.where((np.array(pulldata(AClist[t])[2]) == 'Nitrite') | (np.array(pulldata(AClist[t])[2]) == 'Nit'))[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                    
            if test.lower() in ('cltds'):
                name = 'Closed Loop TDS'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[3][i]
                        ind = np.where(np.array(pulldata(AClist[t])[2]) == 'TDS')[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                    
            if test.lower() in ('clph'):
                name = 'Closed Loop pH'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[3][i]
                        ind = np.where(np.array(pulldata(AClist[t])[2]) == 'pH')[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                    
            if test.lower() in ('clcu'):
                name = 'Closed Loop Cu'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[3][i]
                        ind = np.where(np.array(pulldata(AClist[t])[2]) == 'Cu')[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                    
            if test.lower() in ('clfe'):
                name = 'Closed Loop Fe'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[3][i]
                        ind = np.where(np.array(pulldata(AClist[t])[2]) == 'Fe')[0][0]
                        u1 = str(d1[ind])
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                            if u1[-1] in ban2:
                                u1 = u1[:-1]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
            
            datadict["data{0}".format(i)] = np.array(data)
            if len(data2) != 0:
                datadict2["data{0}".format(i)] = np.array(data2)
    
    data_sets = []
    data_sets2 = []
    for c in range(NCT):
        empt = []
        empt2 = []
        for i in range(len(datadict['data{0}'.format(c)])):
            #entry = dates[i] + '  ' + name + ': ' + str(datadict['data{0}'.format(c)][i])
            entry = name + ': ' + str(datadict['data{0}'.format(c)][i])
            empt.append(entry)
            if len(datadict2) != 0:
                #entry2 = dates[i] + '  ' + name2 + ': ' + str(datadict2['data{0}'.format(c)][i])
                entry2 =name2 + ': ' + str(datadict2['data{0}'.format(c)][i])
                empt2.append(entry2)
        #data_labels.append(empt)
        #data_labels2.append(empt2)
        #axis_num = 'y'
        #if c > 0:
        #    axis_num = 'y' + str(c+1)
            
        trace = go.Scatter(
             x = dates, 
            y = datadict['data{0}'.format(c)], 
            name = labels_local[c], 
            text = empt, 
            yaxis = 'y', 
            marker = dict(
                    size = 8,
                    color = colors[c],
                    )
        )
        data_sets.append(trace)
        if len(datadict2) != 0:
            trace2 = go.Scatter(
                 x = dates, 
                y = datadict2['data{0}'.format(c)], 
                name = labels_local[c], 
                text = empt2, 
                yaxis = 'y',
                marker = dict(
                    size = 8,
                    color = colors_alt[c],
                    )
            )
            data_sets2.append(trace2)
    
    data = go.Data(data_sets)
        # style all the traces
    for k in range(len(data)):
        data[k].update(
            {
                "type": "scatter",
                "hoverinfo": "name+x+text",
                'legendgroup': 'group{0}'.format(k),
                "line": {"width": 0.5}, 
                "marker": {"size": 8},
                "mode": "lines+markers",
                "showlegend": True
            }
        )
    if len(data_sets2) != 0:
        data2 = go.Data(data_sets2)
        for k in range(len(data2)):
            data2[k].update(
                {
                    "type": "scatter",
                    "hoverinfo": "name+x+text",
                    'legendgroup': 'group{0}'.format(k),
                    "line": {"width": 0.5}, 
                    "marker": {"size": 8},
                    "mode": "lines+markers",
                    "showlegend": False
                }
            )
        data = data + data2
    title = name + ' ({} - {})'.format(dates_title[0], dates_title[1])
    if len(datadict2) != 0:
        title = name + ' & ' + name2+ ' ({} - {})'.format(dates_title[0], dates_title[1])
    if test.lower() in ('tds', 'cltds'):
        y_title = 'TDS (ppm)'
    if test.lower() in ('cu', 'fe', 'cl', 'zn', 'po4', 'nitrite', 'malk', 'hardness', 'clcu', 'clfe'):
        if len(datadict2) != 0:
            y_title = name + ' & ' + name2 + ' (mg/L)'
        else:
            y_title = name + ' (mg/L)'
    if test.lower() in ('ph', 'clph'):
        if len(datadict2) != 0:
            y_title = name + ' & ' + name2
        else:
            y_title = name
    if test.lower() == 'orp':
        y_title = 'ORP (mV)'
    if test.lower() == 'atp':
        y_title = name + ' & ' + name2 + ' (RLU)'
    if test.lower() == 'cond':
        y_title = 'Conductivity (μS)'
    
    layout = {
      "dragmode": "zoom", 
    #  "hovermode": "x", 
    #  "legend": {"traceorder": "reversed"}, 
    #  "margin": {
    #    "t": 100, 
    #    "b": 100
    #  }, 
      'legend': {
        'x': -.17,
        'y': 1.2#,
#        'traceorder': 'reversed'
      },
      'title': title,
      'hovermode': 'closest',
      "xaxis": {
        "autorange": True,
        "range": [min(dates), max(dates)],
        "rangeselector": {
          'buttons': [
                   dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                        label='YTD',
                        step='year',
                        stepmode='todate'),
                    dict(count=1,
                        label='1y',
                        step='year',
                        stepmode='backward'),
                    dict(step='all')
                ]
        },
        "rangeslider": {
          "autorange": True,
          "range": [min(dates), max(dates)]
        },
        "type": "date"
      },    
      "yaxis": {
        "anchor": "x", 
        "autorange": True, 
        "domain": [0, 1], 
        "linecolor": '#000000', 
        "mirror": True, 
        "range": [-60.0858369099, 28.4406294707], 
        "showline": True, 
        "side": "right", 
        "tickfont": {"color": '#000000'}, 
        "tickmode": "auto", 
        "ticks": "",
        "title": y_title,
        "titlefont": {"color": '#000000'}, 
        "type": "linear", 
        "zeroline": False
      }
    }
    fig = go.Figure(data=data, layout=layout)
    py2.offline.plot(fig, auto_open=True, filename='Trend ({} - {}).html'.format(dates_title[0], dates_title[1]), image_filename='Trend')

class app():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Air Canada Trends")
        self.window.iconbitmap('aircanadaicon.ico')       
        self.create_widgets()
        self.window.grid()

        self.radio_variable = tk.StringVar()
        self.combobox_value = tk.StringVar()
        self.window.protocol("WM_DELETE_WINDOW", lambda: on_exit(self.window))

    def create_widgets(self):
        # Create some room around all the internal frames

        # - - - - - - - - - - - - - - - - - - - - -
        # The Commands frame
        # cmd_frame = ttk.LabelFrame(self.window, text="Commands", padx=5, pady=5, relief=tk.RIDGE)
        cmd_frame = ttk.LabelFrame(self.window, text="CT Tests", relief=tk.RIDGE)
        cmd_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button1 = ttk.Button(cmd_frame,
                         text="TDS",
                         command=lambda: plotter('CT', 'TDS'))  
        #    button1.pack(side=LEFT)
        button2 = ttk.Button(cmd_frame,
                                 text="ORP",
                                 command= lambda: plotter('CT','ORP'))
        #    button2.pack(side=LEFT)
        button3 = ttk.Button(cmd_frame,
                                 text="pH",
                                 command=lambda: plotter('CT','pH'))  
        #    button3.pack(side=LEFT)
        button10 = ttk.Button(cmd_frame,
                                 text="M. Alk",
                                 command=lambda: plotter('CT','malk'))  
        #    button10.pack(side=LEFT)
        button4 = ttk.Button(cmd_frame,
                                 text="PO4 & PhO4",
                                 command=lambda: plotter('CT','po4')) 
        #    button4.pack(side=LEFT)
        button5 = ttk.Button(cmd_frame,
                                 text="Chlorine",
                                 command=lambda: plotter('CT','cl'))  
        #    button5.pack(side=LEFT)
        button6 = ttk.Button(cmd_frame,
                                 text="Fe/Iron",
                                 command=lambda: plotter('CT','fe'))  
        #    button6.pack(side=LEFT)
        button7 = ttk.Button(cmd_frame,
                                 text="Cu/Copper",
                                 command=lambda: plotter('CT','Cu'))  
        #    button7.pack(side=LEFT)
        button8 = ttk.Button(cmd_frame,
                                 text="Hardness",
                                 command=lambda: plotter('CT','Hardness'))  
        #    button8.pack(side=LEFT)
        button9 = ttk.Button(cmd_frame,
                                 text="Zn/Zinc",
                                 command=lambda: plotter('CT','Zn'))   
        button14 = ttk.Button(cmd_frame,
                                 text="FATP & TATP",
                                 command=lambda: plotter('CT','atp'))  
        button15 = ttk.Button(cmd_frame,
                         text="Conductivity",
                         command=lambda: plotter('CT','cond')) 
        
        button1.grid(row=0, column=0, rowspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button2.grid(row=0, column=1, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button3.grid(row=0, column=2, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button4.grid(row=0, column=3, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button5.grid(row=0, column=4, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button6.grid(row=0, column=5, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button7.grid(row=1, column=0, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button8.grid(row=1, column=1, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button9.grid(row=1, column=2, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button14.grid(row=1, column=3, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button15.grid(row=1, column=4, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button10.grid(row=1, column=5, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)

        # - - - - - - - - - - - - - - - - - - - - -
        # The Data entry frame
        entry_frame = ttk.LabelFrame(self.window, text="CL Tests",
                                     relief=tk.RIDGE)
        entry_frame.grid(row=2, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        button11 = ttk.Button(entry_frame,
                                 text="Closed Loop TDS",
                                 command=lambda: plotter('CL','cltds'))  
        button12 = ttk.Button(entry_frame,
                                 text="Closed Loop pH",
                                 command=lambda: plotter('CL','clph')) 
        button13 = ttk.Button(entry_frame,
                                 text="Closed Loop Nitrite",
                                 command=lambda: plotter('CL','nitrite'))
        button16 = ttk.Button(entry_frame,
                                 text="Closed Loop Cu",
                                 command=lambda: plotter('CL','clcu'))
        button17 = ttk.Button(entry_frame,
                                 text="Closed Loop Fe",
                                 command=lambda: plotter('CL','clfe'))
        button11.grid(row=0, column=0, rowspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button12.grid(row=0, column=1, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button13.grid(row=0, column=2, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button16.grid(row=0, column=3, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)
        button17.grid(row=0, column=4, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)

        # - - - - - - - - - - - - - - - - - - - - -
        # Menus
        menubar = tk.Menu(self.window)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=lambda: on_exit(self.window))
        filemenu.add_command(label = 'Change file directory', command=change_directory)
        filemenu.add_command(label = 'Change CT sample entries', command =lambda: change_samples('ct'))
        filemenu.add_command(label = 'Change CL sample entries', command =lambda: change_samples('cl'))
        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)

        # - - - - - - - - - - - - - - - - - - - - -


class listbox():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('CT Sample Entries')
        self.args = choice
        self.window.grid()
        self.InitResizing()
        self.CreateWidgets()
        self.window.protocol("WM_DELETE_WINDOW", lambda: on_exit(self.window))
        
    def InitResizing(self):
        """Initialize the Resizing of the Window"""
        top=self.window.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(6, weight=1)
       
    def CreateWidgets(self):
        """Create all the widgests that we need"""
                       
        """Create the Text"""
        box1Text = ttk.LabelFrame(self.window, text="Sample Labels:")
        box1Text.grid(row=0, column=0, sticky=tk.W+ tk.N)
        box2Text = ttk.LabelFrame(self.window, text="Alternative Sample Names:")
        box2Text.grid(row=0, column=6, sticky=tk.W+ tk.N)
        
        """Create the First ListBox"""
        scrollbarV = tk.Scrollbar(box1Text, orient=tk.VERTICAL)
        
        self.samplenames = tk.Listbox(box1Text, selectmode=tk.BROWSE
                                , yscrollcommand=scrollbarV.set
                                , relief=tk.SUNKEN)
        self.samplenames.grid(row=1, column=0, columnspan=4, sticky=tk.N+tk.W+tk.S+tk.E)
        def onselect(evt):
            global index_selected
            # Note here that Tkinter passes an event object to onselect()
            w = evt.widget
            try:
                index_selected = int(w.curselection()[0])
            except IndexError:
                pass
            if self.args == 'ct':
                self.samplealtnames.delete(0,tk.END)
                for item in alt_labels[index_selected]:
                    self.samplealtnames.insert(tk.END, item)
            if self.args == 'cl':
                self.samplealtnames.delete(0,tk.END)
                for item in alt_cl_labels[index_selected]:
                    self.samplealtnames.insert(tk.END, item)
        
        self.samplenames.bind('<<ListboxSelect>>', onselect)
        """Show the scrollbars and attatch them"""
        scrollbarV.grid(row=1, column=4, sticky=tk.N+tk.S)
        scrollbarV.config(command=self.samplenames.yview)
        
        def save_list():
            global labels, labels_sub, cl_labels, cl_labels_sub, alt_labels, alt_cl_labels
            # get a list of listbox lines
            temp_list1 = list(self.samplenames.get(0, tk.END))
            temp_list2 = list(self.samplealtnames.get(0, tk.END))
            if self.args == 'ct':
                labels = sorted(temp_list1, key = lambda x: x[:3].lower())
                alt_labels.pop(index_selected)
                alt_labels.append(temp_list2)
                alt_labels = sorted(alt_labels, key = lambda x: x[0][:3].lower())
                labels_sub = [item[:3].lower() for item in labels]
                for i in range(len(labels)):
                    config.set('CT Labels', labels[i], alt_labels[i])
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
            if self.args == 'cl':
                cl_labels = sorted(temp_list1, key = lambda x: x[:3].lower())
                alt_cl_labels.pop(index_selected)
                alt_cl_labels.append(temp_list2)
                alt_cl_labels = sorted(alt_cl_labels, key = lambda x: x[0][:3].lower())
                labels_sub = [item[:3].lower() for item in labels]
                for i in range(len(cl_labels)):
                    config.set('CL Labels', cl_labels[i], alt_cl_labels[i])
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
                
        def add_item(*args):
            if text_entry.get() != '':
                args[0].insert(tk.END, text_entry.get())
                text_entry.delete(0, tk.END)
        def delete_item(*args):
            try:
                # get selected line index
                index = args[0].curselection()[0]
                args[0].delete(index)
            except IndexError:
                pass
        entry_frame = ttk.LabelFrame(self.window,labelwidget = box1Text,
                                     relief=tk.RIDGE)
        entry_frame.grid(row=3, column=0, sticky=tk.E + tk.W+ tk.N + tk.S)
        """Create the Add, Remove, Edit, and View Buttons"""
        self.btnAdd = tk.Button(entry_frame, text="+", command = lambda: add_item(self.samplenames))
        self.btnAdd.grid(column=1, row=3, stick=tk.E, pady=5)
        self.btnRemove = tk.Button(entry_frame, text="-", command = lambda: delete_item(self.samplenames))
        self.btnRemove.grid(column=2, row=3, stick=tk.E, pady=5)
        
        """Create a frame for space between the two items"""
        
        """Create the Second ListBox"""
        scrollbarV = tk.Scrollbar(box2Text, orient=tk.VERTICAL)

        
        self.samplealtnames = tk.Listbox(box2Text, selectmode=tk.BROWSE
                                , yscrollcommand=scrollbarV.set
                                , relief=tk.SUNKEN)
        self.samplealtnames.grid(row=1, column=6, sticky=tk.N+tk.W+tk.S+tk.E)
        """Show the scrollbars and attatch them"""
        scrollbarV.grid(row=1, column=7, sticky=tk.N+tk.S)
        scrollbarV.config(command=self.samplealtnames.yview)
        entry_frame3 = ttk.Frame(self.window,#labelwidget = box2Text,
                                     relief=tk.FLAT)
        entry_frame3.grid(row=4, column=0, columnspan=8,sticky=tk.E + tk.W + tk.S)
        text_entry = ttk.Entry(entry_frame3, width = 40)
        text_entry.grid(row = 4, column=1, sticky = tk.E)
        text_label = tk.Label(entry_frame3, text="Sample:")
        text_label.grid(row=4, column=0, sticky=tk.W)
        self.btnEdit = tk.Button(entry_frame3, text="Save", command=save_list)
        self.btnEdit.grid(row=4,column=10, stick=tk.E)
               
        """Create the Set TextButton"""
        entry_frame2 = ttk.LabelFrame(self.window,labelwidget = box2Text,
                                     relief=tk.RIDGE)
        entry_frame2.grid(row=3, column=6, columnspan = 4, sticky=tk.E + tk.W+ tk.N + tk.S)
        """Create the Add, Remove, Edit, and View Buttons"""
        self.btnAdd = tk.Button(entry_frame2, text="+", command = lambda: add_item(self.samplealtnames))
        self.btnAdd.grid(column=20, row=3, stick=tk.E, pady=5)
        self.btnRemove = tk.Button(entry_frame2, text="-", command = lambda: delete_item(self.samplealtnames))
        self.btnRemove.grid(column=10, row=3, stick=tk.E, pady=5)
        
        
        """Just fill up the listbox with some numbers"""
        

        if self.args == 'ct':
            for item in labels:
                self.samplenames.insert(tk.END, item)
        if self.args == 'cl':
            for item in cl_labels:
                self.samplenames.insert(tk.END, item)

# Create the entire GUI program
program = app()



# Start the GUI event loop
program.window.mainloop()


