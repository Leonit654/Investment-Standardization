from django.db import models

from apps.common.models import TimeStamp
from apps.trades.models import Trade


class CashFlowType(TimeStamp):
    value = models.CharField(max_length=25)


    def __str__(self):
        # TODO: I suggest we return self.value in here
        return self.id


class CashFlow(TimeStamp):
    trade = models.ForeignKey("trades.Trade", related_name="cash_flows", on_delete=models.CASCADE, null=True)
    identifier = models.CharField(max_length=75, unique=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    date = models.DateField()
    cash_flow_type = models.ForeignKey("CashFlowType", related_name="cash_flows", on_delete=models.CASCADE)


