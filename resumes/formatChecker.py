from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat

WORD_PROCESSING_CONTENT_TYPES = [
    "application/pdf",
    "application/msword",  # Word .doc
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # Word .docx
    "application/x-abiword",
    "application/vnd.oasis.opendocument.text", # OpenOffice .odt
    "application/rtf",
    "text/plain",
]


class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 52428800
            100MB - 104857600
            250MB - 214958080
            500MB - 429916160
    """

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", [])
        self.max_upload_size = kwargs.pop("max_upload_size", 0)

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        file = data.file
        try:
            content_type = file.content_type
            if content_type not in self.content_types:
                raise forms.ValidationError(f"{content_type} filetype not supported")

            if file.size > self.max_upload_size:
                raise forms.ValidationError(
                    f"File ({filesizeformat(file.size)}) exceeds size limit of {filesizeformat(self.max_upload_size)}"
                )
        except AttributeError:
            pass

        return data
