from django.conf.urls import patterns
import views as competitors_views


urlpatterns = patterns('',
    (r'^$', competitors_views.competitors),
    (r'^(?P<competitor_id>\w+)', competitors_views.competitor),
)