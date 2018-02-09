import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML
import math
import time

def animal_read(inpath, filename, sheet):
    '''
    Returns corresponding animals for sheets
    Reads data into dataframe with long header removed.
    Uses correct labels as column labels.
    Uses time as row indexes.
    '''
    filepath = os.path.join(inpath,filename)
    df = pd.read_excel(filepath,sheetname=sheet,skip_footer=35,index_col=0)
    group = df.iloc[33][0]
    animal = df.iloc[32][0]
    context = df.iloc[10][0]
    print(filename + " " + sheet + " is " + animal + " in " + context)

    df = pd.read_excel(filepath,sheetname=sheet,skiprows=36,index_col=0,headers=0)
    df = df[1:]
    df.replace(to_replace='-',value=0,inplace=True)
    return(animal,context,group,df)

def find_tones(df, ntones):
    '''
    Creates dictionary of each tone. Values are
    dataframes for times at which each tone == 1.
    '''
    tones = {}
    i = 1
    while i <= ntones: # number of tones
        num = str(i)
        label = 'Tone ' + num
        tone = pd.DataFrame(df[df[label] == 1])
        tones[i] = tone
        i += 1
    return(tones)

def find_pretones(df, ntones):
    '''
    Creates dictionary of each pretone. Values
    are dataframes for 30s before tone == 1
    '''
    pretones = {}
    i = 1
    while i<= ntones:
        num = str(i)
        label = 'Tone ' + num #Column label for each tone

        tone = df[df[label] == 1] #Tone dataframe
        tonestart = tone.iloc[0] #Time for tone start

        starttime = math.floor(tonestart['Recording time']-30) #Time for pretone start
        endtime = math.floor(tonestart['Recording time']) #Time for pretone end
        itime = df.index.get_loc(starttime,method='bfill') #Index for pretone start
        etime = df.index.get_loc(endtime,method='bfill') #Index for pretone end

        pretone = df.iloc[itime:etime] #df for pretone
        pretones[i] = pretone #dictionary for all pretones
        i += 1
    return(pretones)

def find_shock_responses(df, ntones):
    '''
    Creates dictionary of each shock response. Values
    are dataframes for 5s after tone == 1
    '''
    sresponses = {}
    i = 1
    while i<= ntones:
        num = str(i)
        label = 'Tone ' + num #Column label for each tone

        tone = df[df[label] == 1] #Tone dataframe
        toneend = tone.iloc[-1] #Time for tone end

        starttime = math.floor(toneend['Recording time']) #Time for sresponse start
        endtime = math.floor(toneend['Recording time'] + 5) #Time for sresponse end
        itime = df.index.get_loc(starttime,method='bfill') #Index for sresponse start
        etime = df.index.get_loc(endtime,method='bfill') #Index for sresponse end

        sresponse = df.iloc[itime:etime] #df for sresponse
        sresponses[i] = sresponse #dictionary for all sresponse
        i += 1
    return(sresponses)

def find_postshocks(df, ntones):
    '''
    Creates dictionary of each postshock. Values
    are dataframes for 5s to 30s after tone == 1
    '''
    pshocks = {}
    i = 1
    while i<= ntones:
        num = str(i)
        label = 'Tone ' + num #Column label for each tone

        tone = df[df[label] == 1] #Tone dataframe
        toneend = tone.iloc[-1] #Time for tone end

        starttime = math.floor(toneend['Recording time'] + 5) #Time for pshock start
        endtime = math.floor(toneend['Recording time'] + 35) #Time for pshock end
        itime = df.index.get_loc(starttime,method='bfill') #Index for pshock start
        etime = df.index.get_loc(endtime,method='bfill') #Index for pshock end

        pshock = df.iloc[itime:etime] #df for pshock
        pshocks[i] = pshock #dictionary for all sresponse
        i += 1
    return(pshocks)

def get_means(datadict,timebin, ntones):
    '''
    Returns a dataframe of mean velocity of timebin at each tone.
    '''
    meanlist = []
    i = 1
    while i <= ntones:
        epoch = datadict[i]
        vels = epoch['Velocity']
        mean = round(np.mean(vels),3)
        meanlist.append(mean)
        i += 1
    means = pd.DataFrame(meanlist,columns=[timebin + ' Mean Velocity'])
    means.index = np.arange(1, len(meanlist) + 1)
    return(means)

def get_meds(datadict,timebin, ntones):
    '''
    Returns a dataframe of median velocity of timebin at each tone.
    '''
    medlist = []
    i = 1
    while i <= ntones:
        epoch = datadict[i]
        vels = epoch['Velocity']
        med = round(np.median(vels),3)
        medlist.append(med)
        i += 1
    meds = pd.DataFrame(medlist,columns=[timebin + ' Median Velocity'])
    meds.index = np.arange(1, len(meds) + 1)
    return(meds)

def get_SEMs(datadict,timebin, ntones):
    '''
    Returns a dataframe of median velocity of timebin at each tone.
    '''
    SEMlist = []
    i = 1
    while i <= ntones:
        epoch = datadict[i]
        vels = epoch['Velocity']
        SEM = round(np.std(vels),3)
        SEMlist.append(SEM)
        i += 1
    SEMs = pd.DataFrame(SEMlist,columns=[timebin + 'SEM'])
    SEMs.index = np.arange(1, len(SEMs) + 1)
    return(SEMs)

