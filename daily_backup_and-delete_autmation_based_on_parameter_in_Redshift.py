'''
automation for daily backup based on flag in Redshift- where yesterdays backup is deleted everyday before taking todays backup using paramterized functionality,
so that whenever we need to disable the automation for xyz reasons we can simply change the flag to F in Redshift 

'''

import os
import shutil
import redshift_connector
from send_mail import *

#specify Source path
prod_src = ''

#specify Destination path
prod_dst = ''


def backup(dst,src):
    #delete old backup
    if(os.path.exists(dst)):
       shutil.rmtree(dst)

    #take latest backup
    shutil.copytree(src, dst)

#redshift credentials/details
RS_HOST_PRD = ""
RS_PORT_PRD = 5439
RS_DATABASE_PRD = ""
RS_USER_PRD = ""
RS_PASSWORD_PRD = ""



conn = redshift_connector.connect(
        host = RS_HOST_PRD,
        database= RS_DATABASE_PRD,
        port=5439,
        user= RS_USER_PRD,
        password= RS_PASSWORD_PRD
    )
cur = conn.cursor()
sql = "select param_value from schema.table where param_name ='DAILY_BACKUP_FLAG';"
out = cur.execute(sql).fetchone()

print(out[0])
if out[0]=='T':
    backup(prod_dst,prod_src)
else:
    print('Flag is F so no backup')


