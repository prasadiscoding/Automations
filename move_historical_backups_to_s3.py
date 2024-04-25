#HISTORICAL BACKUPS OLDER THAN 6 months are moved to S3
import boto3
import datetime
import os
from datetime import date
from dateutil.relativedelta import relativedelta

#specify the needful in below fields
s3=boto3.client("s3", aws_access_key_id="",aws_secret_access_key="",region_name="")


def check_file_modified_date(path):

    # file modification
    timestamp = os.path.getmtime(path)

    # convert timestamp into DateTime object
    mdate = date.fromtimestamp(timestamp)
    return mdate



#check current date and get 6 months old date
current_date = date.today()
old_date = current_date - relativedelta(months=6)



#folder_path - explicitly specify full path of folder where backup files rest that need to be transferred to S3)
#s3_destn_path - explicitly specify full path where you need to store the backup files on s3)
#s3_bucket - specify s3 bucket
folder_path = ''
s3_destn_path = ''
s3_bucket = ''
files = os.listdir(folder_path)
for x in files:
    s3_path = os.path.join(s3_destn_path, x)
    file_path = os.path.join(folder_path,x)
    modified_date = check_file_modified_date(file_path)
    if modified_date < old_date:
        s3.upload_file(file_path, s3_bucket ,s3_path )
        os.remove(file_path)
        
    else:
        print('No need to move file', x)



