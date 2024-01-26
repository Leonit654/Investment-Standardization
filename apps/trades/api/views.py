import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.common.serializers import CashFlowInputSerializer
from apps.trades.api.serializers import TradeSerializer
from apps.trades.models import Trade
from services.synchronizer import Synchronizer


class TradeMappingView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        # file = request.FILES.get('file')

        serializer = CashFlowInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        synchronizer = Synchronizer(
            file=serializer.validated_data["file"],
            file_type="trade",
            columns_to_rename=serializer.validated_data["column_mapping"],
            values_to_replace={}
        )
        synchronizer.run()
        return Response("Trades uploaded successfully", status=200)
