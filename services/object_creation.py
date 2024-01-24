# services.object_creator.py
from apps.trades.models import Trade
from apps.transactions.models import CashFlow, CashOrder, CashFlowType
from typing import Dict


class ObjectCreator:
    model_mapping = {
        "trade": Trade,
        "cash_flow": CashFlow,
        "cash_order": CashOrder,
    }

    @classmethod
    def create_objects(cls, object_type: str, data: list, additional_data: Dict = None):
        if additional_data is None:
            additional_data = {}

        model_class = cls.model_mapping.get(object_type)
        if not model_class:
            raise ValueError(f"Invalid object type: {object_type}")

        created_objects = []

        # List to hold instances before bulk_create
        instances_to_create = []

        for row in data:
            current_row_data = row.copy()

            if model_class == CashFlow:
                trade_identifier = current_row_data.pop("trade_identifier")
                cash_flow_type_value = current_row_data.pop("cashflow_type")

                trade = Trade.objects.get(identifier=trade_identifier)
                cash_flow_type = CashFlowType.objects.get(value=cash_flow_type_value)
                obj_data = {**current_row_data, "trade": trade, "cash_flow_type": cash_flow_type}
            else:
                obj_data = {**current_row_data, **additional_data}

            # Create an instance but don't save it yet
            instance = model_class(**obj_data)
            instances_to_create.append(instance)

        # Save the instances in a single bulk_create operation
        model_class.objects.bulk_create(instances_to_create)
        created_objects.extend(instances_to_create)

        return created_objects
