from django.conf.urls import patterns
import views as routes_views


urlpatterns = patterns('',
    (r'^$', routes_views.routes),
    (r'^(?P<route_id>\w+)', routes_views.route),
)