# Database

## Create the database in AWS
Documentation followed: https://awstip.com/connecting-your-django-application-to-aws-rds-postgresql-database-149ca685f546

AWS -> RDS -> Create database

<pre>
Choose a database creation method: Standard create
Engine type: PostgreSQL
Templates: Free tier
DB instance identifier: ratemyresume-postgresql
Master username: master
Credentials management: Self managed
✓ Auto generate password
Public access: Yes
Additional configuration -> Initial database name: ratemyresume_db
</pre>

Note: Free Tier provides 750 running hours per month at no charge, more than the total number of hours in a month, so hours are not a concern. Free Tier only lasts for 12 months. After that, it would be a good idea to turn the dev database off when not using it to save hours.

After creating the database, change some settings to allow Django to access the database.

AWS -> RDS -> Databases -> ratemyresume-postgresql

Connectivity & security -> VPC security group -> default group -> Edit inbound rules -> Add rule

<pre>
Type: PostgreSQL
Source: My IP
Description: Allows dev computer to access database
</pre>

## View database contents

### Download pgAdmin 4

AWS sets up the database server, but you can't view the database contents through AWS. For this, we will use pgAdmin 4, a desktop app, which allows viewing database tables and running SQL against the database.

[Download pgAdmin 4](https://www.pgadmin.org/download/)

Select the appropriate option for your device. Make sure you are looking at the options for pgAdmin 4, not pgAgent.

Select the download option with the latest release date. You will be brought to a file explorer. Select the download file appropriate for your device, and perform the typical download process for your device. When finished, open pgAdmin 4 on your device.

### Connect to database in pgAdmin 4

Dashboard -> Quick Links -> Add New Server

In this project, database configuration values are stored in one central location: the `.env` file. Plug in the following values from `.env` into pgAdmin 4.

- General -> Name: `DB_NAME` from `.env`

Switch to Connection tab

- Host name/address: `DB_HOST` from `.env`
- Port: `DB_PORT` from `.env`
- Maintenance database: `DB_NAME` from `.env`
- Username: `DB_USER` from `.env`
- Password: `DB_PASSWORD` from `env`
- Save password? ✓

### View table contents in pgAdmin 4

Object Explorer -> Servers -> `DB_NAME` from `.env` -> Databases -> `DB_NAME` from `.env` -> Schemas -> public -> Tables

Now you can see all tables in the database. To view the contents of a certain table, right-click the table name in Object Explorer and select **View/Edit Data**. Select **All Rows**, or whichever option suits your needs.

To execute SQL, right-click Tables in Object Explorer and select **Query Tool**.

### Other actions

Delete all tables (useful when changing database table configurations, DO NOT do this in production db). Run this SQL:
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

Refresh the database (after doing something like dropping all schemas to reset it): Object Explorer -> Servers -> right-click db name -> **Refresh...**

