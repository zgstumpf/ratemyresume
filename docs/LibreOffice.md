# Deprecated
Most of this information is no longer applicable after using Docker.

# LibreOffice
ratemyresume uses LibreOffice to convert user-uploaded resumes, which may be of varying file types, to pdfs, which can be displayed on an HTML page. LibreOffice is free and open-source software and functions like Microsoft Word. For ratemyresume to use LibreOffice, it must be installed on the same system the app is running from. For development, installing LibreOffice to your device works, but for production, Docker will be used to ensure ratemyresume has access to LibreOffice.

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