# sanitization.py

import pandas as pd


class Sanitizer:

    method_mapping = {
        "float": "process_float",
        "percentage": "process_percentage",
        "date": "process_date"
    }

    def __init__(self, df, data_type_mapping, columns_to_keep):
        self.df = df
        self.data_type_mapping: dict = data_type_mapping
        self.columns_to_keep = columns_to_keep

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

    def run(self):
        for key, method_name in self.method_mapping.items():
            columns = self.data_type_mapping[key]
            for column in columns:
                self.df[column] = self.df[column].apply(getattr(self, method_name))
        self.df = self.df[self.columns_to_keep]
