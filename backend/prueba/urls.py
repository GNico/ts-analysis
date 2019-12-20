from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('clients/<slug:pk>/', views.ClientDetailView.as_view(), name="client"),
    path('clients/<slug:pk>/series/', views.SeriesView.as_view(), name='series'),
    path('clients/<slug:pk>/series/contexts/', views.TagListView.as_view(), name='contexts'),
    path('clients/<slug:pk>/series/tags/', views.ContextListView.as_view(), name='tags'),
    path('anomalies/', views.anomalies, name='anomalies'),
    path('testalgo/', views.testalgo, name='testalgo'),
]