from django.conf.urls import patterns
import views as equipment_views


urlpatterns = patterns('',
    (r'^$', equipment_views.equipments),
    (r'^(?P<equipment_id>\w+)', equipment_views.equipment),
)