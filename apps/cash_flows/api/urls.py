from django.urls import path

from apps.cash_flows.api.views import CashFlowList

urlpatterns = [
    path("get-create/", CashFlowList.as_view(), name="get-create")
]
