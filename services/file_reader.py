import os
import logging
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from apps.common.models import File

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileReader:
    def __init__(self, file_identifier, sheet_names=None):
        self.file_identifier = file_identifier
        self.sheet_names = sheet_names

    def read(self):
        try:
            file_obj = File.objects.get(file_identifier=self.file_identifier)
            file_name = os.path.basename(file_obj.file.path)
        except ObjectDoesNotExist:
            raise FileNotFoundError(f"File with identifier '{self.file_identifier}' does not exist.")

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        management_dir = "Investment_Management"
        uploads_dir = "uploads"

        file_dir = os.path.join(base_dir, management_dir, uploads_dir)

        new_file_path = os.path.join(file_dir, file_name)
        if not os.path.exists(new_file_path):
            raise FileNotFoundError(f"File '{new_file_path}' does not exist.")
        try:
            filename_extension = os.path.splitext(new_file_path)[-1]
            if filename_extension.lower() == ".csv":
                return pd.read_csv(new_file_path)
            elif filename_extension.lower() in [".xls", ".xlsx"]:
                if self.sheet_names:
                    data_frame = {}
                    for sheet_name in self.sheet_names:
                        data_frame = pd.read_excel(new_file_path, sheet_name=sheet_name)
                    return data_frame
                else:
                    return pd.read_excel(new_file_path)

            else:
                raise ValueError(f"Unsupported file format: {filename_extension}")
        except Exception as e:
            logger.error(f"Error reading file '{new_file_path}': {e}")
            raise e
