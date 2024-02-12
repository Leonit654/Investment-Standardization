from django.urls import path

from apps.cash_flows.api.views import CashFlowView, CashFlowDetailView, CashFlowTypeView, CashFlowTypeDetailsView

urlpatterns = [
    path("list_cash_flows/", CashFlowView.as_view(), name="list-cash-flows"),
    path("cash_flow_detail/<str:identifier>/", CashFlowDetailView.as_view(), name="cash-flow-detail"),
    path("list_cash_flow_type/", CashFlowTypeView.as_view(), name="list-cash-flow-type"),
    path("cash_flow_type_detail/<str:value>/", CashFlowTypeDetailsView.as_view(), name="cash-flow-type-detail")
]

