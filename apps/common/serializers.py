from rest_framework import serializers
from apps.trades.services import TRADE_COLUMNS
from apps.cash_flows.services import CASH_FLOW_COLUMNS


def validate_column_mapping(value):
    trade_standard_columns = [key for key, value in TRADE_COLUMNS.items()]
    cash_flow_standard_columns = [key for key, value in CASH_FLOW_COLUMNS.items()]
    if not isinstance(value, dict):
        raise serializers.ValidationError("column_mapping must be a dictionary")

    if not value:
        raise serializers.ValidationError("column_mapping dictionary must not be empty")

    for key, mapping in value.items():
        if not isinstance(mapping, dict):
            raise serializers.ValidationError(f"Mapping columns for key '{key}' must be a dict")

        if key not in ["trade", "cash_flow"]:
            raise serializers.ValidationError(f"{key} is not valid. Try to use 'trade' or 'cash_flow'")

        for user_fields, standard_field in mapping.items():
            if key == "trade" and standard_field not in trade_standard_columns:
                raise serializers.ValidationError(f"{standard_field} is not valid. Try to use {trade_standard_columns}")
            if key == "cash_flow" and standard_field not in cash_flow_standard_columns:
                raise serializers.ValidationError(
                    f"{standard_field} is not valid. Try to use {cash_flow_standard_columns}")


def validate_values_to_replace(value):
    trade_standard_columns = [key for key, value in TRADE_COLUMNS.items()]
    cash_flow_standard_columns = [key for key, value in CASH_FLOW_COLUMNS.items()]

    if not isinstance(value, dict):
        raise serializers.ValidationError("Values to replace must be a dictionary")

    if not value:
        raise serializers.ValidationError("Values to replace dictionary must not be empty")

    for key, replace_items in value.items():
        if key not in ["trade", "cash_flow"]:
            raise serializers.ValidationError(f"{key} is not valid. Try to use 'trade' or 'cash_flow'")
        if not isinstance(replace_items, list):
            raise serializers.ValidationError(f"Replace items for key '{key}' must be a list")

        for replace_item in replace_items:
            if not isinstance(replace_item, dict):
                raise serializers.ValidationError(f"Each replace item for key '{key}' must be a dictionary")

            required_keys = ["column_name", "operator", "value", "condition"]
            for req_key in required_keys:
                if req_key not in replace_item:
                    raise serializers.ValidationError(f"'{req_key}' is required in each replace item for key '{key}'")

            column_name = replace_item.get("column_name", None)
            if key == "trade" and column_name not in trade_standard_columns:
                raise serializers.ValidationError(
                    f"'{column_name}' is not a valid column name for 'trade'. It will not be saved in the standard "
                    f"tables.")
            elif key == "cash_flow" and column_name not in cash_flow_standard_columns:
                raise serializers.ValidationError(
                    f"'{column_name}' is not a valid column name for 'cash_flow'. It will not be saved in the "
                    f"standard tables.")

            operator_value = replace_item.get("operator", None)
            common_operators = ["&", "|"]
            if operator_value is not None and operator_value not in common_operators:
                raise serializers.ValidationError(
                    f"'{operator_value}' is not valid. Try to use operators like {common_operators[0]} and {common_operators[1]}")

            condition = replace_item.get("condition", [])
            if not isinstance(condition, list):
                raise serializers.ValidationError(f"Condition must be a list in each replace item for key '{key}'")

            for condition_item in condition:
                required_condition_keys = ["column_name", "operator", "value"]
                for condition_key in required_condition_keys:
                    if condition_key not in condition_item:
                        raise serializers.ValidationError(
                            f"'{condition_key}' is required in each condition item for key '{key}'")


def validate_merge_columns(value):
    allowed_operators = ["sum", "subtract", "multiply"]

    if not isinstance(value, list):
        raise serializers.ValidationError("Input must be a list of merge column configurations")

    for merge_config in value:
        if not isinstance(merge_config, dict):
            raise serializers.ValidationError("Each item in the list must be a dictionary")

        required_keys = ["new_column_name", "operator", "columns_to_merge"]
        for req_key in required_keys:
            if req_key not in merge_config:
                raise serializers.ValidationError(f"'{req_key}' is required in each merge column configuration")

        operator_value = merge_config.get("operator", None)
        if operator_value not in allowed_operators:
            raise serializers.ValidationError(
                f"'{operator_value}' is not a valid operator. Try to use operators like {', '.join(allowed_operators)}")

        columns_to_merge = merge_config.get("columns_to_merge", [])
        if not isinstance(columns_to_merge, list) or not all(isinstance(column, str) for column in columns_to_merge):
            raise serializers.ValidationError("columns_to_merge must be a list of column names")


def validate_file_or_sheet_mapping(value):
    if not isinstance(value, dict):
        raise serializers.ValidationError("This field must be a dictionary")

    if not value:
        raise serializers.ValidationError("This field dictionary must not be empty")

    for key, value in value.items():
        if value not in ['trade', 'cash_flow']:
            raise serializers.ValidationError(f"{value} is not  valid. Try to use trade or cash_flow")


class InputSerializer(serializers.Serializer):
    file = serializers.ListField(child=serializers.FileField())
    file_title = serializers.CharField(max_length=255)
    column_mapping = serializers.JSONField(validators=[validate_column_mapping])
    values_to_replace = serializers.JSONField(validators=[validate_values_to_replace], required=False)
    sheet_mapping = serializers.JSONField(validators=[validate_file_or_sheet_mapping], required=False)
    merge_columns = serializers.JSONField(validators=[validate_merge_columns], required=False)
    file_mapping = serializers.JSONField(validators=[validate_file_or_sheet_mapping], required=False)


class BothInputSerializer(serializers.Serializer):
    trades_file = serializers.FileField(required=False)
    cashflows_file = serializers.FileField(required=False)
    file_title = serializers.CharField(max_length=255, required=False)
    column_mapping = serializers.JSONField()
    values_to_replace = serializers.JSONField(required=False)
    sheet_mapping = serializers.JSONField(required=False)
    merge_columns = serializers.JSONField(required=False)