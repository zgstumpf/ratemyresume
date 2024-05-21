# The .env file
If you are a team member, ask Zach for AWS keys.

If you are a contributor, you will have to make your own S3 bucket for testing. Or, develop without testing S3 and hope it works with S3 enabled.

## Template
```env
# Set to True to use S3. Else, set to False to not consume AWS resources.
USE_S3=False

AWS_ACCESS_KEY_ID=update_this
AWS_SECRET_ACCESS_KEY=update_this
AWS_STORAGE_BUCKET_NAME=update_this
```