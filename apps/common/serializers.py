from rest_framework import serializers


def validate_values_to_replace(value):
    if not isinstance(value, dict):
        raise serializers.ValidationError("Values to replace must be a dictionary")

    if not value:
        raise serializers.ValidationError("Values to replace dictionary must not be empty")

    for key, replace_items in value.items():
        if not isinstance(replace_items, list):
            raise serializers.ValidationError(f"Replace items for key '{key}' must be a list")

        for replace_item in replace_items:
            if not isinstance(replace_item, dict):
                raise serializers.ValidationError(f"Each replace item for key '{key}' must be a dictionary")

            required_keys = ["column_name", "operator", "value", "condition"]
            for req_key in required_keys:
                if req_key not in replace_item:
                    raise serializers.ValidationError(f"'{req_key}' is required in each replace item for key '{key}'")

            condition = replace_item.get("condition", [])
            if not isinstance(condition, list):
                raise serializers.ValidationError(f"Condition must be a list in each replace item for key '{key}'")

            for condition_item in condition:
                required_condition_keys = ["column_name", "operator", "value"]
                for condition_key in required_condition_keys:
                    if condition_key not in condition_item:
                        raise serializers.ValidationError(
                            f"'{condition_key}' is required in each condition item for key '{key}'")


class InputSerializer(serializers.Serializer):
    file = serializers.ListField(child=serializers.FileField())
    file_title = serializers.CharField(max_length=255)
    column_mapping = serializers.JSONField()
    values_to_replace = serializers.JSONField(validators=[validate_values_to_replace], required=False)
    sheet_mapping = serializers.JSONField(required=False)
    merge_columns = serializers.JSONField(required=False)
    file_mapping = serializers.JSONField(required=False)
