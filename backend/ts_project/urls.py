from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('clients/<slug:pk>/', views.ClientView.as_view(), name='client'),
    path('clients/<slug:pk>/series/', views.SeriesView.as_view(), name='series'),
    path('clients/<slug:pk>/series/tagcount/', views.TagCountView.as_view(), name='tagcount'),
    path('clients/<slug:pk>/series/contexts/', views.ContextListView.as_view(), name='contexts'),
    path('clients/<slug:pk>/series/tags/', views.TagListView.as_view(), name='tags'),
    path('analysis/', views.AnalysisView.as_view(), name='analysis'),

    path('pipelines/', views.PipelineListView.as_view(), name='pipelines'),
    path('pipelines/<slug:pk>/', views.PipelineDetailView.as_view(), name='pipeline_detail'),
    path('node-types/', views.PipelineNodesListView.as_view(), name='pipeline_types'),

    path('analysis-settings/', views.AnalysisSettingsListView.as_view(), name='settings'),
    path('analysis-settings/<slug:pk>/', views.AnalysisSettingsDetailView.as_view(), name='settings_detail'),


    path('source-files/', views.DataSourceFilesList.as_view(), name='source-files'),

    path('testalgo/', views.AlgoTestView.as_view(), name='testalgo'),

]