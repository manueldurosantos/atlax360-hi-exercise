# atlax360-hi-exercise

Python exercise for ATLAX 360 Junior Data Engineer hiring processes


PRE-REQUISITES
--------------

You must have installed previously:

Python 3.6.x
<br>
PIP 21.3.x
<br>
Docker 20.10.x




DOCKER IMAGE
------------

In order to install our SQL Server image, you will need to run this command:

```
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=cmgYB2Zr4NJra2gRtGyjypag" -p 1433:1433 fbertos/mssql-atlax360-hi:3.0
```

Our Docker image can be found here:
https://hub.docker.com/r/fbertos/mssql-atlax360-hi

Once this is done, a new SQL server instance will be running locally on port 1433 (please make sure this port is available in your computer or change it if needed)


The SQL Server database contains two tables:

Customer: this table will store our list of customers with their ID and their Name.

Item: this table will store our items with their ID and their Version. There can be many Versions for the same ID, but only the latest VersionNbr will be the active one for each item, the others will be considered old versions.
Also, the DeletedFlag column will tell us if the Item is deleted.
      
For example:
```
+-----------------------------------+
+ ItemId | VersionNbr | DeletedFlag +
+      1 |          1 |           0 +
+      1 |          2 |           0 + 
+      1 |          3 |           1 + => This version is the only one active (latest VersionNbr) for Item 1, but it is deleted so we should discard all rows for Item 1
+-----------------------------------+
```

```
+-----------------------------------+
+ ItemId | VersionNbr | DeletedFlag +
+      1 |          1 |           1 +
+      1 |          2 |           1 + 
+      1 |          3 |           0 + => This version is the only one active (latest VersionNbr) for Item 1 and it is active, so we should include only this row for Item 1 in our export file
+-----------------------------------+
```



PYODBC
------

Python pyodbc library is needed, please use PIP to install it following these guides:

- ODBC DRIVER 18: https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017

- PYODBC: https://www.altaruru.com/python-sqlserver-desde-ubuntu/



EXERCISE
--------

Our tables are growing up quickly and we have now some performance issues on the system. We decided to solve the problem with some adjustments:

1. Create indexes on these tables to increase the performance

2. Create a Python command line program in order to move our Item data from SQL Server into a CSV file to be loaded into a Datawarehouse (only active items)


In order to achieve that, please:

1. Create any index you decide it is needed to increase queries performance

2. Please finish the extract method of our DBExtract class with the code needed to export the following data from SQL Server into a CSV file by using Pandas Python library:
  - ItemId
  - ItemDocumentNbr
  - CustomerName
  - CreateDate (format YYYY-MM-dd HH:mm:ss)
  - UpdateDate (format YYYY-MM-dd HH:mm:ss)

Please notice we just want active (latest version is not deleted) items. 

3. We want also a column in the excel with the ItemSource calculated like:
   - ItemSource: "Local" if the CustomerName ends with 66 or 99, "External" in any other case

4. Please use Python pandas or petl libraries to extract the data (even though code is ready for Pandas).

5. The resulting CSV file should be in UTF-8 format and compressed with GZIP

6. Please use ; as field terminator, CRLF as line terminator and " as quote field character

7. A requirements.txt file is provided with the needed Python dependencies


RESOLUTION
----------

Each applier will have to deliver by email:
  - The DDL CREATE INDEX sentences of any index potentially needed
  - A new public GIT repository with the Python solution provided

Please notice we should discard any item when their latest version is disabled.

If you did your exercise correctly, the resulting CSV file should have 9.514 total rows (header included).



