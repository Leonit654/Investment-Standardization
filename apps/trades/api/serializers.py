from apps.trades.models import Trade
from rest_framework import serializers


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['identifier', 'issue_date', 'maturity_date', 'invested_amount', 'interest_rate']
    def validate(self, data):
        # Check if there are existing rows in the database that conflict with the submitted data
        conflicting_instances = Trade.objects.filter(**data)
        if conflicting_instances.exists():
            # If there are conflicts, raise a validation error
            raise serializers.ValidationError("This location already exists.")
        return data