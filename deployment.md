# Deployment

## Install LibreOffice

[Install LibreOffice](https://www.libreoffice.org/download/download-libreoffice/) 24.2.3 for MacOS(Intel)

After installing, run this command to make sure you know the right path for it.

```sh
/Applications/LibreOffice.app/Contents/MacOS/soffice --help
```

## Test LibreOffice command to convert docx to pdf
This command converts a file named `input.docx` to a new file `input.pdf`, which is stored in the `pdf` directory. Both `input.pdf` and `pdf` are in the root directory `/Users/zacharystumpf`. I found if `pdf` doesn't exist, the command will create it first. The quotes around `input.docx` allow the command to work if the input file has spaces in its name.

```sh
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf --outdir pdfs "input.docx"
```
[Source](https://tariknazorek.medium.com/convert-office-files-to-pdf-with-libreoffice-and-python-a70052121c44)

If that doesn't work, try this. In this command, the `"-env...` argument is meant to fix a bug where the command won't work if LibreOffice is currently open, though I didn't experience this bug in LibreOffice 24.2.3 for MacOS(Intel). It also uses a more specific argument for the `--convert-to` command, though I found it made no difference.

```sh
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless "-env:UserInstallation=file:///tmp/LibreOffice_Conversion_${USER}" --convert-to pdf:writer_pdf_Export --outdir pdfs "worddoc.docx"
```
[Source](https://stackoverflow.com/a/30465397/22737945)

## Run command with Python
[Source](https://tariknazorek.medium.com/convert-office-files-to-pdf-with-libreoffice-and-python-a70052121c44)
The code is in resumes/views.py convert_to_pdf. It works, but the command is written for MacOS machines, so you need to make sure Docker is running on MacOS.

**Important:** The current code stores user-created media (resumes) in the `media` directory. This works in development but it won't work in production. *Maybe use an S3 bucket?* Also, currently there is no code to verify if file is safe.

## Serving static (CSS, JS) and media (.pdf) files
I followed [this guide](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/) for Amazon S3.

Before deploying, in `.env`, set `USE_S3` to `True` then run `python manage.py collectstatic.`

## Database
See the "Connecting a PostgreSQL database with Amazon RDS" section of [this guide](https://aws.amazon.com/blogs/containers/deploy-and-scale-django-applications-on-aws-app-runner/).

While experimenting with S3 and PostegreSQL, just comment out old settings, and later get environment variables to work to switch between dev and prod configurations.

## Docker
[Install Docker](https://docs.docker.com/desktop/install/mac-install/) Mac with Intel Chip

I signed in with GitHub as zgstumpf@crimson.ua.edu and set my Docker username as `zgstumpf`

Strategy: get code including LibreOffice in a docker image: https://www.digitalocean.com/community/questions/how-to-install-libreoffice-in-app

This docker image will then be connected to AWS Django apprunner in the next step.

## Hosting
connect docker image to aws django apprunner: https://aws.amazon.com/blogs/containers/deploy-and-scale-django-applications-on-aws-app-runner/
