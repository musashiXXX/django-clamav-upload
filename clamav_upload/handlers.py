import pyclamd, logging, magic
from .models import AllowedContentType
from clamav_upload import get_settings
from .exceptions import UploadPermissionDenied
from django.core.files.uploadhandler import TemporaryFileUploadHandler


logger = logging.getLogger(__name__)
s = get_settings()


class ClamAVFileUploadHandler(TemporaryFileUploadHandler):

    def __init__(self, *args, **kwargs):
        super(ClamAVFileUploadHandler, self).__init__(*args, **kwargs)
        self.content_type_check = s.get('CONTENT_TYPE_CHECK_ENABLED')
        self.content_type_already_checked = False
        self.is_last_handler = False
        if s.get('LAST_HANDLER') == "{0}.{1}".format(__name__, self.__class__.__name__):
            self.is_last_handler = True
        try:
            self.cd = pyclamd.ClamdAgnostic()
        except ValueError:
            raise UploadPermissionDenied(self.request, logger.critical, 'Service currently unavailable')

    def new_file(self, file_name, *args, **kwargs):
        super(ClamAVFileUploadHandler, self).new_file(file_name, *args, **kwargs)
        logger.info('Starting new file upload, scanning for malicious content')
        logger.debug('Original Filename: {0}'.format(self.file.name))
        logger.debug('Temporary Filepath: {0}'.format(self.file.temporary_file_path()))

    def check_content_type(self, upload_buffer):
        if self.content_type_check and not self.content_type_already_checked:
            content_type = None
            try:
                content_type = magic.from_buffer(upload_buffer, mime=True)
                if content_type is None:
                    raise UploadPermissionDenied(
                        self.request, logger.critical, 'Unable to determine content-type, upload denied!')
                AllowedContentType.objects.get(allowed_type=content_type)
                self.content_type_already_checked = True
                logger.debug('Content-Type: "{0}"'.format(content_type))
            except AllowedContentType.DoesNotExist:
                    raise UploadPermissionDenied(
                        self.request, logger.critical, 'Content-Type: {0} is not an accepted type'.format(content_type))

    def receive_data_chunk(self, raw_data, start):
        self.check_content_type(raw_data)
        try:
            if self.cd.scan_stream(raw_data) is None:
                if self.is_last_handler:
                    self.file.write(raw_data)
                else:
                    return raw_data
            else:
                raise UploadPermissionDenied(
                    self.request, logger.critical, 'Malicious content detected in stream, upload denied!')
        except pyclamd.ConnectionError as e:
            raise UploadPermissionDenied(self.request, logger.critical, e.message)

    def file_complete(self, file_size):
        logger.info('File upload: "{0}" complete!'.format(self.file.name))
        if self.is_last_handler:
            self.file.seek(0)
            self.file.size = file_size
            return self.file
