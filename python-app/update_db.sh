#!/bin/bash
#Download database from url
rm databases/*.sql
rm databases/*.zip
echo "downloading database..."
wget -P databases/ https://www.worldcubeassociation.org/wst/wca-developer-database-dump.zip 
unzip databases/wca-developer-database-dump.zip -d databases
rm wca-developer-database-dump.zip
echo "download finished, starting import to database, this might take a while"
mysql -u inigo -pinigo wca_dev < databases/wca-developer-database-dump.sql
echo "import finished, exited successfully"
rm databases/*.sql

