import pyclamd, logging
from django.conf import settings
from django.contrib import messages
from .models import AllowedContentType
from django.core.exceptions import PermissionDenied
from django.core.files.uploadhandler import TemporaryFileUploadHandler


logger = logging.getLogger(__name__)


class ClamAVFileUploadHandler(TemporaryFileUploadHandler):

    def __init__(self, *args, **kwargs):
        super(ClamAVFileUploadHandler, self).__init__(*args, **kwargs)
        self.check_content_type = getattr(
            settings, 'CONTENT_TYPE_CHECK_ENABLED', False)
        last_handler = getattr(settings, 'FILE_UPLOAD_HANDLERS')[-1]
        if last_handler == "{0}.{1}".format(__name__, self.__class__.__name__):
            self.is_last_handler = True
        else:
            self.is_last_handler = False
        try:
            self.cd = pyclamd.ClamdAgnostic()
        except ValueError:
            logger.critical('The ClamAV daemon does not appear to be running!')
            messages.error(self.request, 'Service currently unavailable')
            raise PermissionDenied

    def new_file(self, file_name, *args, **kwargs):
        super(ClamAVFileUploadHandler, self).new_file(file_name, *args, **kwargs)
        logger.info('Starting new file upload, scanning for malicious content')
        logger.debug('Original Filename: {0}'.format(self.file.name))
        logger.debug('Temporary Filepath: {0}'.format(self.file.temporary_file_path()))
        logger.debug('Content-Type: "{0}"'.format(self.file.content_type))
        if self.check_content_type:
            try:
                AllowedContentType.objects.get(allowed_type=self.file.content_type)
            except AllowedContentType.DoesNotExist:
                error_message = 'Content-Type: {0} is not an accepted type, skipping'.format(self.file.content_type)
                logger.warning('{0}'.format(error_message))
                messages.error(self.request, error_message)
                raise PermissionDenied

    def receive_data_chunk(self, raw_data, start):
        try:
            if self.cd.scan_stream(raw_data) is None:
                if self.is_last_handler:
                    self.file.write(raw_data)
                else:
                    return raw_data
            else:
                error_message = 'Malicious content detected in stream, skipping'
                logger.warning(error_message)
                messages.error(self.request, error_message)
                raise PermissionDenied
        except pyclamd.ConnectionError as e:
            messages.error(self.request, e.message)
            raise PermissionDenied

    def file_complete(self, file_size):
        logger.info('File upload: %s complete!' % self.file.name)
        if self.is_last_handler:
            self.file.seek(0)
            self.file.size = file_size
            return self.file
