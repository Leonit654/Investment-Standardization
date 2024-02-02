from apps.trades.models import Trade
from apps.cash_flows.models import CashFlow, CashFlowType
from django.core.exceptions import ValidationError


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

        identifiers = {row.get("identifier") for row in data if row.get("identifier")}

        existing_identifiers = set(
            model_class.objects.filter(identifier__in=identifiers).values_list('identifier', flat=True))
        data_without_existing = [row for row in data if row.get("identifier") not in existing_identifiers]

        instances_to_create = []

        for row in data_without_existing:
            current_row_data = row.copy()
            try:
                if model_class == CashFlow:
                    trade_identifier = current_row_data.pop("trade_identifier")
                    cash_flow_type_value = current_row_data.pop("cash_flow_type")

                    trade = Trade.objects.get(identifier=trade_identifier)
                    cash_flow_type = CashFlowType.objects.get(value=cash_flow_type_value)
                    current_row_data["trade"] = trade
                    current_row_data["cash_flow_type"] = cash_flow_type

                instance = model_class(**current_row_data)
                instance.full_clean()
                instances_to_create.append(instance)
            except ValidationError as e:
                error_messages = {}
                for field, error_list in e.message_dict.items():
                    error_messages[field] = ", ".join(error_list)
                return error_messages

        model_class.objects.bulk_create(instances_to_create)

        return instances_to_create
