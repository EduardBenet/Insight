from datetime import datetime
from collections import OrderedDict
from itertools import islice
import sys 

#Create function that finds closed sessions due to inactivity,
#writes output lines, and removes the data from our current
#dictionaries
def addline(new_dict,in_p):
    #Loop over the all the active logs
    for t, v in new_dict.items():
        tdelta = CurrTime - v[1] #Find the elapsed time
        if tdelta.seconds>in_p:  #If the elapsed time is bigger than in_p close session
            TotalTime = v[1] - v[0]  #Determine total activity time for output
            # Write output
            file.write('{0},{1},{2},{3},{4}\n'.format(t,v[0].strftime(tformat),v[1].strftime(tformat),TotalTime.seconds+1,v[2]))
            #Delete closed session
            del new_dict[t]
    return new_dict
#Get the inactivity period (in_p) value in seconds
in_p = open(sys.argv[2],'r')
in_p = int(in_p.read())

#Open file with data in read mode
INFO = open(sys.argv[1],'r')

#Create string format to process strings into time objects
tformat = '%Y-%m-%d %H:%M:%S'

#Open output file
file = open(sys.argv[3],'w')

#Find the column number for all fields of interest
for lines in islice(INFO,0,1):
    entry = lines.split(',') #csv file has fields separated by comas, split each line into the fields
    entry = [x.lower() for x in entry] #Lowercase all fields, to avoid any error when checking for the field e.g. (IP \neq ip)
    #Find columns of all fields of interest
    ip = entry.index('ip')
    date = entry.index('date')
    tim = entry.index('time')
    cik = entry.index('cik')
    acc = entry.index('accession')
    ext = entry.index('extention')

#Create ordered dictionary to store the data, important since the log order is later used
new_dict = OrderedDict()

#Process first log entry, different than the rest since there is nothing to compare to yet
for lines in islice(INFO,0,1):
    entry = lines.split(',') #Get separate fields in list
    new_ip = entry[ip]       #Get IP address
    #Process Time of log into time object
    CurrTime = datetime.strptime(entry[date] + ' ' + entry[tim],tformat)    
    #Create dictionary with [key= ip] and item [StartTime,EndTime,Visits]
    new_dict[entry[ip]] = [CurrTime,CurrTime,1] #First entry starttime and endtime are the same, Visits = 1
    #Define the Previous time to check (if a new entry does not change the time, no sessions ended so there is no need to check)
    PrevTime = CurrTime

#Loop over all log entries
for lines in islice(INFO,0,None):
    #Process line (same as before), get list, ip, and time object
    entry = lines.split(',')    
    
    new_ip = entry[ip]
    CurrTime = datetime.strptime(entry[date] + ' ' + entry[tim],tformat)

    #If the time of entry is bigger than previous, some sessions might have ended, run addline
    if CurrTime > PrevTime:
        new_dict = addline(new_dict,in_p)    

    #Check if the new ip had an open session
    idx = new_dict.get(new_ip,None)
    if idx is None: #If not, create a new entry on dictionary
        new_dict[entry[ip]] = [CurrTime,CurrTime,1]
    else: #If yes, update CurrentTime and Visits number
        new_dict[entry[ip]] = [idx[0],CurrTime,idx[2]+1]
    #Redefine Previous time
    PrevTime = CurrTime    

#If we reach the end of the log, close all sessions in order of entry (that is where the OrderedDict becomes useful)    
for t in new_dict: #Loop over ordered dictionary
    #Get information
    usr = new_dict[t]
    #Process total time CurrentTime - StartTime
    TotalTime = usr[1] - usr[0]
    #Write output
    file.write('{0},{1},{2},{3},{4}\n'.format(t,usr[0].strftime(tformat),usr[1].strftime(tformat),TotalTime.seconds+1,usr[2]))
    
file.close()#Close file
