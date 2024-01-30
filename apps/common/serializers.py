from rest_framework import serializers


class InputSerializer(serializers.Serializer):
    # TODO: Make file, file_title, column_mapping required since we are using them in trades and cashflow
    file = serializers.FileField(required=False)
    file_title = serializers.CharField(max_length=255,required=False)
    column_mapping = serializers.JSONField(required=False)
    values_to_replace = serializers.JSONField(required=False)
    sheet_mapping = serializers.JSONField(required=False)
