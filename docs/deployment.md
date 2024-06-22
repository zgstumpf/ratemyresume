# Deployment

TODO: currently there is no code to verify if file is safe.

## Serving static (CSS, JS) and media (.pdf) files
I followed [this guide](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/) for Amazon S3.

Before deploying, in `.env`, set `STATIC_S3` to `True` then run `python manage.py collectstatic.`

## Database
Use dev and prod databases

## Docker
The `.env` file contents will be inserted into the Docker image and then it will be connected to AWS Django AppRunner.

## Hosting
connect docker image to aws django apprunner: https://aws.amazon.com/blogs/containers/deploy-and-scale-django-applications-on-aws-app-runner/
