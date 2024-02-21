from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cash_flows.api.serializers import CashFlowSerializer
from apps.cash_flows.models import CashFlow
from apps.trades.models import Trade




class CashFlowList(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        org_id = request.query_params.get('organizationId')
        if org_id:
            trades_with_org_id = Trade.objects.filter(organization_id=org_id)
            cash_flows = CashFlow.objects.filter(trade__in=trades_with_org_id)
        else:
            return Response("Provide ORG ID", status=status.HTTP_400_BAD_REQUEST)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(cash_flows, request)
        serializer = CashFlowSerializer(result_page, many=True)

        response_data = {
            'results': serializer.data,
            'total_pages': paginator.page.paginator.num_pages,
        }

        return Response(response_data)

    def post(self, request):
        serializer = CashFlowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

