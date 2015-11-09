from distutils.core import setup

setup(
    name='django-clamav-upload',
    version='v0.1.0',
    packages=['clamav_upload','tests'],
    url='https://github.com/musashiXXX/django-clamav-upload/releases/tag/v0.1.0',
    license='LICENSE.txt',
    author='Charles Hamilton',
    author_email='musashi@nefaria.com',
    description='A simple upload handler for django that scans inbound streams for malicious content',
    install_requires=[
        'Django >=1.8.4',
        'pyClamd >=0.3.15'
    ]
)