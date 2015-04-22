from django.conf.urls import patterns
import views as dataset_views


urlpatterns = patterns('',
    (r'^$', dataset_views.datasets),
    (r'^(?P<dataset_id>\w+)', dataset_views.dataset),
)