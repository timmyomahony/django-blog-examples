from django.conf.urls import patterns, url
from .views import UploadURLView, UploadDetailView

urlpatterns = patterns('',
    url(r'^$', UploadURLView.as_view(), name="upload-url"),
    url(r'^show/(?P<pk>\d+)/$', UploadDetailView.as_view(), name="upload-detail")
)
