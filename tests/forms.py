from django.forms import ModelForm
from .models import FileUpload

class FileUploadForm(ModelForm):
    class Meta:
        model = FileUpload
        fields = '__all__'
