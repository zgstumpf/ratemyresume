# The .env file
Data that should be kept secret from source control is stored in the `.env` file in the root directory of the project.

If you've just cloned the repo, you will have to create the `.env` file yourself.

## Template
```env
# IMPORTANT:
# If you modify this file,
#   1. Copy this entire file and paste it into the Template code block in docs > env.md.
#   2. In env.md, remove the value from each key.


# S3
# -----------------------------------------------------------------------------

# Set to True to fetch static files from S3. This is used in production or while testing production.
# Set to False to fetch static files from your device's filesystem. This is used during development.
STATIC_S3=

# AWS -> Amazon S3 -> Buckets
AWS_STORAGE_BUCKET_NAME=

# AWS -> IAM -> Users -> ratemyresume-s3-user -> Access key 1 (or 2)
AWS_ACCESS_KEY_ID=

# Only visible right after IAM user was created in AWS. If you lost the secret key, go to the Security
# credentials tab, delete the access key, and create a new access key - just make sure production doesn't
# use the key before you delete it.
AWS_SECRET_ACCESS_KEY=

# Database
# -----------------------------------------------------------------------------
# All values come from AWS -> RDS -> Databases -> ratemyresume-postgresql

# Configuration -> DB name (NOT DB identifier)
DB_NAME=

# Configuration -> Master username
DB_USER=

# Only visible right after database was created in AWS RDS. If you lost the password, reset it:
# https://repost.aws/knowledge-center/reset-master-user-password-rds
DB_PASSWORD=

# Connectivity & security -> Endpoint
DB_HOST=

# Connectivity & security -> Port
DB_PORT=
```