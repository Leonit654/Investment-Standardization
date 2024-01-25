# services.object_creator.py
from apps.trades.models import Trade
from apps.cash_flows.models import CashFlow, CashFlowType
from typing import Dict


class ObjectCreator:
    model_mapping = {
        "trade": Trade,
        "cash_flow": CashFlow,
    }

    @classmethod
    def create_objects(cls, object_type: str, data: list[dict]):

        model_class = cls.model_mapping.get(object_type)
        if not model_class:
            raise ValueError(f"Invalid object type: {object_type}")

        instances_to_create = []

        for row in data:
            current_row_data = row.copy()

            if model_class == CashFlow:
                trade_identifier = current_row_data.pop("trade_identifier")
                cash_flow_type_value = current_row_data.pop("cash_flow_type")

                trade = Trade.objects.filter(identifier=trade_identifier).first()
                cash_flow_type = CashFlowType.objects.get(value=cash_flow_type_value)
                current_row_data = {**current_row_data, "trade": trade, "cash_flow_type": cash_flow_type}

            instance = model_class(**current_row_data)
            instances_to_create.append(instance)

        model_class.objects.bulk_create(instances_to_create)

        return instances_to_create
