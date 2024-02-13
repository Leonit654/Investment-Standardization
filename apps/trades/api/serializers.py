from apps.trades.models import Trade
from rest_framework import serializers


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['identifier', 'issue_date', 'maturity_date', 'invested_amount', 'interest_rate']
