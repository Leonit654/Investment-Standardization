from apps.trades.models import Trade
from apps.cash_flows.models import CashFlow, CashFlowType
from typing import Dict, List


class ObjectCreator:
    model_mapping = {
        "trade": Trade,
        "cash_flow": CashFlow,
    }

    def __init__(self, object_type, data: List[Dict]):
        self.object_type = object_type
        self.data = data

    def create_new_objects(self):
        try:
            model_class = self.model_mapping.get(self.object_type)
            if not model_class:
                raise ValueError(f"Invalid object type: {self.object_type}")

            instances_to_create = []

            for row in self.data:
                current_row_data = row.copy()

                if model_class == CashFlow:
                    trade_identifier = current_row_data.pop("trade_identifier")
                    cash_flow_type_value = current_row_data.pop("cash_flow_type")

                    # Try to get the Trade instance or set it to None if not found
                    trade = Trade.objects.filter(identifier=trade_identifier).first()
                    current_row_data["trade"] = trade if trade else None

                    cash_flow_type = CashFlowType.objects.get(value=cash_flow_type_value)
                    current_row_data["cash_flow_type"] = cash_flow_type

                # Check if an instance with the same data already exists in the database
                if not model_class.objects.filter(**current_row_data).exists():
                    instance = model_class(**current_row_data)
                    instances_to_create.append(instance)

            model_class.objects.bulk_create(instances_to_create)
            return instances_to_create
        except Exception as e:
            raise Exception(f"Error while creating objects: {e}")
