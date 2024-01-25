import json

from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.serializers import CashFlowInputSerializer
from services.synchronizer import Synchronizer


class CashFlowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = CashFlowInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        synchronizer = Synchronizer(
            serializer.validated_data["file"],
            file_type="cash_flow",
            columns_to_rename=serializer.validated_data["column_mapping"],
            values_to_replace=serializer.validated_data["values_to_replace"]
        )
        synchronizer.run()

        return Response("Cash flows uploaded successfully", status=200)


