# serializers.py

from rest_framework import serializers
from cardo.models import *
class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cash_flows
        fields = '__all__'

class TradeDetailSerializer(serializers.ModelSerializer):
    cashflows = CashFlowSerializer(many=True, read_only=True)

    class Meta:
        model = Trade
        fields = '__all__'

class TradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
