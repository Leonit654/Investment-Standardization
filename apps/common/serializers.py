from rest_framework import serializers
from .validators import (
    validate_column_mapping,
    validate_values_to_replace,
    validate_merge_columns,
    validate_file_or_sheet_mapping
)
from apps.common.models import Configuration



class InputSerializer(serializers.Serializer):
    trades_file = serializers.FileField(required=False)
    cashflows_file = serializers.FileField(required=False)
    file_title = serializers.CharField(max_length=255, required=False)
    column_mapping = serializers.JSONField(validators=[validate_column_mapping])
    values_to_replace = serializers.JSONField(validators=[validate_values_to_replace], required=False)
    sheet_mapping = serializers.JSONField(validators=[validate_file_or_sheet_mapping], required=False)
    merge_columns = serializers.JSONField(validators=[validate_merge_columns], required=False)
    organization_id = serializers.IntegerField()


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'
