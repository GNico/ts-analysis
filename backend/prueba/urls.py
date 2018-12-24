from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contexts/', views.contexts, name='contexts'),
    path('tags/', views.tags, name='tags'),
    path('anomalies/', views.anomalies, name='anomalies'),
    path('series/', views.series, name='series'),
    path('clients/', views.clients, name='clients'),
    path('newclient/', views.newclient, name='newclient')
]