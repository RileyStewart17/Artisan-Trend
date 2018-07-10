import plotly.plotly as py
import plotly as py2
import plotly.graph_objs as go
import numpy as np
from os import listdir
from os.path import isfile, join

# Created by Riley Stewart for Artisan Engineering.
# Not to be copied, used, or revised without explicit written 
# permission from the author and Artisan Engineering.

import xlrd
from tkinter import filedialog
from tkinter import *
from datetime import datetime
from tkinter.filedialog import askdirectory
from tkinter import messagebox

## ADD test not present to group, add labeling system to CL samples,
## fix settings.txt to include, prompt user if new sample found
## Append to CTdata/CLdata if only one table present

#----------------------------------------------------------------------

# This loads the directory of the files + the sample names for future use. The
# script first trys to open the 'settings.txt' file to pull the directory; if
# such a file doesn't exist, the user is prompted to select directory using a menu.
# The 'settings.txt' file is then created with the directory stored. The labels
# for the samples are then pulled from the settings file. 


try:
    with open ("settings.txt", "r") as myfile:
        data=myfile.readlines()
    dirname = data[0][:-1]
except:
    root = Tk()
    root.withdraw()
    messagebox.showinfo('Air Canada Trends', 'Please select the folder that contains the excel report files.')
    dirname = askdirectory(parent=root,initialdir="/",title='Please select a directory')+'/'
    root.destroy()
    with open("settings.txt", "w") as text_file:
        text_file.write(dirname+'\n')

labels = []  # full labels of samples
labels_sub = [] # First three letters of each sample name (for sorting)
try:
    with open("settings.txt", "r") as text_file:
        temp = data[1:]
        for i in range(len(temp)):
            labels.append(temp[i][:-1])
            labels_sub.append(labels[i][:3].lower())
except:
    pass

ACdir = dirname

