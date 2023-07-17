#This file is executed only once to setup the databases in order to be able to be connected
#This assumes that mysql is installed along with the requirements specified in requirements.txt. A
#Mysql uses the credentials in secure/credentials.json
import json
import mysql.connector as connector
import requests
from datetime import date
import zipfile
import os
import subprocess
def main():
    download_db()
    import_to_mysql()
     

def import_to_mysql():
    commands = [
        "pv",
        "databases/wca-developer-database-dump.sql",
        "|",
        "mysql",
        "-u inigo",
        "-p123456",
        "wca_dev"
    ]
    subprocess.run(commands, shell=True)
    


def download_db():
    
    final_url = "https://www.worldcubeassociation.org/wst/wca-developer-database-dump.zip" 
    temp_url = "https://www.dwsamplefiles.com/?dl_id=559"
    r = requests.get(final_url, allow_redirects=True)
    path_to_zip_file = 'databases/' + str(date.today()) + ".zip"
    #Save zipped file
    open(path_to_zip_file, 'wb').write(r.content)
    #Unzip file
    print(path_to_zip_file)
    with zipfile.ZipFile("databases/2023-07-17.zip", 'r') as zip_ref:
        #Before saving the file, remove all of the files with .sql in that directory so that it is automatically updated
        remove_all_sql_files()
        #extract to databases/
        zip_ref.extractall('databases/')
        #Delete the original zipfile
        os.remove(path_to_zip_file)
        
def remove_all_sql_files():
    dir_name = 'databases/'
    files = os.listdir(dir_name)
    for file in files:
        if file.endswith('.sql'):
            os.remove(os.path.join(dir_name, file))
    


    
