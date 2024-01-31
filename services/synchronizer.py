from typing import Literal

from apps.cash_flows.api.serializers import CashFlowSerializer
from apps.trades.api.serializers import TradeSerializer
from apps.trades.services import TRADE_COLUMNS
from apps.cash_flows.services import CASH_FLOW_COLUMNS
from services.file_reader import FileReader
from services.sanitization import Sanitizer
from services.utils import invert_dict


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
            self, file, file_type: Literal["cash_flow", "trade"] = None, columns_to_rename=None,
            values_to_replace=None,
            multiple_sheets=None):

        if multiple_sheets is None:
            multiple_sheets = {}

        if values_to_replace is None:
            values_to_replace = {}
        if columns_to_rename is None:
            columns_to_rename = {}

        self.file = file
        self.file_type = file_type
        self.columns_to_rename = columns_to_rename
        self.values_to_replace = values_to_replace
        self.multiple_sheets = multiple_sheets

    def get_data_type_mapping(self):
        return invert_dict(self.model_mapping[self.file_type])

    def get_columns(self):
        return self.model_mapping[self.file_type].keys()

    def run(self):
        if not self.multiple_sheets:
            # If no specific sheets are provided, process the entire file as a single sheet
            df = FileReader(self.file).read()
            self._process_sheet(df, self.file_type)
        else:
            for sheet_name, sheet_file_type in self.multiple_sheets.items():
                df = FileReader(self.file, sheet_names=[sheet_name]).read()
                self._process_sheet(df, sheet_file_type, sheet_name)

    def _process_sheet(self, df, sheet_file_type, sheet_name=None):
        self.file_type = sheet_file_type if sheet_name is not None else self.file_type
        columns_to_rename = self.columns_to_rename.get(
            self.file_type,
            {}) if sheet_name is not None else self.columns_to_rename
        sanitizer = Sanitizer(
            df,
            data_type_mapping=self.get_data_type_mapping(),
            columns_to_keep=self.get_columns(),
            columns_to_rename=columns_to_rename,
            values_to_replace=self.values_to_replace if self.file_type == "cash_flow" else None,
        )
        sanitizer.run()
        data = sanitizer.to_dict()
        serializer_class = self.serializer_mapping.get(self.file_type)
        if serializer_class:
            serializer = serializer_class(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Validation error for {sheet_file_type} - Sheet {sheet_name}:", serializer.errors)
        else:
            print(f"No serializer found for {sheet_file_type} - Sheet {sheet_name}")
