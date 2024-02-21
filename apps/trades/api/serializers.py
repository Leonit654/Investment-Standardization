from apps.cash_flows.api.serializers import CashFlowSerializer
from apps.trades.models import Trade
from rest_framework import serializers


class TradeSerializer(serializers.ModelSerializer):
    cash_flows = CashFlowSerializer(many=True, read_only=True)

    class Meta:
        model = Trade
        fields = ('id', 'identifier', 'issue_date', 'maturity_date', 'invested_amount', 'interest_rate', 'organization', 'cash_flows')