import os

import pandas as pd


class FileReader:
    def __init__(self, buffer):
        self.buffer = buffer

    def read(self):
        filename_extension = self.buffer.name.split(".")[-1]

        if filename_extension == "csv":
            return pd.read_csv(self.buffer)
        elif filename_extension == "xlsx":
            return pd.read_excel(self.buffer)
        raise f"Unsupported file format: {filename_extension}"
