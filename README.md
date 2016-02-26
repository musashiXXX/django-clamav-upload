# django-clamav-upload
A virus scanning file upload handler for the Django framework

## Prerequisites

The ``clamav-daemon`` must be running on the local machine.

## Installation

Standard python installation:

        python setup.py install
        
... or install using pip:

        pip install django-clamav-upload

## Configuration

    In [django_project]/settings.py:

        FILE_UPLOAD_HANDLERS = (
            'clamav_upload.handlers.ClamAVFileUploadHandler',
        )

This handler can be used as a total replacement for Django's ``TemporaryFileUploadHandler``. In addition to scanning uploaded files for malicious content, the handler can also be configured to restrict the types of files that will be accepted. To enable this check, you need to set the following variable in ``settings.py``:

    CLAMAV_UPLOAD = {
        'CONTENT_TYPE_CHECK_ENABLED': True
    }

This determines whether the handler will check the content type of the file against the allowed types that have been configured in the database. If you don't want this feature, simply leave the option unconfigured -- it defaults to ``False``, but if you do, next you'll need to configure some allowed types from within Django's admin interface. In order to do that, you need to add ``clamav_upload`` to ``INSTALLED_APPS`` in ``settings.py``:

        INSTALLED_APPS = (
            [...]
            'clamav_upload',
        )

The check relies on ``python-magic`` to determine the content-type of the uploaded file. To _enable_ a content-type, simply add it:
 
        >>> from clamav_upload.models import *
        >>> a = AllowedContentType(allowed_type = 'video/mpeg').save()
        
See the [IANA page on media-types](http://www.iana.org/assignments/media-types/media-types.xhtml) for a comprehensive list.

## Tests

To run the tests, setup a virtualenv with the required packages (see `requirements.txt`) and then cd into the project directory and run `runtests.py`:

        ./runtests.py
        
The test suite has a default logging configuration so if you want to see what the upload handler is doing, tail the logfile:

        tail -f /tmp/clamav_upload.log
        
You should see the following output:
      
        [2015-11-09 08:37:49,935] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Starting new file upload, scanning for malicious content
        [2015-11-09 08:37:49,935] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Original Filename: tmpsqWNdw
        [2015-11-09 08:37:49,935] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Temporary Filepath: /tmp/tmpo_BjOS.upload
        [2015-11-09 08:37:49,935] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Content-Type: application/octet-stream
        [2015-11-09 08:37:49,936] [THIS IS A TEST] [WARNING] [clamav_upload.handlers] Content-Type: application/octet-stream is not an accepted type, skipping
        [2015-11-09 08:37:49,943] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Starting new file upload, scanning for malicious content
        [2015-11-09 08:37:49,943] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Original Filename: tmpwkYlwv
        [2015-11-09 08:37:49,944] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Temporary Filepath: /tmp/tmpE2nr0u.upload
        [2015-11-09 08:37:49,944] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Content-Type: application/octet-stream
        [2015-11-09 08:37:49,945] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] File upload: tmpwkYlwv complete!
        [2015-11-09 08:37:49,950] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Starting new file upload, scanning for malicious content
        [2015-11-09 08:37:49,950] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Original Filename: tmpfSPdrE
        [2015-11-09 08:37:49,950] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Temporary Filepath: /tmp/tmptQnzu3.upload
        [2015-11-09 08:37:49,950] [THIS IS A TEST] [DEBUG] [clamav_upload.handlers] Content-Type: application/octet-stream
        [2015-11-09 08:37:49,953] [THIS IS A TEST] [WARNING] [clamav_upload.handlers] Malicious content detected in stream, skipping

The test runner attempts to upload three types of files: one "clean", one "infected", and one clean but unacceptable filetype. 

## Error handling

The upload handler will trigger a 403 if any of the following conditions are met:

 * Attempted upload of a file that is an unacceptable mimetype
 * Attempted upload of a file that contains malicious content as detected by ClamAV
 * An exception will be raised if the handler is unable to communicate with ClamAV (clamd)
 
The resulting errors can be retrieved via the messages framework (``django.contrib.messages``) by using a 403 handler.
Here's an example that returns the error as a JSON response:

    import json
    from django.http import HttpResponse
    from django.contrib.messages import get_messages
    
    def my_403_handler(request):
        storage = get_messages(request)
        response_data = {'error', []}
        for message in storage:
            response_data['error'] += [str(message)]
        return HttpResponse(
            json.dumps(response_data), content_type='application/json', status=403)
            


## To-do

* Create a ``MemoryFileUploadHandler`` version