onlyfilesAC = [f for f in listdir(ACdir) if isfile(join(ACdir, f))] # List of files present in directory
onlyfilesAC = [i for i in onlyfilesAC if 'xlsx' in i] # grabs list of files present in directory that are excel worksheets


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
    ban1 = ['target', 'Target']  # Contains banned strings
    d={} # create dictionary to contain CTdata
    c=0  # This are all used as indexes later on, reset to 0
    v=0
    t=0
    
    labels_loc = []    # List to contain sample names in file
    labels_loc_3 = []  # List to contain first three letters of sample names (for sorting)
    done = False       # Boolean value used later

    for i in range(100):
        x = file.row_values(i)   #pulls rows in file, one at a time looking for data table
        if 'Sample' in x:
            v = i  # index of row containing all table headers (test names)
            break
    for i in range(10):  # Looking for CT samples under the table header 'Sample'
        x = file.row_values(v+i+1)
        if x[0] not in ['', 'target', 'Target']:                # If string in column 1 is
            d["data{0}".format(i)]=np.array(x)                  # not in banned strings,
            strin = d["data{0}".format(i)][0].split(' ',1)[0]   # grab data, and append sample name
            labels_loc.append(d["data{0}".format(i)][0])        # to labels_loc, and first three letters
            labels_loc_3.append(strin[:3].lower())              # of sample name to labels_loc_3
        if x[0] in ban1:
            c = i
            break  # Break parsing through the CT samples if 'Target' is found.
        c = i   
    CTvariables = np.array(file.row_values(v))
    CTdata = list(d.values())
    for i in range(4):
        x = file.row_values(c+v+1+i)
        if 'Sample' in x:
            t = i+c+v+1
            d2 = {}
            variables2 = np.array(file.row_values(t))
            for i1 in range(len(CTdata)+1):
                x = file.row_values(t+1+i1)
                if x[0] not in ['', 'target', 'Target']:
                    d2["data{0}".format(i1)] = np.array(x)
                if x[0] in ban1:
                    t2 = t+2+i1
                    break
                t2 = t+2+i1
            data2 = list(d2.values())
            lis = []
            lis2 = [item[0] for item in CTdata]
            stacked = False
            for i2 in range(len(data2)):
                if data2[i2][0] in lis2:
                    ind = np.where(np.array(lis2) == data2[i2][0])[0][0]
                    lis.append(np.concatenate((CTdata[ind], data2[i2][1:])))
                    stacked = True
            if not stacked:
                for l in range(5):
                    for o in range(len(CTvariables)):
                        if variables2[o] != CTvariables[o]:
                            ind_sort = np.where(np.array(CTvariables) == variables2[o])[0]
                            if len(ind_sort) == 0:  ##ADD to data if not present
                                variables2[o] = ''
                                data2[i2][o] == ''
                            else:
                                variables2[o], variables2[ind_sort[0]] = variables2[ind_sort[0]], variables2[o]
                                for v in range(len(data2)):
                                    data2[v][o], data2[v][ind_sort[0]] = data2[v][ind_sort[0]], data2[v][o]
                for i2 in range(len(data2)):
                    CTdata.append(data2[i2])
                    strin = data2[i2][0].split(' ',1)[0]
                    labels_loc.append(data2[i2][0])      
                    labels_loc_3.append(strin[:3].lower())
                        
            if stacked:
                CTvariables = np.concatenate((CTvariables, variables2[1:]))
                CTdata = lis
                
            for i3 in range(100):
                x = file.row_values(t2+i3)
                if 'Sample' in x:
                    w = i3+t2
                    break
            CLvariables = np.array(file.row_values(w))
            d3 = {}
            for i4 in range(15):
                x = file.row_values(w+i4+1)
                if x[0] not in ['', 'target', 'Target']:
                    d3["data{0}".format(i4)]=np.array(x)
                if x[0] in ban1:
                    break 
            CLdata = list(d3.values())
            done = True
    if not done:
        for i5 in range(100):
            x = file.row_values(c+v+i5)
            if 'Sample' in x:
                v = i5+c+v
                break
        CLvariables = np.array(file.row_values(v))
        d3 = {}
        for i6 in range(15):
            x = file.row_values(v+i6+1)
            if x[0] not in ['', 'target', 'Target']:
                d3["data{0}".format(i6)]=np.array(x)
            if x[0] in ban1:
                break 
        CLdata = list(d3.values())
    if len(labels_sub) != 0:
        if set(labels) != set(labels_loc):
            if set(labels_sub) != set(labels_loc_3):
                missing_samples = np.setdiff1d(labels_sub,labels_loc_3)
                for v in range(len(missing_samples)):
                    ind_lab = np.where(np.array(labels_sub) == missing_samples[v])[0][0]
                    labels_loc_3.append(missing_samples[v])
                    fill = ['' for x in range(len(AClist))]
                    fill[0] = labels[ind_lab]
                    labels_loc.append(labels[ind_lab])
                    CTdata.append(fill)
                if set(labels) != set(labels_loc):
                    wrong_names = np.setdiff1d(labels_loc, labels)
                    diff_names = np.setdiff1d(labels, labels_loc)
                    for v in range(len(wrong_names)):
                        ind_lab = np.where(np.array(labels_loc) == wrong_names[v])[0][0]
                        CTdata = [[x.replace(wrong_names[v], diff_names[v]) for x in i] for i in CTdata]
                        labels_loc = [i.replace(wrong_names[v], diff_names[v])for i in labels_loc] 
            else:
                wrong_names = np.setdiff1d(labels_loc, labels)
                diff_names = np.setdiff1d(labels, labels_loc)
                for v in range(len(wrong_names)):
                    ind_lab = np.where(np.array(labels_loc) == wrong_names[v])[0][0]
                    CTdata = [[x.replace(wrong_names[v], diff_names[v]) for x in i] for i in CTdata]
                    labels_loc = [i.replace(wrong_names[v], diff_names[v])for i in labels_loc]                   
    together = zip(labels_loc, CTdata)
    sorted_together =  sorted(together, key=lambda x: x[0].lower())     
    labels_loc = [x[0] for x in sorted_together]
    CTdata = [x[1] for x in sorted_together]


    return CTvariables, CTdata, CLvariables, CLdata
 
