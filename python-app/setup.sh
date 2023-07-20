#!/bin/bash
#This script installs all the necessary dependencies
##And downloads the database from the wca export and imports it into a mysql database
##The following dependencies are needed to be able to run this script:
#
#Mysql, python3, pip, curl, unzip, pv

#First install python dependencies from requirements.txt
apt update
apt install python3-pip unzip curl pv -y
pip3 install -r requirements.txt
#Then download the db from the link
#

temp_url="https://www.dwsamplefiles.com/?dl_id=559"
final_url=""
echo "Downloading demo zip file..."
curl $temp_url > databases/zipped_file.zip 
echo "Extracting zip file..."
unzip databases/zipped_file.zip -d databases

mysql_user=inigo
mysql_password=inigo

#Now import the sql file into mysql database
#This assumes there is a database already created called wca_dev
echo "importing the database into mysql, this might take a while"
pv databases/wca-developer-database-dump.sql | mysql -u $mysql_user -p$mysql_password wca_dev
python3 app.py
