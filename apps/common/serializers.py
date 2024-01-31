from rest_framework import serializers


class InputSerializer(serializers.Serializer):
    file = serializers.FileField()
    file_title = serializers.CharField(max_length=255)
    column_mapping = serializers.JSONField()
    values_to_replace = serializers.JSONField(required=False)
    sheet_mapping = serializers.JSONField(required=False)
