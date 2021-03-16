from rest_framework import serializers
from .models import Pipeline, Analysis, PeriodicAnalysis

class ClientInputSerializer(serializers.Serializer):
    name = serializers.RegexField(regex='^[a-z0-9_]+$', allow_blank=False)
    folder_name = serializers.CharField(allow_blank=False)


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = ['id', 'name', 'description', 'nodes', 'created', 'modified']


class AnalysisSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['id', 'client', 'name', 'description', 'data_options', 'model', 'created', 'modified']


class AnalysisSerializer(serializers.Serializer):
    client = serializers.CharField(allow_blank=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, min_length=None, max_length=None)
    contexts = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True, min_length=None, max_length=None)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    interval = serializers.RegexField(regex='^[0-9]+[mhd]$', allow_blank=True, required=False)
    model = serializers.JSONField()

    def validate_start(self, value):
        if self.end and (self.start > self.end):
            raise serializers.ValidationError("Start date must be before end date")
        return value


class PeriodicAnalysisSerializer(serializers.ModelSerializer):
    time_interval = serializers.RegexField(regex='^[0-9]+[smhd]$', allow_blank=False, required=True)

    class Meta:
        model = PeriodicAnalysis
        fields = [ 'analysis', 'task', 'active', 'time_interval', 'created' ]