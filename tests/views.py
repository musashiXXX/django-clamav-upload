from .forms import FileUploadForm
from django.http import HttpResponse, HttpResponseServerError

def file_upload(request):
    upload_form = FileUploadForm(request.POST, request.FILES)
    if upload_form.is_valid():
        upload_form.save()
    return HttpResponse()
