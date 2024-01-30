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




def pandas_merge(df, new_column_name, operation, columns_to_merge):
    operations = {
        "sum": lambda df, columns: df[columns].sum(axis=1),
        "multiply": lambda df, columns: df[columns].prod(axis=1),
        "subtract": lambda df, columns: df[columns[0]] - df[columns[1]],
    }

    if operation in operations:
        df[new_column_name] = operations[operation](df, columns_to_merge)
    else:
        raise ValueError(f"Unsupported operation: {operation}")

    return df
