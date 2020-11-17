from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('clients/<slug:pk>/', views.ClientView.as_view(), name="client"),
    path('clients/<slug:pk>/series/', views.SeriesView.as_view(), name='series'),
    path('clients/<slug:pk>/series/tagcount/', views.TagCountView.as_view(), name='tagcount'),
    path('clients/<slug:pk>/series/contexts/', views.ContextListView.as_view(), name='contexts'),
    path('clients/<slug:pk>/series/tags/', views.TagListView.as_view(), name='tags'),
    path('analysis/', views.AnalysisView.as_view(), name='analysis'),
    path('testalgo/', views.AlgoTestView.as_view(), name='testalgo'),
]