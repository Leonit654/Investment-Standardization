import json

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.transactions.models import CashFlow
from services.synchronizer import Synchronizer


class CashFlowView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file = request.FILES.get('file')
        column_mapping = json.loads(request.data.get('column_mapping', None))
        cash_flow_type_mapping = json.loads(request.data.get('cash_flow_type_mapping', None))
        synchronizer = Synchronizer(
            file,
            file_type="cash_flow",
            columns_to_rename=column_mapping,
            additional_data=cash_flow_type_mapping
        )
        df = synchronizer.run()
        return Response("Cash flows uploaded successfully", status=200)


