from apps.trades.models import Trade
from apps.cash_flows.models import CashFlow, CashFlowType
from typing import Dict, List

from services.file_reader import logger


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
            instances_to_update = []

            for row in self.data:
                current_row_data = row.copy()

                if model_class == CashFlow:
                    trade_identifier = current_row_data.pop("trade_identifier")
                    cash_flow_type_value = current_row_data.pop("cash_flow_type")

                    trade = Trade.objects.filter(identifier=trade_identifier).first()
                    current_row_data["trade"] = trade if trade else None

                    cash_flow_type = CashFlowType.objects.get(value=cash_flow_type_value)
                    current_row_data["cash_flow_type"] = cash_flow_type

                identifier = current_row_data.get('identifier')
                existing_object = model_class.objects.filter(identifier=identifier).first()
                if existing_object:
                    for attr, value in current_row_data.items():
                        setattr(existing_object, attr, value)
                    instances_to_update.append(existing_object)
                else:
                    instance = model_class(**current_row_data)
                    instances_to_create.append(instance)

            model_class.objects.bulk_create(instances_to_create)

            for obj in instances_to_update:
                obj.save()

            return instances_to_create + instances_to_update
        except Exception as e:
            raise Exception(f"Error while creating/updating objects: {e}")
