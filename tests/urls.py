from django.conf.urls import url
from .views import file_upload


urlpatterns = [ 
    url(r'^upload/', file_upload),
]
