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
    path('analysis/<slug:id>/', views.AnalysisResultView.as_view(), name='analysis_result'),
   # path('periodic-analysis/', views.PeriodicAnalysisListView.as_view(), name='periodic_analysis'),   
   # path('periodic-analysis/<slug:pk>/', views.PeriodicAnalysisDetailView.as_view(), name='periodic_analysis_detail'),   

    path('analysis-settings/', views.AnalysisSettingsListView.as_view(), name='settings'),
    path('analysis-settings/<slug:pk>/', views.AnalysisSettingsDetailView.as_view(), name='settings_detail'),

    path('pipelines/', views.PipelineListView.as_view(), name='pipelines'),
    path('pipelines/<slug:pk>/', views.PipelineDetailView.as_view(), name='pipeline_detail'),
    path('nodes/', views.PipelineNodesListView.as_view(), name='nodes'),
    path('nodes/<slug:group>/<slug:type>/', views.PipelineNodesDetailView.as_view(), name='node_detail'),

    path('monitors/', views.MonitorListView.as_view(), name='monitors'),
    path('monitors/<slug:monitor_id>/', views.MonitorDetailView.as_view(), name='monitors_detail'),
    path('monitors/<slug:monitor_id>/detectors/', views.PeriodicAnalysisListView.as_view(), name='periodic_analysis'),
    path('monitors/<slug:monitor_id>/detectors/<slug:detector_id>/', views.PeriodicAnalysisDetailView.as_view(), name='periodic_analysis_detail'),   
    path('notification-channels/', views.NotificationChannelView.as_view(), name='notifications_channels'),
    path('notification-channels/<slug:pk>/', views.NotificationChannelDetailView.as_view(), name='notifications_channels_detail'),

    path('incidents/', views.IncidentsListView.as_view(), name='incidents'),
    path('incidents/<slug:incident_id>/', views.IncidentDetailView.as_view(), name='incident_detail'),

    path('source-files/', views.DataSourceFilesList.as_view(), name='source-files'),

    path('test-sets/', views.TestSetListView.as_view(), name='test_sets'),
    path('test-sets/<slug:test_id>/', views.TestSetDetailView.as_view(), name='test_sets_detail'),

    path('testalgo/', views.AlgoTestView.as_view(), name='testalgo'),

]