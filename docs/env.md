# The .env file
Data that should be kept secret from source control is stored in the `.env` file in the root directory of the project.

If you've just cloned the repo, you will have to create the `.env` file yourself.

## Template
```env
# S3
# -----------------

# Set to True to fetch static files from S3. Set to False to fetch from local filesystem.
STATIC_S3=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# Database
# -----------------
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```