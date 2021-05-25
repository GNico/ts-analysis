from rest_framework import serializers
from .models import Pipeline, Analysis, PeriodicAnalysis, Monitor, NotificationChannel, Incident
from . import services


class ClientInputSerializer(serializers.Serializer):
    name = serializers.RegexField(regex='^[a-z0-9_]+$', allow_blank=False)
    folder_name = serializers.CharField(allow_blank=False)


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = ['id', 'name', 'description', 'nodes', 'created', 'modified']


#serializer to store analysis settings
class AnalysisSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['id', 'client', 'name', 'description', 'data_options', 'model', 'created', 'modified']


#serializer for performing live analysis requests
class AnalysisSerializer(serializers.Serializer):
    client = serializers.CharField(allow_blank=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, min_length=None, max_length=None)
    contexts = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, min_length=None, max_length=None)
    start = serializers.DateTimeField(required=False, allow_null=True)
    end = serializers.DateTimeField(required=False, allow_null=True)
    interval = serializers.RegexField(regex='^[0-9]+[mhd]$', allow_blank=True, required=False)
    model = serializers.JSONField()

    def validate_start(self, value):
        data = self.get_initial()
        if data.get('end') and data.get('start') and (data['start'] > data['end']):
            raise serializers.ValidationError("Start date must be before end date")
        return value


class PeriodicAnalysisSerializer(serializers.ModelSerializer):
    time_interval = serializers.RegexField(regex='^[0-9]+[smhd]$', allow_blank=False, required=False)
    relevant_period = serializers.RegexField(regex='^[0-9]+[smhd]$', allow_blank=False, required=False)
    analysis_details = AnalysisSettingsSerializer(read_only=True, source='analysis')

    class Meta:
        model = PeriodicAnalysis
        fields = ['id', 'monitor', 'analysis', 'analysis_details', 'task', 'active', 'alerts_enabled', 'time_interval', 'relevant_period', 'created', 'last_run' ]


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

    def get_series(self, obj):
        options = obj.periodic_analysis.analysis.data_options
        data = services.get_series(options['client'], options['start'], options['end'], options['contexts'], options['tags'], options['interval'])
        return data

    class Meta:
        model = Incident
        fields = ['id', 'state', 'score', 'start', 'end', 'desc', 'series']


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
        fields = ['id', 'state', 'score', 'start', 'end', 'desc', 'analysis_name', 'monitor']