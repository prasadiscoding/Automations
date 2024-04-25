'''

Below code uses python to automate a flow wherein,if there is a change in a specific count in an oracle database from the previous day,
then it runs a query to get the latest data from the oracle db and saves it in a csv which is then used to refresh a .xlsb (excel binary) file 
which picks up the latest data from the newly generated csv - which end users can access on a shared cloud directory

'''

import win32com.client
import pandas as pd
import cx_Oracle
import time
import os
import datetime
import shutil
import fnmatch


#specify connection details in below field for db connection format - username/password@servername:port/db_name
conn = cx_Oracle.connect('')

cur = conn.cursor()

today = datetime.date.today()
year = today.year

def refresh_excel(fname):

    print('Refreshing ' + fname)
    # Opening Excel software using the win32com
    File = win32com.client.Dispatch("Excel.Application")
      
    # Optional line to show the Excel software
    File.Visible = 1
      
    # Opening your workbook
    Workbook = File.Workbooks.open(fname)
      
    # Refeshing all the shests
    Workbook.RefreshAll()
    time.sleep(60)
          
    # Saving the Workbook
    Workbook.Save()
          
    # Closing the Excel File
    Workbook.Close()

def readfile(filename: str):
    fd = open(filename, 'r')
    value = fd.read()
    fd.close
    return value

def search(list1, pattern):
    for a in list1:    
        if pattern in str(a.lower()):
            return a

#rename xlsb files

files = []
for file in os.listdir('.'):
    #find .xlsb files and store filenames in a variable files
    if fnmatch.fnmatch(file, '*.xlsb'):
        files.append(file)

file1 = search(files,'table1')
file2 = search(files,'table2')

os.rename(file1,'table1'+str(year)+'.xlsb')
os.rename(file2,'table2'+str(year)+'.xlsb')


count_query = 'select count(*) from db.table1'

#initial count check (previous day count)
out1 = cur.execute(count_query).fetchone()
count1 = str(out1).strip("(,)")
print(count1,  end = '\n')


#insert - basically updates the db with latest data. Insert_query is present in the same directory as this python file
print('Insert query running...\n')
ins = readfile(os.path.join(os.getcwd(),'insert_query.sql'))
cur.execute(ins)
print('insert done\n')

#count after insert
out2 = cur.execute(count_query).fetchone()
count2 = str(out2).strip("(,)")
print(count2, end = '\n')


#count check

if count1 != count2 :

    print('Count not matching. Need to update the data\n')
    
    #read both sqls i.e. table1.sql and table2.sql which is basically a select on those tables.
    tab1 = readfile(os.path.join(os.getcwd(),'table1.sql'))
    tab2 = readfile(os.path.join(os.getcwd(),'table2.sql'))

    
    #storing result of these select statements into csv.
    tab1_query = pd.read_sql_query(tab1,conn)
    tab1_query.to_csv(os.path.join(os.getcwd(),'table1.csv'),index=False, encoding = 'utf-8')
    tab2_query = pd.read_sql_query(tab2,conn)
    tab2_query.to_csv(os.path.join(os.getcwd(),'table2.csv'),index=False, encoding = 'utf-8')
    

    #refresh both xlsb files as we have latest csvs
    refresh_excel(os.path.join(os.getcwd(),'table1'+ str(year)+'.xlsb'))
    refresh_excel(os.path.join(os.getcwd(),'table2'+ str(year)+'.xlsb'))

    
    '''
    upload to sharepoint - here sharepoint shortcut has been added to windows which shows up as onedrive on local windows explorer and can
    be accessed like just another directory- this is a pre-requiste to avoid writing another code for uploading files to sharepoint
    '''


    print('Refresh Completed with latest data. Uploading xlsb files to Sharepoint\n')
    shutil.copy(os.path.join(os.getcwd(),'table1' + str(year) + '.xlsb'),'D:/Users/'+ os.getlogin() +'/OneDrive - Org_Name/Project')
    shutil.copy(os.path.join(os.getcwd(),'table2' + str(year)+ '.xlsb'),'D:/Users/'+ os.getlogin() +'/OneDrive - Org_Name/Project')    
    print('Upload done\n')


else :
    print('Count Matching, thank you')

    

    

