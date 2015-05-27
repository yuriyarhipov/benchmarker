from django.conf.urls import patterns
import views as graphs_views


urlpatterns = patterns('',
    (r'^$', graphs_views.graphs),
    (r'^legends/$', graphs_views.legends),
    (r'^legends/(?P<legend_id>\w+)', graphs_views.legend),
)