from django.conf.urls import patterns
import views as competitors_views


urlpatterns = patterns('',
    (r'^$', competitors_views.competitors),
    (r'^competitor_names/$', competitors_views.competitor_names),
    (r'^(?P<competitor_name>\w+)', competitors_views.competitor),
)