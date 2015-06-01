from django.conf.urls import patterns
import views as dataset_views


urlpatterns = patterns('',
    (r'^$', dataset_views.datasets),
    (r'^tests/$', dataset_views.tests),
    (r'^(?P<dataset_id>\w+)/$', dataset_views.dataset),


    (r'^(?P<dataset_id>\w+)/tests/$', dataset_views.dataset_tests),
)