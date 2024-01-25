from django.db import models

from apps.common.models import TimeStamp


class Trade(TimeStamp):
    identifier = models.CharField(max_length=100, unique=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    maturity_date = models.DateTimeField(null=True, blank=True)
    invested_amount = models.DecimalField(null=True, max_digits=30, decimal_places=20, blank=True)
    interest_rate = models.DecimalField(max_digits=30, decimal_places=20)



