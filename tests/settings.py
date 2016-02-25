import os, sys
DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'tests',
    'clamav_upload'
]
ROOT_URLCONF = 'tests.urls'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

FILE_UPLOAD_HANDLERS = ( 
    'clamav_upload.handlers.ClamAVFileUploadHandler',
)

DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test.db.sqlite3'),
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'test_uploaded_files_delete_me')

CLAMAV_UPLOAD = {
    'CONTENT_TYPE_CHECK_ENABLED': True
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [THIS IS A TEST] [%(levelname)s] [%(name)s] %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/clamav_upload.log',
            'maxBytes': 1024*1024*20,
            'backupCount': 30,
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propogate': True
        }
    }
}
