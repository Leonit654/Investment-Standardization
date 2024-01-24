# sanitization.py

import pandas as pd


class Sanitizer:

    type_conversion_method_mapping = {
        "float": "process_float",
        "percentage": "process_percentage",
        "date": "process_date",
        "str": "process_string",
        "integer": "process_integer",
        "boolean": "process_boolean",
    }

    def __init__(self, df, data_type_mapping=None, columns_to_keep=None, columns_to_rename=None):

        if data_type_mapping is None:
            data_type_mapping = {}
        if columns_to_rename is None:
            columns_to_rename = {}

        self.df = df
        self.data_type_mapping: dict = data_type_mapping
        self.columns_to_keep = columns_to_keep
        self.columns_to_rename = columns_to_rename


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
        self.df = self.df.rename(columns=self.columns_to_rename)

    def convert_data_types(self):
        for data_type, columns in self.data_type_mapping.items():
            method_name = self.type_conversion_method_mapping[data_type]
            for column in columns:
                self.df[column] = self.df[column].apply(getattr(self, method_name))

    def keep_columns(self):
        if self.columns_to_keep:
            self.df = self.df[self.columns_to_keep]

    def to_dict(self):
        return self.df.to_dict(orient="records")

    @staticmethod
    def process_float(value):
        if pd.isna(value) or (str(value).strip() == ""):
            return None
        if isinstance(value, float):
            return value
        if isinstance(value, int):
            return float(value)

        value = str(value).translate(str.maketrans({",": "", " ": ""}))
        return round(float(value), 6)

    @staticmethod
    def process_percentage(value):
        return float(value.split('%')[0]) / 100

    @staticmethod
    def process_date(value):
        return pd.to_datetime(value, format='%d/%m/%Y')

    @staticmethod
    def process_string(value):

        if pd.isna(value) or (str(value).strip() == ""):
            return None

        if isinstance(value, float) and int(value) == value:
            value = int(value)

        return str(value)

    def run(self):
        self.rename_columns()
        self.convert_data_types()
        self.keep_columns()
