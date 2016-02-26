from distutils.core import setup

setup(
    name='django-clamav-upload',
    version='0.1.2',
    packages=['clamav_upload'],
    url='https://github.com/musashiXXX/django-clamav-upload',
    download_url='https://github.com/musashiXXX/django-clamav-upload/tarball/0.1.2',
    license='LICENSE.txt',
    author='Charles Hamilton',
    author_email='musashi@nefaria.com',
    description='A simple upload handler for django that scans inbound streams for malicious content',
    long_description='README.md',
    install_requires=[
        'Django>=1.8.4',
        'pyClamd==0.3.17'
    ],
    keywords='clamav django upload'
)