#----------------------------------------------------------------------
    

colors = ['#4285F4', '#FBBC05', '#34A853', '#EA4335', '#964f8e', '#33cccc']
colors_alt = ['#00A1F1', '#e06000', '#A4C639', '#EA4335', '#EA4335', '#EA4335']    
        
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
        #cell = first_sheet.cell(0,0)
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
    elif 'report' in filename:
        date_str = filename.split('report')[1][:-5]
        return datestr

dates = []
            
for i in range(len(onlyfilesAC)):
    dates.append(date(onlyfilesAC[i]))
date_temp = zip(dates, AClist)
date_temp_sorted =  sorted(date_temp, key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))
dates = [x[0] for x in date_temp_sorted]
AClist = [x[1] for x in date_temp_sorted]
    

def plotter(system, test):
    datadict = {}
    datadict2 = {}
    
    ban = ('', 'system drained', '-', 'drained')
    ban2 = ('>', '<')
    keysnom = ('TDS', 'ORP', 'Cu', 'Zn', 'pH')
    NumCT = []
    
    if system == 'CT':
        for i in range(len(AClist)):
            x = len(pulldata(AClist[i])[1])
            NumCT.append(x)
        NCT = max(NumCT)
        maxindCT = np.where(np.array(NumCT) == NCT)[0][0]
        labels = []
        for i in range(NCT):
            labels.append(pulldata(AClist[maxindCT])[1][i][0])
        
        #totdata = np.array([NCT,len(AClist)])
        for i in range(NCT):
            data = []
            data2 = []

            if test in keysnom:
                name = test
                for t in range(len(AClist)):  
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where(pulldata(AClist[t])[0] == test)[0][0]
                        u1 = d1[ind]
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
        
            if test.lower() == 'cl':
                name = 'Cl'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((pulldata(AClist[t])[0] == 'Free Cl') | (pulldata(AClist[t])[0] == 'Cl'))[0][0]
                        u1 = d1[ind]
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
            
            if test.lower() == 'malk':
                name = 'M. Alk'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((pulldata(AClist[t])[0] == 'M. Alk') | (pulldata(AClist[t])[0] == 'Alkalinity') | (pulldata(AClist[t])[0] == 'Alk.'))[0][0]
                        u1 = d1[ind]
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
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
                        ind = np.where(pulldata(AClist[t])[0] == 'PO4')[0][0]
                        u1 = d1[ind]
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                for t in range(len(AClist)):
                    try:
                        d2 = pulldata(AClist[t])[1][i]
                        ind = np.where(pulldata(AClist[t])[0] == 'PhO4')[0][0]
                        u2 = d2[ind]
                        if u2 in ban:
                            u2 = np.nan
                        elif u2[0] in ban2:
                            u2 = u1[1:]
                        data2.append(float(u2))
                    except:
                        data2.append(np.nan)
                        pass    
                    
            if test.lower() in ('fe', 'iron'):
                name = 'Fe'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((pulldata(AClist[t])[0] == 'Fe') | (pulldata(AClist[t])[0] == 'Iron'))[0][0]
                        u1 = d1[ind]
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                    
            if test.lower() in ('hardness', 'ca', 'ca hardness', 'mg hardness', 'total hardness'):
                name = 'Ca'
                name2 = 'Mg'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[1][i]
                        ind = np.where((pulldata(AClist[t])[0] == 'Ca Hardness') | (pulldata(AClist[t])[0] == 'Ca'))[0][0]
                        u1 = d1[ind]
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                for t in range(len(AClist)):
                    try:
                        d2 = pulldata(AClist[t])[1][i]
                        ind = np.where((pulldata(AClist[t])[0] == 'Mg Hardness') | (pulldata(AClist[t])[0] == 'Mg'))[0][0]
                        u2 = d2[ind]
                        if u2 in ban:
                            u2 = np.nan
                        elif u2[0] in ban2:
                            u2 = u1[1:]
                        data2.append(float(u2))
                    except:
                        data2.append(np.nan)
                        pass

            datadict["data{0}".format(i)] = np.array(data)
            if len(data2) != 0:
                datadict2["data{0}".format(i)] = np.array(data2)
            
                

    if system == 'CL':
        for i in range(len(AClist)):
            x = len(pulldata(AClist[i])[3])
            NumCT.append(x)
        NCT = max(NumCT)
        maxindCL = np.where(np.array(NumCT) == NCT)[0][0]
        labels = []
        for i in range(NCT):
            labels.append(pulldata(AClist[maxindCL])[3][i][0])
        #totdata = np.array([NCT,len(AClist)])
        for i in range(NCT):
            data = []
            data2 = []
            if test.lower() in ('nitrite'):
                name = 'Nitrite'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[3][i]
                        ind = np.where(pulldata(AClist[t])[2] == 'Nitrite')[0][0]
                        u1 = d1[ind]
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                    
            if test.lower() in ('cltds'):
                name = 'TDS'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[3][i]
                        ind = np.where(pulldata(AClist[t])[2] == 'TDS')[0][0]
                        u1 = d1[ind]
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
                        data.append(float(u1))
                    except:
                        data.append(np.nan)
                        pass
                    
            if test.lower() in ('clpH'):
                name = 'pH'
                for t in range(len(AClist)):
                    try:
                        d1 = pulldata(AClist[t])[3][i]
                        ind = np.where(pulldata(AClist[t])[2] == 'pH')[0][0]
                        u1 = d1[ind]
                        if u1 in ban:
                            u1 = np.nan
                        elif u1[0] in ban2:
                            u1 = u1[1:]
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
        axis_num = 'y'
        if c > 0:
            axis_num = 'y' + str(c+1)
            
        trace = go.Scatter(
             x = dates, 
            y = datadict['data{0}'.format(c)], 
            name = labels[c], 
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
                name = labels[c], 
                text = empt2, 
                yaxis = axis_num,
                marker = dict(
                    size = 8,
                    color = colors_alt[c],
                    )
            )
            data_sets2.append(trace2)
    
    return go.Data(data_sets), go.Data(data_sets2)

