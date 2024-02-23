import os

from rest_framework import serializers
from apps.trades.services import TRADE_COLUMNS
from apps.cash_flows.services import CASH_FLOW_COLUMNS


def validate_file_extension(value):
    if not hasattr(value, 'name'):
        return
    file_name, file_extension = os.path.splitext(value.name)
    allowed_extensions = ['.xlsx', '.xls', '.csv']
    if file_extension.lower() not in allowed_extensions:
        raise serializers.ValidationError("Only Excel (XLSX/XLS) and CSV files are allowed.")


def validate_key(key, valid_keys):
    if key not in valid_keys:
        raise serializers.ValidationError(f"{key} is not valid. Try to use {', '.join(valid_keys)}")


def validate_column_mapping(value):
    trade_standard_columns = list(TRADE_COLUMNS)
    cash_flow_standard_columns = list(CASH_FLOW_COLUMNS)

    if not isinstance(value, dict):
        raise serializers.ValidationError("column_mapping must be a dictionary")

    if not value:
        raise serializers.ValidationError("column_mapping dictionary must not be empty")

    at_least_one_mapping = []

    for key, mapping in value.items():
        validate_key(key, ["trade", "cash_flow"])

        if not isinstance(mapping, dict):
            raise serializers.ValidationError(f"Mapping columns for key '{key}' must be a dict")
        if not mapping:
            at_least_one_mapping.append(False)
        else:
            at_least_one_mapping.append(True)
        for user_field, standard_field in mapping.items():
            if not user_field or not standard_field:
                raise serializers.ValidationError("Both user_field and standard_field must be provided")

            if key == "trade":
                if standard_field not in trade_standard_columns:
                    raise serializers.ValidationError(
                        f"{standard_field} is not a valid column name for 'trade'. Valid columns are: {trade_standard_columns}"
                    )
            elif key == "cash_flow":
                if standard_field not in cash_flow_standard_columns:
                    raise serializers.ValidationError(
                        f"{standard_field} is not a valid column name for 'cash_flow'. Valid columns are: {cash_flow_standard_columns}"
                    )

    if not any(at_least_one_mapping):
        raise serializers.ValidationError("At least one column mapping must be provided for 'trade' or 'cash_flow'")

    return value


def validate_values_to_replace(value):
    columns_dicts = {"trade": TRADE_COLUMNS, "cash_flow": CASH_FLOW_COLUMNS}

    if not isinstance(value, dict):
        raise serializers.ValidationError("Values to replace must be a dictionary")

    if not value:
        raise serializers.ValidationError("Values to replace dictionary must not be empty")

    keys_to_delete = []
    for key, replace_items in value.items():
        validate_key(key, ["trade", "cash_flow"])
        if replace_items is None or replace_items == []:
            keys_to_delete.append(key)
            continue
        if not isinstance(replace_items, list):
            raise serializers.ValidationError(f"Replace items for key '{key}' must be a list")

        for replace_item in replace_items:
            if not isinstance(replace_item, dict):
                raise serializers.ValidationError(f"Each replace item for key '{key}' must be a dictionary")

            required_keys = ["column_name", "operator", "value", "condition"]
            for req_key in required_keys:
                if req_key not in replace_item:
                    raise serializers.ValidationError(f"'{req_key}' is required in each replace item for key '{key}'")
                if not replace_item[req_key]:
                    raise serializers.ValidationError(f"'{req_key}' in replace item for key '{key}' cannot be empty")

            # column_name = replace_item.get("column_name")
            # validate_key(column_name, columns_dicts.get(key, {}))

            operator_value = replace_item.get("operator")
            common_operators = ["&", "|"]
            if operator_value not in common_operators:
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
                    if not condition_item[condition_key]:
                        raise serializers.ValidationError(
                            f"'{condition_key}' in condition item for key '{key}' cannot be empty")

    for key in keys_to_delete:
        del value[key]

    return value


def validate_merge_columns(value):
    if not value:
        raise serializers.ValidationError("You need to fill all the fields")

    allowed_operators = ["sum", "subtract", "multiply"]

    if not isinstance(value, dict):
        raise serializers.ValidationError("Value must be a dictionary")

    value_copy = value.copy()

    for merge_config, merge_list in value_copy.items():
        if not merge_list:
            del value[merge_config]
        else:
            if not isinstance(merge_list, list):
                raise serializers.ValidationError("Each value must be a list")
            for merge in merge_list:
                required_keys = ["new_column_name", "operator", "columns_to_merge"]
                for req_key in required_keys:
                    if req_key not in merge:
                        raise serializers.ValidationError(f"'{req_key}' is required in each merge column configuration")
                    elif req_key == "columns_to_merge":
                        if not merge[req_key]:
                            raise serializers.ValidationError(
                                "'columns_to_merge' cannot be empty in each merge column  configuration")
                        elif not all(column.strip() for column in merge[req_key]):
                            raise serializers.ValidationError(
                                f"{merge_config} 'columns_to_merge' elements cannot be empty or contain only "
                                f"whitespace in each merge column  configuration")
                    elif not merge[req_key] or merge[req_key].strip() == "":
                        raise serializers.ValidationError(
                            f"'{req_key}' cannot be empty or contain only whitespace in each merge column configuration")

                operator_value = merge.get("operator")
                if operator_value not in allowed_operators:
                    raise serializers.ValidationError(
                        f"'{operator_value}' is not a valid operator. Try to use operators like {', '.join(allowed_operators)}")

                columns_to_merge = merge.get("columns_to_merge", [])
                if not all(isinstance(column, str) for column in columns_to_merge):
                    raise serializers.ValidationError("columns_to_merge must be a list of column names")

    return value


def validate_file_or_sheet_mapping(value):
    valid_keys = ['trade', 'cash_flow']

    if not isinstance(value, dict):
        raise serializers.ValidationError("This field must be a dictionary")

    if not value:
        raise serializers.ValidationError("This field dictionary must not be empty")

    for key in value.values():
        if key not in valid_keys:
            raise serializers.ValidationError(f"'{key}' is not a valid value. Try to use 'trade' or 'cash_flow'")
