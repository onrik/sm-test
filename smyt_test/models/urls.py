from django.conf.urls import patterns, url

urlpatterns = patterns('smyt_test.models.views',
    url(r'^$', 'index', name='index'),
    url(r'^objects/(?P<model_name>\w+)/$', 'get_objects_view', name='objects-list'),
    url(r'^create/$', 'create_object_view', name='create-object'),
    url(r'^upload/$', 'create_models_view', name='upload-models'),
)