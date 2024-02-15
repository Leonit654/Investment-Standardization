from rest_framework import serializers

from apps.common.models import Configuration


class InputSerializer(serializers.Serializer):
    file = serializers.ListField(child=serializers.FileField())
    file_title = serializers.CharField(max_length=255)
    column_mapping = serializers.JSONField()
    values_to_replace = serializers.JSONField(required=False)
    sheet_mapping = serializers.JSONField(required=False)
    merge_columns = serializers.JSONField(required=False)
    file_mapping = serializers.JSONField(required=False)


class BothInputSerializer(serializers.Serializer):
    trades_file = serializers.FileField(required=False)
    cashflows_file = serializers.FileField(required=False)
    file_title = serializers.CharField(max_length=255, required=False)
    column_mapping = serializers.JSONField()
    values_to_replace = serializers.JSONField(required=False)
    sheet_mapping = serializers.JSONField(required=False)
    merge_columns = serializers.JSONField(required=False)
    organization_id = serializers.IntegerField()


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'