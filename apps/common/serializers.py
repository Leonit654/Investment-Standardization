from rest_framework import serializers


class InputSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    file_title = serializers.CharField(max_length=255,required=False)
    column_mapping = serializers.JSONField(required=False)
    values_to_replace = serializers.JSONField(required=False)
