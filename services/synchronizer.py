from typing import Literal

from apps.cash_flows.api.serializers import CashFlowSerializer
from apps.trades.api.serializers import TradeSerializer
from apps.trades.services import TRADE_COLUMNS
from apps.cash_flows.services import CASH_FLOW_COLUMNS
from services.file_reader import FileReader
from services.sanitization import Sanitizer
from services.utils import invert_dict
from services.object_creation import ObjectCreator


class Synchronizer:
    model_mapping = {
        "cash_flow": CASH_FLOW_COLUMNS,
        "trade": TRADE_COLUMNS
    }

    serializer_mapping = {
        "cash_flow": CashFlowSerializer,
        "trade": TradeSerializer
    }

    def __init__(
            self,
            file,
            file_type: Literal["cash_flow", "trade"] = None,
            columns_to_rename=None,
            values_to_replace=None,
            multiple_sheets=None,
            merge_columns=None,
            file_mapping=None
    ):

        if file_mapping is None:
            file_mapping = {}

        if multiple_sheets is None:
            multiple_sheets = {}

        if values_to_replace is None:
            values_to_replace = {}

        if columns_to_rename is None:
            columns_to_rename = {}

        if merge_columns is None:
            merge_columns = {}

        self.file = file
        self.file_type = file_type
        self.columns_to_rename = columns_to_rename
        self.values_to_replace = values_to_replace
        self.multiple_sheets = multiple_sheets
        self.merge_columns = merge_columns
        self.file_mapping = file_mapping

    def get_data_type_mapping(self):
        return invert_dict(self.model_mapping[self.file_type])

    def get_columns(self):
        return self.model_mapping[self.file_type].keys()

    def run(self):
        try:
            if not self.multiple_sheets:
                for uploaded_file in self.file:
                    df = FileReader(uploaded_file).read()
                    file_name = uploaded_file.name
                    file_type = self.file_mapping.get(file_name)
                    if file_type:
                        self._process_sheet(df, file_type, file_name)
                    else:
                        print(f"File type not specified for {file_name}. Skipping.")
            else:
                # TODO: make sure we process trades first
                for sheet_name, sheet_file_type in self.multiple_sheets.items():
                    for uploaded_file in self.file:
                        df = FileReader(uploaded_file, sheet_names=[sheet_name]).read()
                        self._process_sheet(df, sheet_file_type, sheet_name)
        except Exception as e:
            raise Exception(f"Error while reading the file: {e}")

    def _process_sheet(self, df, sheet_file_type, sheet_name=None):
        try:
            self.file_type = sheet_file_type if sheet_name is not None else self.file_type
            columns_to_rename = self.columns_to_rename.get(
                self.file_type,
                {}
            ) if sheet_name is not None else self.columns_to_rename
            values_to_replace = self.values_to_replace.get(
                self.file_type,
                {}) if sheet_name is not None else self.values_to_replace

            merge_columns = self.merge_columns.get(
                self.file_type,
                {}
            ) if sheet_name is not None else self.merge_columns

            sanitizer = Sanitizer(
                df,
                merge_columns_config=merge_columns,
                data_type_mapping=self.get_data_type_mapping(),
                columns_to_keep=self.get_columns(),
                columns_to_rename=columns_to_rename,
                values_to_replace=values_to_replace,
            )
            sanitizer.run()
            data = sanitizer.to_dict()
            data_to_save = ObjectCreator(self.file_type, data)
            data_to_save.create_new_objects()
        except Exception as e:
            raise Exception(f"Error while processing data {e}")
