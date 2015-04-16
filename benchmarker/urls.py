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
    url(r'^data/(\S+)/datasets/', elements_views.datasets),
    url(r'^data/get_modules/', elements_views.get_modules),
    url(r'^data/save_file/', elements_views.save_file),
    url(r'^data/(\S+)/get_files/', elements_views.get_files),
    url(r'^data/(\S+)/(\S+)/(\S+)/get_points/', elements_views.get_points),
    url(r'^data/(\S+)/save_standart_route/', elements_views.save_standart_route),
    url(r'^data/(\S+)/routes/', elements_views.routes),
    url(r'^data/(\S+)/modules/', elements_views.modules),
    url(r'^data/(\S+)/(\S+)/files', elements_views.files),
    url(r'^data/(\S+)/save_competitor/', elements_views.save_competitor),
    url(r'^data/(\S+)/competitor/(\S+)', elements_views.competitor),
)
