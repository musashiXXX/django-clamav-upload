from django.conf import settings
"""
    Configuration options for the ``clamav_upload`` package:

    All options reside in a dictionary, ``CLAMAV_UPLOAD`` within your project's ``settings.py``. The options are as
    follows:

        CONTENT_TYPE_CHECK_ENABLED      Set to ``True`` or ``False`` in order to enable or disable content type checking
                                        via python-magic. Default is ``False``.

    To configure any or all of these options, you simply need to define them in ``settings.py``:

        CLAMAV_UPLOAD = {
            'CONTENT_TYPE_CHECK_ENABLED': True,
        }

"""

def get_settings():
    """
        This function returns a dict containing default settings
    """
    s = getattr(settings, 'CLAMAV_UPLOAD', {})
    s = {
            'CONTENT_TYPE_CHECK_ENABLED': s.get('CONTENT_TYPE_CHECK_ENABLED', False),
            # LAST_HANDLER is not a user configurable option; we return
            # it with the settings dict simply because it's convenient.
            'LAST_HANDLER': getattr(settings, 'FILE_UPLOAD_HANDLERS')[-1]
        }
    return s

