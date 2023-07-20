#!/bin/bash
#This script installs all the necessary dependencies
##And downloads the database from the wca export and imports it into a mysql database
##The following dependencies are needed to be able to run this script:
#
#Mysql, python3, pip, curl, unzip, pv

#First install python dependencies from requirements.txt
pip install -r requirements.txt
#Then download the db from the link
#

temp_url="https://www.dwsamplefiles.com/?dl_id=559"
final_url=""
echo "Downloading demo zip file..."
curl $temp_url > databases/zipped_file.zip
echo "Extracting zip file..."
unzip databases/zipped_file.zip -d databases

mysql_host="mydb"
mysql_user="root"
mysql_password="123456"
mysql_port="3306"

#Now import the sql file into mysql database
#This assumes there is a database already created called wca_dev
mysql -u $mysql_user -p$mysql_password -h $mysql_host -p $mysql_port
# pv databases/wca-developer-database-dump.sql | mysql -u $mysql_user -p$mysql_password wca_dev -h mysql_host -h $mysql_host -P $mysql_port

