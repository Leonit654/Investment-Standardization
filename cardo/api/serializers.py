from rest_framework import serializers
from cardo.models import Cash_flows, Trade

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = "__all__"


class CashFlowSerializer(serializers.ModelSerializer):
    trade = TradeSerializer()

    class Meta:
        model = Cash_flows
        fields = "__all__"
