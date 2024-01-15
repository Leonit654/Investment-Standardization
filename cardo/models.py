from django.db import models


class Trade(models.Model):
    loan_id = models.CharField(primary_key=True, max_length=50)
    issue_date = models.DateField()
    maturity_date = models.DateField()
    invested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    debtor_identifier = models.CharField(max_length=50)
    seller_identifier = models.CharField(max_length=50)


class Cash_flows(models.Model):
    cashflow_id = models.CharField(primary_key=True, max_length=75)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, db_column='trade_id', related_name="cashflows")
    cashflow_date = models.DateField()
    cashflow_currency = models.CharField(max_length=10)
    cashflow_type = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

# Create your models here.
