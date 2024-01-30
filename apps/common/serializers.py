from rest_framework import serializers


class InputSerializer(serializers.Serializer):
    # TODO: Make file, file_title, column_mapping required since we are using them in trades and cashflow
    file = serializers.FileField()
    file_title = serializers.CharField(max_length=255)
    column_mapping = serializers.JSONField()
    values_to_replace = serializers.JSONField()
    sheet_mapping = serializers.JSONField()
