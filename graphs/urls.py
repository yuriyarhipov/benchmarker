from django.conf.urls import patterns
import views as graphs_views


urlpatterns = patterns('',
    (r'^$', graphs_views.graphs),
    (r'^legends/$', graphs_views.legends),
    (r'^calculations/$', graphs_views.calculations),
    (r'^calculations/(?P<calculation_id>\w+)', graphs_views.calculations),
    (r'^workspaces/$', graphs_views.workspaces),
    (r'^legends/(?P<legend_id>\w+)', graphs_views.legend),
    (r'^graph/(?P<graph_id>\w+)', graphs_views.graph),
)