def get_vels(df, ntones):
    '''
    Creates data of all velocities from original dataframe for plotting.
    '''
    tonevels = {}
    i = 1
    while i <= ntones: # number of tones
        vels = []
        num = str(i)
        label = 'Tone ' + num
        tone = pd.DataFrame(df[df[label] == 1])
        vels.append(tone['Velocity'])
        tonevels[i] = vels
        i += 1
    return(tonevels)

def get_top_vels(datadict,nmax, ntones):
    '''
    Returns dataframe of nmax (int) maximum velocities for a timebin.
    The second section adds a column for an average of the maxima.
    '''
    nmaxes = pd.DataFrame()
    i = 1
    while i <= ntones:
        epoch = datadict[i]
        vels = epoch['Velocity']
        vlist = vels.tolist()
        vlist.sort()
        topvels = pd.DataFrame([vlist[-nmax:-1]])
        nmaxes = nmaxes.append(topvels)
        i += 1

    nmaxes.index = np.arange(1, nmaxes.shape[0] + 1)
    nmaxes.columns = np.arange(1, nmaxes.shape[1] + 1)

    nmaxes['Mean'] = nmaxes.mean(axis = 1)

    return(nmaxes)

def find_tone_vels(df,i):
    '''
    '''
    tone = pd.DataFrame()
    num = str(i)
    label = 'Tone ' + num
    tone = pd.DataFrame(df[df[label] == 1])

    tone = tone['Velocity']
    return(tone)

def find_shock_vels(df, i):
    '''
    '''
    sresponse = pd.DataFrame()
    num = str(i)
    label = 'Tone ' + num

    tone = df[df[label] == 1] #Tone dataframe
    toneend = tone.iloc[-1] #Time for tone end

    starttime = math.floor(toneend['Recording time']) #Time for sresponse start
    endtime = math.floor(toneend['Recording time'] + 5) #Time for sresponse end
    itime = df.index.get_loc(starttime,method='bfill') #Index for sresponse start
    etime = df.index.get_loc(endtime,method='bfill') #Index for sresponse end

    sresponse = df.iloc[itime:etime] #df for sresponse
    sresponse = sresponse['Velocity']

    return(sresponse)

def scaredy_read_FC(csv_dir):
    meancsv = []
    SEMcsv = []
    medcsv = []

    for file in os.listdir(csv_dir):
        if file.startswith("FC-mean-"):
            f = os.path.join(csv_dir, file)
            meancsv.append(f)
        if file.startswith("FC-SEM-"):
            f = os.path.join(csv_dir, file)
            SEMcsv.append(f)
        if file.startswith("FC-med-"):
            f = os.path.join(csv_dir,file)
            medcsv.append(f)
    return(meancsv,SEMcsv,medcsv)

def scaredy_read_ext(csv_dir):
    meancsv = []
    SEMcsv = []
    medcsv = []

    for file in os.listdir(csv_dir):
        if file.startswith("ext-mean-"):
            f = os.path.join(csv_dir, file)
            meancsv.append(f)
        if file.startswith("ext-SEM-"):
            f = os.path.join(csv_dir, file)
            SEMcsv.append(f)
        if file.startswith("ext-med-"):
            f = os.path.join(csv_dir,file)
            medcsv.append(f)
    return(meancsv,SEMcsv,medcsv)

def get_anim(csv, n):
    m = re.split('[-.]', csv)
    anim = m[n]
    return(anim)

def compress_FC_data(csvlist,tbin):
    '''
    tbins:
    0 = tone
    1 = pretone
    2 = shock
    3 = postshock
    '''
    allanims = pd.DataFrame()
    for csv in csvlist:
        anim = get_anim(csv,2)
        df = pd.read_csv(csv,index_col=0).transpose()

        tonevels = pd.DataFrame(df.iloc[tbin]).transpose()
        tonevels.set_index([[anim]],inplace=True)

        allanims = pd.concat([allanims,tonevels])
    return(allanims)

def concat_FC_data(means, SEMs, meds, ntones):
    allData = pd.DataFrame()

    for n in range(ntones):
        allData = allData.append(means.iloc[:,n])
        allData = allData.append(SEMs.iloc[:,n])
        allData = allData.append(meds.iloc[:,n])

    ix = []
    for n in range(ntones):
        ix.append('Tone {} Mean'.format(n+1))
        ix.append('Tone {} SEM'.format(n+1))
        ix.append('Tone {} Median'.format(n+1))

    allData.index = ix
    allData = allData.transpose()

    return(allData)

def scaredy_read_FC_max(csv_dir):
    maxToneCSV = []
    maxPretoneCSV = []
    maxShockCSV = []
    maxPostshockCSV = []

    for file in os.listdir(csv_dir):
        if file.startswith("FC-tone-max-"):
            f = os.path.join(csv_dir, file)
            maxToneCSV.append(f)
        if file.startswith("FC-pretone-max-"):
            f = os.path.join(csv_dir, file)
            maxPretoneCSV.append(f)
        if file.startswith("FC-shock-max-"):
            f = os.path.join(csv_dir,file)
            maxShockCSV.append(f)
        if file.startswith("FC-shock-max-"):
            f = os.path.join(csv_dir,file)
            maxPostshockCSV.append(f)
    return(maxToneCSV, maxPretoneCSV, maxShockCSV, maxPostshockCSV)

def compress_FC_max_data(csvlist):
    anims = []
    maxVels = pd.DataFrame()

    for csv in csvlist:
        anim = get_anim(csv,4)
        anims.append(anim)

        df = pd.read_csv(csv,index_col=0).transpose()
        df = df.iloc[-1,:]
        maxVels = maxVels.append(df)

    maxVels.index = anims
    return(maxVels)
