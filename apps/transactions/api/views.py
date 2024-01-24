import json

from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.transactions.models import CashFlow, CashOrder
from services.synchronizer import Synchronizer
from services.cash_flow_synchronizer import CashFlowSynchronizer


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
        )
        df = synchronizer.run()
        cash_flow_synchronizer =CashFlowSynchronizer(file,file_type="cash_flow",columns_to_rename=column_mapping,df=df)
        cash_flows_df = cash_flow_synchronizer.filtered_cash_flow_type_dataframe(column_name="trade_identifier",is_na=True)
        cash_orders_df = cash_flow_synchronizer.filtered_cash_flow_type_dataframe(column_name="cash_flow_type",filter="cash_order",is_na=False)
        CashFlow.create(cash_flows_df.to_dict(orient="records"), cash_flow_type_mapping)
        cash_orders_df=cash_flow_synchronizer.cash_order_df()
        CashOrder.create(cash_orders_df.to_dict(orient="records"))

        return Response("Cash flows uploaded successfully", status=200)


