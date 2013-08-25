from django.conf.urls import patterns, url

from tours import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^info$', views.info, name='info'),
                       url(r'^new$', views.newreq, name='new'),
                       url(r'^notify$', views.notifyreq, name='notify'),
                       url(r'^claim$', views.claimreq, name='claim'),
)
