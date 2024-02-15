# sanitization.py

import pandas as pd
from services.utils import get_pandas_mask, pandas_merge


class Sanitizer:

    type_conversion_method_mapping = {
        "float": "process_float",
        "percentage": "process_percentage",
        "date": "process_date",
        "str": "process_string",
        "integer": "process_integer",
        "boolean": "process_boolean",
    }

    def __init__(
            self,
            df,
            data_type_mapping=None,
            columns_to_keep=None,
            columns_to_rename=None,
            values_to_replace=None,
            merge_columns_config=None
    ):

        if values_to_replace is None:
            values_to_replace = []
        if data_type_mapping is None:
            data_type_mapping = {}
        if columns_to_rename is None:
            columns_to_rename = {}
        if merge_columns_config is None:
            merge_columns_config = {}

        self.df = df
        self.data_type_mapping: dict = data_type_mapping
        self.columns_to_keep = columns_to_keep
        self.columns_to_rename = columns_to_rename
        self.values_to_replace = values_to_replace
        self.merge_columns_config = merge_columns_config

    def clear_column_spaces(self):
        self.df.columns = [col.strip() for col in self.df.columns]

    def merge_columns(self):
        for merge_config in self.merge_columns_config:
            new_column_name = merge_config.get("new_column_name")
            operation = merge_config.get("operator")
            columns_to_merge = merge_config.get("columns_to_merge")
            pandas_merge(self.df, new_column_name, operation, columns_to_merge)

    @staticmethod
    def process_integer(value):
        if pd.isna(value) or (str(value).strip() == ""):
            return None
        return int(value)

    @staticmethod
    def process_boolean(value):
        if pd.isna(value) or (str(value).strip() == ""):
            return None
        return str(value).lower() in ['true', 'yes', '1']

    def rename_columns(self):
        columns_to_rename_no_spaces = {key.strip(): value for key, value in self.columns_to_rename.items()}
        self.df = self.df.rename(columns=columns_to_rename_no_spaces)

    def convert_data_types(self):
        for data_type, columns in self.data_type_mapping.items():
            method_name = self.type_conversion_method_mapping[data_type]
            for column in columns:
                self.df[column] = self.df[column].apply(getattr(self, method_name))

    def keep_columns(self):
        if self.columns_to_keep:
            self.df = self.df[self.columns_to_keep]

    def replace_values(self):
        for value_to_replace in self.values_to_replace:
            column_name = value_to_replace["column_name"]
            new_value = value_to_replace["value"]
            operator = value_to_replace["operator"]
            condition = value_to_replace["condition"]
            mask = get_pandas_mask(self.df, condition, operator)
            self.df.loc[mask, column_name] = new_value

    def to_dict(self):

        return self.df.to_dict(orient="records")

    @staticmethod
    def process_float(value, decimal_places=2):
        if pd.isna(value) or (str(value).strip() == ""):
            return None
        if isinstance(value, str):
            value = value.translate(str.maketrans({",": "", " ": ""}))

        if decimal_places is None:
            return float(value)

        return round(float(value), decimal_places)

    @staticmethod
    def process_percentage(value):
        try:
            float_value = float(value)
            if 0 <= float_value <= 100:
                return float_value
            else:
                raise ValueError("Float value outside the valid percentage range [0, 1]")
        except (ValueError, TypeError):
            return float(value.split('%')[0]) / 100

    @staticmethod
    def process_date(value):
        return pd.to_datetime(value, format='%d/%m/%Y').date()

    @staticmethod
    def process_string(value):
        if pd.isna(value) or (str(value).strip() == ""):
            return None
        if isinstance(value, float) and int(value) == value:
            value = int(value)
        return str(value)

    def run(self):
        try:
            print("Starting Sanitization")
            print("Clearing column spaces")
            self.clear_column_spaces()
            self.merge_columns()
            print("Replacing Values")
            self.replace_values()
            print("Renaming columns")
            self.rename_columns()
            print("Converting data types")
            self.convert_data_types()
            self.keep_columns()
            print("Finished Sanitization")
        except Exception as e:
            raise Exception(f"Error while sanitizing data: {e}")
