from django.db import models

class FileUpload(models.Model):
    file = models.FileField()
