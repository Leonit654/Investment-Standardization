from django.db import models


class Trade(models.Model):
    loan_id = models.CharField(max_length=255, null=True, blank=True)
    debtor_identifier = models.IntegerField(null=True, blank=True)
    seller_identifier = models.IntegerField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    investment_date = models.DateTimeField(null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    trade_receivable_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchase_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    outstanding_principal_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    approved_limit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    maturity_date = models.DateTimeField(null=True, blank=True)
    extension_date = models.DateTimeField(null=True, blank=True)
    interest_rate_exp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    expected_net_return = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    trade_receivable_status = models.CharField(max_length=50, null=True, blank=True)
    days_in_delay = models.IntegerField(null=True, blank=True)
    performance_status = models.CharField(max_length=50, null=True, blank=True)
    default_date = models.DateTimeField(null=True, blank=True)
    default_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    write_off_date = models.DateTimeField(null=True, blank=True)
    write_off_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    repurchased = models.BooleanField(null=True, blank=True)
    current_rating = models.CharField(max_length=50, null=True, blank=True)
    rating_source = models.CharField(max_length=50, null=True, blank=True)
    day_count_convention = models.CharField(max_length=50, null=True, blank=True)
    rollovered_status = models.CharField(max_length=50, null=True, blank=True)
    rollovered_id = models.IntegerField(null=True, blank=True)
    rollovered_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    company_bankrupted_status = models.CharField(max_length=50, null=True, blank=True)
    company_bankrupted_date = models.DateTimeField(null=True, blank=True)
    related_parties = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Trades"

    def __str__(self):
        return f"Trade: {self.loan_id}"


class Cash_flows(models.Model):
    cashflow_id = models.CharField(primary_key=True, max_length=75)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, db_column='trade_id', related_name="cashflows")
    cashflow_date = models.DateField()
    cashflow_currency = models.CharField(max_length=10)
    cashflow_type = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Operators(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=25)

# Create your models here.
