import pandas as pd
from rest_framework.parsers import MultiPartParser
from services.tasks import synchronizer, logger
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import BothInputSerializer
from .models import File
import uuid
from ..cash_flows.models import CashFlow
from ..trades.models import Trade
from rest_framework.views import APIView
from rest_framework.response import Response
from django_celery_results.models import TaskResult  # Import your Task model from Django
from celery.result import AsyncResult
from django.http import Http404


class Synchronizer(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = BothInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            trades_file = serializer.validated_data.get('trades_file')
            cashflows_file = serializer.validated_data.get('cashflows_file')

            column_mapping = serializer.validated_data.get('column_mapping', {})
            values_to_replace = serializer.validated_data.get('values_to_replace', {})
            merge_columns = serializer.validated_data.get('merge_columns', {})
            sheet_mapping = serializer.validated_data.get('sheet_mapping', {})
            # Trade.objects.all().delete()
            # CashFlow.objects.all().delete()
            task_ids = []

            if trades_file:
                trade_file_identifier = str(uuid.uuid4()) + trades_file.name
                File.objects.create(file_identifier=trade_file_identifier, file=trades_file)

                task = synchronizer.apply_async(
                    kwargs={
                        'file_type': "trade",
                        'file_identifier': trade_file_identifier,
                        'columns_to_rename': column_mapping.get('trade'),
                        'merge_columns': merge_columns.get('trade', {}),
                        'values_to_replace': values_to_replace.get('trade'),
                        'sheet_mapping': sheet_mapping
                    }
                )
                task_ids.append(task.id)

            if cashflows_file:
                cashflows_file_identifier = str(uuid.uuid4()) + cashflows_file.name
                File.objects.create(file_identifier=cashflows_file_identifier, file=cashflows_file)

                task = synchronizer.apply_async(
                    kwargs={
                        'file_type': "cash_flow",
                        'file_identifier': cashflows_file_identifier,
                        'columns_to_rename': column_mapping.get('cash_flow'),
                        'merge_columns': merge_columns.get('cash_flow', {}),
                        'values_to_replace': values_to_replace.get('cash_flow'),
                    }
                )

                task_ids.append(task.id)

            return Response({"task_ids": task_ids, "message": "Synchronization started successfully."},
                            status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            logger.error(f"Error occurred during file processing: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskDetails(APIView):
    def get(self, request, task_id, format=None):
        try:
            task_result = TaskResult.objects.get(task_id=task_id)
            async_result = AsyncResult(task_id)
            response_data = {
                "task_id": task_result.task_id,
                "status": async_result.status,
                "result": str(async_result.result),
                "date_done": async_result.date_done,
                "task_kwargs": task_result.task_kwargs
            }
            return Response(response_data)
        except TaskResult.DoesNotExist:
            return Response({"error": "Task does not exist"}, status=status.HTTP_404_NOT_FOUND)



class GetColumns(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        cashflow_file = request.FILES.get('file')

        if cashflow_file:
            df_cashflow = pd.read_excel(cashflow_file)

            excel_file_columns = df_cashflow.columns
            print(excel_file_columns)

            return Response(excel_file_columns, status=status.HTTP_200_OK)
