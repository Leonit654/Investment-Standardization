from rest_framework import serializers
from cardo.models import Cash_flows, Trade, Operators


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = "__all__"


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operators
        fields = "__all__"


class CashFlowSerializer(serializers.Serializer):

    trade = TradeSerializer()
    operation = OperationSerializer()


    class Meta:
        model = Cash_flows
        fields = "__all__"


class CashFlowWithTransactionTypeSerializer(serializers.ModelSerializer):
    transaction_type = serializers.ReadOnlyField(source='operation.transaction_type')

    class Meta:
        model = Cash_flows
        fields = "__all__"
