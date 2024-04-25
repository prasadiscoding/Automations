import os
import shutil
from datetime import date

today = date.today()
#source path(explicitly specify full path of folder where log files rest that need to be transferred)
#alternatively can use os.getcwd() if file in same folder as logs

sourcepath = ''
sourcefiles = os.listdir(sourcepath)
os.mkdir(sourcepath + '_bkp_'+ str(today) +'/')

dest_path = (sourcepath + '_bkp_'+ str(today) +'/')

for file in sourcefiles:
    if file.endswith('.log'):
        shutil.move(os.path.join(sourcepath,file), os.path.join(dest_path,file))
