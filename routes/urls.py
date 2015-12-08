from django.conf.urls import patterns
import views as routes_views


urlpatterns = patterns('',
    (r'^$', routes_views.routes),
    (r'^(?P<route_id>\d+)/frame/', routes_views.route_frame),
    (r'^(?P<route_id>\d+)$', routes_views.route),
)