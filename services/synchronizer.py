from typing import Literal

from apps.trades.services import TRADE_COLUMNS
from apps.transactions.services import CASH_FLOW_COLUMNS
from services.file_reader import FileReader
from services.object_creation import ObjectCreator
from services.sanitization import Sanitizer
from services.utils import invert_dict


class Synchronizer:
    model_mapping = {
        "cash_flow": CASH_FLOW_COLUMNS,
        "trade": TRADE_COLUMNS
    }

    def __init__(self, file, file_type: Literal["cash_flow", "trade"], columns_to_rename=None,additional_data={}):

        if columns_to_rename is None:
            columns_to_rename = {}

        self.file = file
        self.file_type = file_type
        self.columns_to_rename = columns_to_rename
        self.additional_data = additional_data
    def get_data_type_mapping(self):
        return invert_dict(self.model_mapping[self.file_type])

    def get_columns(self):
        return self.model_mapping[self.file_type].keys()

    def run(self):
        df = FileReader(self.file).read()
        sanitizer = Sanitizer(
            df,
            data_type_mapping=self.get_data_type_mapping(),
            columns_to_keep=self.get_columns(),
            columns_to_rename=self.columns_to_rename
        )
        sanitizer.run()
        ObjectCreator.create_objects(self.file_type, sanitizer.df.to_dict('records'), self.additional_data)
        return sanitizer.df
