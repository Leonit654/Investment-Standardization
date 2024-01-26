from typing import Literal

from apps.cash_flows.api.serializers import CashFlowSerializer
from apps.trades.api.serializers import TradeSerializer
from apps.trades.services import TRADE_COLUMNS
from apps.cash_flows.services import CASH_FLOW_COLUMNS
from services.file_reader import FileReader
from services.object_creation import ObjectCreator
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

    def __init__(self, file, file_type: Literal["cash_flow", "trade"], columns_to_rename=None, values_to_replace=None):

        if values_to_replace is None:
            values_to_replace = {}
        if columns_to_rename is None:
            columns_to_rename = {}

        self.file = file
        self.file_type = file_type
        self.columns_to_rename = columns_to_rename
        self.values_to_replace = values_to_replace

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
            columns_to_rename=self.columns_to_rename,
            values_to_replace=self.values_to_replace,
        )

        sanitizer.run()
        # TODO: Use serializer to validate data and crate Trade and CashFlow
        serializer_class = self.serializer_mapping[self.file_type]

        serializer = serializer_class(data=sanitizer.df.to_dict(orient="records"), many=True)
        if serializer.is_valid():
            serializer.save()
            serializer.bulk_create(serializer)
        else:
            print(serializer.errors)


        # if serializer.is_valid():
        #     # Call the bulk_create method
        #     cash_flows_created = serializer.bulk_create(serializer.validated_data)
        #     print("Cash flows created successfully:", cash_flows_created)
        # else:
        #     print("Data is not valid:", serializer.errors)
        return sanitizer.df