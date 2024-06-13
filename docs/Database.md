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

