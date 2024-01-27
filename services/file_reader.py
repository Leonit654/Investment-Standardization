import os
import pandas as pd


class FileReader:
    def __init__(self, buffer, sheet_names=None):
        self.buffer = buffer
        self.sheet_names = sheet_names

    def read(self):
        filename_extension = os.path.splitext(self.buffer.name)[-1]

        if filename_extension.lower() == ".csv":
            return pd.read_csv(self.buffer)
        elif filename_extension.lower() in [".xls", ".xlsx"]:
            if self.sheet_names:
                data_frame = {}
                for sheet_name in self.sheet_names:
                    data_frame = pd.read_excel(self.buffer, sheet_name=sheet_name)
                return data_frame
            else:

                return pd.read_excel(self.buffer)
        else:
            raise ValueError(f"Unsupported file format: {filename_extension}")

# Example usage:
# file_reader = FileReader(buffer, sheet_names=["Sheet1", "Sheet2"])
# data_frames_dict = file_reader.read()
