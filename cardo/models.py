from django.db import models


class Trade(models.Model):
    identifier= models.CharField(max_length=100, primary_key=True)
    debtor_identifier = models.CharField(max_length=50, blank=True)
    seller_identifier = models.CharField(max_length=50, blank=True)
    issue_date=models.DateField(null=True,blank=True)
    invested_amount=models.DecimalField(null=True,max_digits=10,decimal_places=2,blank=True)
    maturity_date = models.DateField(null=True, blank=True)


    class Meta:
        verbose_name_plural = "Trades"

    def __str__(self):
        return f"Trade: {self.loan_id}"


class Cash_flows(models.Model):
    platform_transaction_id = models.CharField(primary_key=True, max_length=75)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, db_column='trade_identifier', related_name="cashflows")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp=models.DateField()
    operation=models.OneToOneField(to="Operators",related_name="operations", on_delete=models.CASCADE)


class Operators(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=25)

# Create your models here.
