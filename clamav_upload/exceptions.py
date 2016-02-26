from django.contrib import messages
from django.core.exceptions import PermissionDenied


class UploadPermissionDenied(PermissionDenied):

    def __init__(self, request, log_func, error_message, *args, **kwargs):
        log_func(error_message)
        messages.error(request, error_message)
        super(UploadPermissionDenied, self).__init__(*args, **kwargs)
