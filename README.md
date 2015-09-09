# django-clamav-upload
A virus scanning file upload handler for the Django framework

## Installation

For now, simply copy the ``clamav_upload`` directory into your project directory. An installation script will follow soon.

## Configuration

    In [django_project]/settings.py:

        FILE_UPLOAD_HANDLERS = (
            'clamav_upload.handlers.ClamAVFileUploadHandler',
        )

This handler can be used as a total replacement for Django's ``TemporaryFileUploadHandler``. At this time, there is only one other configuration option:

        CONTENT_TYPE_CHECK_ENABLED = [True or False]

This determines whether the handler will check the content type of the file against the allowed types that have been configured in the database. If you don't want this feature, simply leave the option unconfigured -- it defaults to ``False``, but if you do, then you'll need to configure some allowed types from within Django's admin interface.

The check is simple, it relies on the content-type provided by the user's browser but I plan on not relying on this in the future and instead incorporating ``python-magic`` to determine the content-type of the uploaded file.


## To-do

* Create a ``MemoryFileUploadHandler`` version
* Implement ``python-magic`` content type checking 
* Create a proper package/setup.py

