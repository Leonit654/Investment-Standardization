from django.db import models

from apps.common.models import TimeStamp


class CashFlowType(TimeStamp):
    value = models.CharField(max_length=25)


class Transaction(TimeStamp):
    identifier = models.CharField(primary_key=True, max_length=75)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateField()

    class Meta:
        abstract = True


class CashFlow(Transaction):
    trade = models.ForeignKey("trades.Trade", related_name="cash_flows", on_delete=models.CASCADE)
    operation = models.ForeignKey("CashFlowType", related_name="cash_flows", on_delete=models.CASCADE)


class CashOrder(Transaction):
    pass
