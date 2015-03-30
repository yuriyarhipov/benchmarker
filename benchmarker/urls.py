from django.conf.urls import patterns, include, url

from django.contrib import admin
from elements import views as elements_views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/get_elements/', elements_views.get_elements),
    url(r'^data/projects/', elements_views.projects),
    url(r'^data/competitors_upload_template/', elements_views.competitors_upload_template),
    url(r'^data/competitors/', elements_views.competitors),
)
