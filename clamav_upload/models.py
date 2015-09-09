from django.db import models

class AllowedContentType(models.Model):

    allowed_type = models.CharField(
        max_length = 255,
        verbose_name = 'Content-Type',
        unique = True)

    def __unicode__(self):
        return self.allowed_type

    class Meta:
        verbose_name = 'Allowed Content Type'
        ordering = ('allowed_type',)
