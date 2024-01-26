#!/bin/bash
#Download database from url
rm databases/*.sql
rm databases/*.zip
echo "downloading database..."
wget -P databases/ https://www.worldcubeassociation.org/wst/wca-developer-database-dump.zip
unzip databases/wca-developer-database-dump.zip -d databases
echo "download finished, starting import to database, this might take a while"
echo "Dividing files to results and other tables"
sed -n '/^-- Table structure for table `Results`/,/^-- Table structure for table `RoundTypes`/p' databases/wca-developer-database-dump.sql > databases/only-results.sql && sed -i '/^-- Table structure for table `Results`/,/^-- Table structure for table `RoundTypes`/d' databases/wca-developer-database-dump.sql
mv databases/wca-developer-database-dump.sql databases/other-tables.sql


echo "Importing results..."
mysql -u u625102952_mysqlresults -pMysqlUser1 u625102952_wca_results < databases/only-results.sql

echo "Importing other tables..."
mysql -u u625102952_mysqluser -pMysqlUser1 u625102952_wca_dev < databases/other-tables.sql
echo "import finished, exited successfully"
rm databases/*
