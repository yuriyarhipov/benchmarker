from django.conf.urls import patterns, include, url

from django.contrib import admin
from elements import views as elements_views
import dataset.urls as datasets_urls
import competitors.urls as competitors_urls
import routes.urls as routes_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/(?P<project_id>\w+)/datasets/', include(datasets_urls)),
    url(r'^data/(?P<project_id>\w+)/competitors/', include(competitors_urls)),
    url(r'^data/(?P<project_id>\w+)/routes/', include(routes_urls)),
    url(r'^data/get_elements/', elements_views.get_elements),
    url(r'^data/projects/', elements_views.projects),
    url(r'^data/get_modules/', elements_views.get_modules),
    url(r'^data/(\S+)/save_file/', elements_views.save_file),
    url(r'^data/(\S+)/get_files/', elements_views.get_files),
    url(r'^data/(\S+)/(\S+)/(\S+)/get_points/', elements_views.get_points),
    url(r'^data/(\S+)/modules/', elements_views.modules),
    url(r'^data/(\S+)/module_files', elements_views.module_files),
)
