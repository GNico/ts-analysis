from rest_framework import serializers
from .models import Pipeline, Analysis, PeriodicAnalysis, Monitor, NotificationChannel

class ClientInputSerializer(serializers.Serializer):
    name = serializers.RegexField(regex='^[a-z0-9_]+$', allow_blank=False)
    folder_name = serializers.CharField(allow_blank=False)


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = ['id', 'name', 'description', 'nodes', 'created', 'modified']


#serializer for database analysis settings
class AnalysisSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['id', 'client', 'name', 'description', 'data_options', 'model', 'created', 'modified']


#serializer for performing analysis requests
class AnalysisSerializer(serializers.Serializer):
    #name = serializers.CharField(allow_blank=False)
    #description = serializers.CharField(allow_blank=True)
    client = serializers.CharField(allow_blank=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, min_length=None, max_length=None)
    contexts = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, min_length=None, max_length=None)
    start = serializers.DateTimeField(required=False, allow_null=True)
    end = serializers.DateTimeField(required=False, allow_null=True)
    interval = serializers.RegexField(regex='^[0-9]+[mhd]$', allow_blank=True, required=False)
    model = serializers.JSONField()

    def validate_start(self, value):
        data = self.get_initial()
        if data['end'] and data['start'] and (data['start'] > data['end']):
            raise serializers.ValidationError("Start date must be before end date")
        return value


class PeriodicAnalysisSerializer(serializers.ModelSerializer):
    time_interval = serializers.RegexField(regex='^[0-9]+[smhd]$', allow_blank=False, required=False)
    relevant_period = serializers.RegexField(regex='^[0-9]+[smhd]$', allow_blank=False, required=False)
    last_run_at = serializers.DateTimeField(source='task.last_run_at', read_only=True)
    analysis_details = AnalysisSettingsSerializer(read_only=True, source='analysis')

    class Meta:
        model = PeriodicAnalysis
        fields = [ 'id', 'monitor', 'analysis', 'analysis_details', 'task', 'active', 'alerts_enabled', 'time_interval', 'relevant_period', 'created', 'last_run_at' ]


class NotificationChannelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = NotificationChannel
        fields = [ 'id', 'email', 'monitor' ]


class MonitorSerializer(serializers.ModelSerializer):
    detectors = PeriodicAnalysisSerializer(many=True, read_only=True)
    notification_channels = NotificationChannelSerializer(many=True, read_only=True)

    class Meta:
        model = Monitor
        fields = [ 'id', 'name', 'notification_channels', 'detectors']


class MonitorListSerializer(serializers.ModelSerializer):
    num_detectors = serializers.IntegerField(read_only=True)
    incidents = serializers.SerializerMethodField("get_incidents")
    last_incident = serializers.SerializerMethodField("get_last_incident")

    class Meta:
        model = Monitor
        fields = [ 'id', 'name', 'num_detectors', 'incidents', 'last_incident']

    def get_detector(self, obj):
        return 3

    def get_incidents(self, obj):
        return 25

    def get_last_incident(self, obj):
        return '27/04/2021'