from rest_framework import serializers
from .models import Pipeline, Analysis, PeriodicAnalysis, Monitor, NotificationChannel, Incident, Client
from .elastic import series_search

class ClientInputSerializer(serializers.Serializer):
    name = serializers.RegexField(regex='^[a-z0-9_]+$', allow_blank=False)
    utc_offset = serializers.IntegerField()
    folder_name = serializers.CharField(allow_blank=False)


class ClientEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'utc_offset']


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = ['id', 'name', 'description', 'nodes', 'created', 'modified']


#serializer to store analysis settings
class AnalysisSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['id', 'client', 'name', 'interval', 'description', 'data_options', 'model', 'created', 'modified']


#serializer for performing live analysis requests
class AnalysisSerializer(serializers.Serializer):
    client = serializers.CharField(allow_blank=False)
    interval = serializers.CharField()
    data_options = serializers.JSONField()
    model = serializers.JSONField()

   # def validate_start(self, value):
   #     data = self.get_initial()
   #     if data.get('end') and data.get('start') and (data['start'] > data['end']):
   #         raise serializers.ValidationError("Start date must be before end date")
   #     return value


class PeriodicAnalysisSerializer(serializers.ModelSerializer):
    time_interval = serializers.RegexField(regex='^[0-9]+[smhd]$', allow_blank=False, required=False)
    data_time_window = serializers.RegexField(regex='^[0-9]+[smhd]$', allow_blank=True, default='')
    anomaly_time_window = serializers.RegexField(regex='^[0-9]+[smhd]$', allow_blank=True, default='')
    analysis_details = AnalysisSettingsSerializer(read_only=True, source='analysis')

    class Meta:
        model = PeriodicAnalysis
        fields = ['id', 'monitor', 'analysis', 'analysis_details', 'task', 'active', 
        'alerts_enabled', 'time_interval', 'data_time_window', 'anomaly_time_window', 'created', 'last_run' ]


class NotificationChannelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = NotificationChannel
        fields = ['id', 'email', 'monitor']


class MonitorSerializer(serializers.ModelSerializer):
    detectors = PeriodicAnalysisSerializer(many=True, read_only=True)
    notification_channels = NotificationChannelSerializer(many=True, read_only=True)

    class Meta:
        model = Monitor
        fields = ['id', 'name', 'notification_channels', 'detectors']


class MonitorListSerializer(serializers.ModelSerializer):
    num_detectors = serializers.IntegerField(read_only=True)
    num_incidents = serializers.IntegerField(read_only=True)
    last_incident = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Monitor
        fields = ['id', 'name', 'num_detectors', 'num_incidents', 'last_incident']


class IncidentSerializer(serializers.ModelSerializer):
    series = serializers.SerializerMethodField()
    analysis = AnalysisSettingsSerializer(read_only=True, source='periodic_analysis.analysis')

    def get_series(self, obj):
        search = series_search.SeriesSearch()
        series_data = {}
        inputs_data = obj.periodic_analysis.analysis.data_options
        client = Client.objects.get(name=obj.client)
        for index, input_data in enumerate(inputs_data):
            s = search.get_series( 
                indexname=client.index_name, 
                start=input_data.get('start', ''),  
                end=input_data.get('end', ''),  
                context=input_data.get('contexts', []), 
                tags=input_data.get('tags', []),             
                interval=input_data.get('interval', '1h'),
                filter_tags=input_data.get('filter_tags', False),
                filter_contexts=input_data.get('filter_contexts', False))
            series_data[str(index+1)] = s
        return series_data

    class Meta:
        model = Incident
        fields = ['id', 'state', 'client', 'score', 'start', 'end', 'desc', 'series', 'duration', 'analysis']


class IncidentListSerializer(serializers.ModelSerializer):
    class AnalysisListingField(serializers.RelatedField):
         def to_representation(self, value):
             return value.analysis.name

    class MonitorListingField(serializers.RelatedField):
        def to_representation(self, value):
            return value.monitor.name

    monitor = MonitorListingField(read_only=True, source='periodic_analysis')
    analysis_name = AnalysisListingField(read_only=True, source='periodic_analysis')

    class Meta:
        model = Incident
        fields = ['id', 'state', 'client', 'score', 'start', 'end', 'desc', 'monitor', 'duration', 'analysis_name']