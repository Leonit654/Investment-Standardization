import pandas as pd


def invert_dict(d: dict) -> dict:
    inverted_dict = {}
    for key, value in d.items():
        inverted_dict.setdefault(value, []).append(key)
    return inverted_dict


def adjust_condition(condition: dict):
    return f"(df[\"{condition['column_name']}\"] {condition['operator']} {condition['value']})"


def get_pandas_mask(df, conditions, operator):
    conditions = [adjust_condition(condition) for condition in conditions]
    mask = operator.join(conditions)
    return pd.eval(mask)