data = plotter('CT', 'TDS')[0]

# style all the traces
for k in range(len(data)):
    data[k].update(
        {
            "type": "scatter",
            "hoverinfo": "name+x+text",
            "line": {"width": 0.5}, 
            "marker": {"size": 8},
            "mode": "lines+markers",
            "showlegend": True
        }
    )

layout = {
#  "annotations": [
#    {
#      "x": "2013-06-01", 
#      "y": 0, 
#      "arrowcolor": "rgba(63, 81, 181, 0.2)", 
#      "arrowsize": 0.3, 
#      "ax": 0, 
#      "ay": 30, 
#      "text": "state1", 
#      "xref": "x", 
#      "yanchor": "bottom", 
#      "yref": "y"
#    }, 
#    {
#      "x": "2014-09-13", 
#      "y": 0, 
#      "arrowcolor": "rgba(76, 175, 80, 0.1)", 
#      "arrowsize": 0.3, 
#      "ax": 0,
#      "ay": 30,
#      "text": "state2",
#      "xref": "x", 
#      "yanchor": "bottom", 
#      "yref": "y"
#    }
#  ], 
  "dragmode": "zoom", 
#  "hovermode": "x", 
#  "legend": {"traceorder": "reversed"}, 
#  "margin": {
#    "t": 100, 
#    "b": 100
#  }, 
#  "shapes": [
#    {
#      "fillcolor": "rgba(63, 81, 181, 0.2)", 
#      "line": {"width": 0}, 
#      "type": "rect", 
#      "x0": "2013-01-15", 
#      "x1": "2013-10-17", 
#      "xref": "x", 
#      "y0": 0, 
#      "y1": 0.95, 
#      "yref": "paper"
#    }, 
#    {
#      "fillcolor": "rgba(76, 175, 80, 0.1)", 
#      "line": {"width": 0}, 
#      "type": "rect", 
#      "x0": "2013-10-22", 
#      "x1": "2015-08-05", 
#      "xref": "x", 
#      "y0": 0, 
#      "y1": 0.95, 
#      "yref": "paper"
#    }
#  ],
  'legend': {
    'x': -.17,
    'y': 1.2,
    'traceorder': 'reversed'
  },
#  'images': [{
#    'source': '/Users/riley/Documents/Work/ACtrendscript/'+ 'aritsan_logo.jpg',
#    'xref':"paper", 
#    'yref':"paper",
#    'x':1, 
#    'y':1.05,
#    'sizex': 0.2,
#    'sizey': 0.2,
#    'xanchor': "right",
#    'yanchor': "bottom"
#  }],
  'title': 'Plot',
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
    "title": "mg/L",
    "titlefont": {"color": '#000000'}, 
    "type": "linear", 
    "zeroline": False
  }, 
  "yaxis2": {
    "anchor": "x", 
    "autorange": True, 
    "domain": [1/len(data)+0.1*1/len(data), 2*1/len(data)-0.1*1/len(data)], 
    "linecolor": colors[1], 
    "mirror": True, 
    "range": [29.3787777032, 100.621222297], 
    "showline": True, 
    "side": "right", 
    "tickfont": {"color": colors[1]}, 
    "tickmode": "auto", 
    "ticks": "",
    "title": "mg/L",
    "titlefont": {"color": colors[1]}, 
    "type": "linear", 
    "zeroline": False
  }, 
  "yaxis3": {
    "anchor": "x", 
    "autorange": True, 
    "domain": [2*1/len(data)+0.1*1/len(data), 3*1/len(data)-0.1*1/len(data)], 
    "linecolor": colors[2], 
    "mirror": True, 
    "range": [-3.73690396239, 22.2369039624], 
    "showline": True, 
    "side": "right", 
    "tickfont": {"color": colors[2]}, 
    "tickmode": "auto", 
    "ticks": "", 
    "title": "mg/L", 
    "titlefont": {"color": colors[2]}, 
    "type": "linear", 
    "zeroline": False
  }, 
  "yaxis4": {
    "anchor": "x", 
    "autorange": True, 
    "domain": [3*1/len(data)+0.1*1/len(data), 4*1/len(data)-0.1*1/len(data)], 
    "linecolor": colors[3], 
    "mirror": True, 
    "range": [6.63368032236, 8.26631967764], 
    "showline": True, 
    "side": "right", 
    "tickfont": {"color": colors[3]}, 
    "tickmode": "auto", 
    "ticks": "", 
    "title": "mg/L", 
    "titlefont": {"color": colors[3]}, 
    "type": "linear", 
    "zeroline": False
  }, 
  "yaxis5": {
    "anchor": "x", 
    "autorange": True, 
    "domain": [4*1/len(data)+0.1*1/len(data), 5*1/len(data)-0.1*1/len(data)], 
    "linecolor": colors[4], 
    "mirror": True, 
    "range": [-685.336803224, 3718.33680322], 
    "showline": True, 
    "side": "right", 
    "tickfont": {"color": colors[4]}, 
    "tickmode": "auto",
    "ticks": "", 
    "title": "mg/L", 
    "titlefont": {"color": colors[4]}, 
    "type": "linear", 
    "zeroline": False
  }, 
  "yaxis6": {
    "anchor": "x", 
    "autorange": True, 
    "domain": [5*1/len(data)+0.1*1/len(data), 6*1/len(data)-0.1*1/len(data)], 
    "linecolor": colors[5], 
    "mirror": True, 
    "range": [-500, 3000], 
    "showline": True, 
    "side": "right", 
    "tickfont": {"color": colors[5]}, 
    "tickmode": "auto",
    "ticks": "", 
    "title": "mg/L", 
    "titlefont": {"color": colors[5]}, 
    "type": "linear", 
    "zeroline": False
  }
}
fig = go.Figure(data=data, layout=layout)

py2.offline.plot(fig, auto_open=False, filename='Trend.html', image_filename='Trend')