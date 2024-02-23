from rest_framework import serializers
from .validators import (
    validate_column_mapping,
    validate_values_to_replace,
    validate_merge_columns,
    validate_file_or_sheet_mapping, validate_file_extension
)
from apps.common.models import Configuration



class InputSerializer(serializers.Serializer):
    trades_file = serializers.FileField(required=False, validators=[validate_file_extension])
    cashflows_file = serializers.FileField(required=False, validators=[validate_file_extension])
    file_title = serializers.CharField(max_length=255, required=False)
    column_mapping = serializers.JSONField(validators=[validate_column_mapping], required=True)
    values_to_replace = serializers.JSONField(validators=[validate_values_to_replace])
    sheet_mapping = serializers.JSONField(validators=[validate_file_or_sheet_mapping], required=False)
    merge_columns = serializers.JSONField(validators=[validate_merge_columns], required=False)
    organization_id = serializers.IntegerField(required=True)




class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'
