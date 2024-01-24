from django.db import models

from apps.common.models import TimeStamp


class Trade(TimeStamp):
    identifier = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField(null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    invested_amount = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    @classmethod
    def create(cls, data):
        trades = [cls(**row) for row in data]

        cls.objects.bulk_create(trades)

