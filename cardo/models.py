# sync_app/models.py
from django.db import models

class CardoTrade(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    issue_date = models.DateField()
    maturity_date = models.DateField()
    invested_amount = models.FloatField()
    debtor_identifier = models.CharField(max_length=255)
    seller_identifier = models.CharField(max_length=255)

class CardoTransaction(models.Model):
    operation = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    amount = models.FloatField()
    trade_identifier = models.CharField(max_length=255)
    platform_transaction_id = models.CharField(max_length=255)

# sync_app/models.py


class ColumnMapping(models.Model):
    raw_column = models.CharField(max_length=255, choices=[])  # choices will be populated dynamically
    standardized_column = models.CharField(max_length=255, choices=[])  # choices will be populated dynamically
    data_type = models.CharField(max_length=255)

