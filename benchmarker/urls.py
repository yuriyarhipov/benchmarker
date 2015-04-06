from django.conf.urls import patterns, include, url

from django.contrib import admin
from elements import views as elements_views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/get_elements/', elements_views.get_elements),
    url(r'^data/projects/', elements_views.projects),
    url(r'^data/competitors_upload_template/', elements_views.competitors_upload_template),
    url(r'^data/(\S+)/competitors/', elements_views.competitors),
    url(r'^data/upload_data_set/', elements_views.upload_data_set),
    url(r'^data/datasets/', elements_views.datasets),
    url(r'^data/get_modules/', elements_views.get_modules),
    url(r'^data/save_file/', elements_views.save_file),
    url(r'^data/(\S+)/get_files/', elements_views.get_files),
    url(r'^data/get_points/', elements_views.get_points),
)
