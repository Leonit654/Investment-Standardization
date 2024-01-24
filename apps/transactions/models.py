from django.db import models

from apps.common.models import TimeStamp
from apps.trades.models import Trade


class CashFlowType(TimeStamp):
    value = models.CharField(max_length=25)


class Transaction(TimeStamp):
    identifier = models.CharField(max_length=75, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        abstract = True


class CashFlow(Transaction):
    trade = models.ForeignKey("trades.Trade", related_name="cash_flows", on_delete=models.CASCADE)
    cash_flow_type = models.ForeignKey("CashFlowType", related_name="cash_flows", on_delete=models.CASCADE)

    @classmethod
    def create(cls, data, cash_flow_type_mapping):

        cash_flows = []
        for row in data:
            trade = Trade.objects.get(identifier=row.pop("trade_identifier"))
            cash_flow_type = cash_flow_type_mapping[row.pop("cashflow_type")]
            cash_flow_type = CashFlowType.objects.get(value=cash_flow_type)
            cash_flows.append(cls(trade=trade, cash_flow_type=cash_flow_type, **row))
        cls.objects.bulk_create(cash_flows)


class CashOrder(Transaction):
    pass
