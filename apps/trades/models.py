from django.db import models

from apps.common.models import TimeStamp


class Trade(TimeStamp):
    identifier = models.CharField(max_length=100)
    issue_date = models.DateField(null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    invested_amount = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    @classmethod
    def get_field_names(cls):
        return [f.name for f in cls._meta.get_fields() if f.name not in ["created_at", "updated_at", "id", "cash_flows"]]

    @staticmethod
    def get_field_types():
        return {
            "date": ["issue_date", "maturity_date"],
            "percentage": ["interest_rate"],
            "float": ["invested_amount"]
        }
