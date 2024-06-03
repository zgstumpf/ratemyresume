# Deployment

TODO: currently there is no code to verify if file is safe.

## Serving static (CSS, JS) and media (.pdf) files
I followed [this guide](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/) for Amazon S3.

Before deploying, in `.env`, set `STATIC_S3` to `True` then run `python manage.py collectstatic.`

## Database
See the "Connecting a PostgreSQL database with Amazon RDS" section of [this guide](https://aws.amazon.com/blogs/containers/deploy-and-scale-django-applications-on-aws-app-runner/).

While experimenting with S3 and PostegreSQL, just comment out old settings, and later get environment variables to work to switch between dev and prod configurations.

## Docker
[Install Docker](https://docs.docker.com/desktop/install/mac-install/) Mac with Intel Chip

The `.env` file contents will be inserted into the Docker image and then it will be connected to AWS Django AppRunner.

## Hosting
connect docker image to aws django apprunner: https://aws.amazon.com/blogs/containers/deploy-and-scale-django-applications-on-aws-app-runner/
