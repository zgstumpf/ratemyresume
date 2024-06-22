# Database

Ratemyresume uses a [PostgreSQL](https://www.postgresql.org/about/) database hosted by [AWS RDS](https://aws.amazon.com/rds/) (Relational Database Service).

## Create the database in AWS
Documentation followed: https://awstip.com/connecting-your-django-application-to-aws-rds-postgresql-database-149ca685f546

AWS -> RDS -> Create database

- Choose a database creation method: Standard create
- Engine type: PostgreSQL
- Templates: Free tier
- DB instance identifier: ratemyresume-postgresql
- Master username: master
- Credentials management: Self managed
- Auto generate password: ✓
- Public access: Yes
- Additional configuration -> Initial database name: ratemyresume_db

Note: Free Tier provides 750 running hours per month at no charge, more than the total number of hours in a month, so hours are not a concern. Free Tier only lasts for 12 months. After that, it would be a good idea to turn the dev database off when not using it to save hours.

Update `.env` with the values from AWS RDS, especially `DB_PASSWORD` since you can't come back and view it later in AWS RDS.

After creating the database, change some settings to allow Django to access the database.

AWS -> RDS -> Databases -> ratemyresume-postgresql

Connectivity & security -> VPC security group -> default group -> Edit inbound rules -> Add rule

- Type: PostgreSQL
- Source: My IP
- Description: Allows dev computer to access database

## View database contents

### Download pgAdmin

AWS sets up the database server, but you can't view the database contents through AWS. For this, we will use pgAdmin, a desktop app, which allows viewing database tables and running SQL against the database.

[Download pgAdmin 4](https://www.pgadmin.org/download/)

Select the appropriate option for your device. Make sure you are looking at the options for pgAdmin 4, not pgAgent.

Select the download option with the latest release date. You will be brought to a file explorer. Select the download file appropriate for your device, and perform the typical download process for your device. When finished, open pgAdmin 4 on your device.

### Connect to database in pgAdmin

Dashboard -> Quick Links -> Add New Server

In this project, database configuration values are stored in one central location: the `.env` file. Plug in the following values from `.env` into pgAdmin.

- General -> Name: `DB_NAME` from `.env`

Switch to Connection tab

- Host name/address: `DB_HOST` from `.env`
- Port: `DB_PORT` from `.env`
- Maintenance database: `DB_NAME` from `.env`
- Username: `DB_USER` from `.env`
- Password: `DB_PASSWORD` from `env`
- Save password? ✓

### View table contents in pgAdmin

Object Explorer -> Servers -> `DB_NAME` from `.env` -> Databases -> `DB_NAME` from `.env` -> Schemas -> public -> Tables

Now you can see all tables in the database. To view the contents of a certain table, right-click the table name in Object Explorer and select **View/Edit Data**. Select **All Rows**, or whichever option suits your needs.

To execute SQL, right-click Tables in Object Explorer and select **Query Tool**.

### Other actions

**Delete all tables and data and restart from fresh**

DO NOT do this in the production database. This is useful when you make substantial changes in `models.py` and you don't want to deal with migrations.

1. Delete all files EXCEPT `__init__.py` in the `migrations` directory.
1. Run this SQL in pgAdmin:
    ```sql
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    ```
1. Object Explorer -> Servers -> right-click db name -> **Refresh...**

### Add your IP address to the database VPC security group inbound rules

You may need to do this again if you get a `Connection refused` error. Even if you already added your IP before, your IP address may change if you are connected to a different network than the first time.

AWS -> RDS -> Databases -> ratemyresume-postgresql -> Connectivity & security tab -> click link under VPC security groups

There should be one security group listed. Click the link under Security group ID. Then click **Edit inbound rules** -> **Add rule**.

In the new rule, set the **Type** to `PostgreSQL` and the **Source** to `My IP`. Set **Description - optional** to something including your name, such as `Allow NAME computer to access database` so you (and the team) remembers why you made the rule if you ever have to go back to this screen.

Click **Save rules** when done.
