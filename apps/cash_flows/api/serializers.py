from rest_framework import serializers

from apps.cash_flows.models import CashFlow


class CashFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashFlow
        fields = ["trade", "identifier", "amount", "date", "cash_flow_type"]