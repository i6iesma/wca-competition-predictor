#!/bin/bash
#This script installs all the necessary dependencies
##And downloads the database from the wca export and imports it into a mysql database
##The following dependencies are needed to be able to run this script:
#
#Mysql, python3, pip, curl, unzip, pv

#First install python dependencies from requirements.txt
apt update
# apt install python3-pip unzip curl pv -y
# pip3 install -r python-app/requirements.txt
apt install python3-pip -y
pip3 install -r python-app/requirements.txt 
#Then download the db from the link
#

# temp_url="https://www.dwsamplefiles.com/?dl_id=559"
# final_url="https://www.worldcubeassociation.org/wst/wca-developer-database-dump.zip"
# echo "Downloading database zipped file..."
# curl $final_url > python-app/databases/zipped_file.zip 
# echo "Extracting zip file..."
# unzip python-app/databases/zipped_file.zip -d databases

mysql_user=inigo
mysql_password=inigo

#Now import the sql file into mysql database
#This assumes there is a database already created called wca_dev
# echo "importing the database into mysql, this might take a while"
# service mysql restart && mysql -u root -e "CREATE DATABASE wca_dev" && pv python-app/databases/wca-developer-database-dump.sql | mysql -u root wca_dev
