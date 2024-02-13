from django.urls import path
from apps.trades.api.views import *

urlpatterns = [
    path("realized_amount/<str:identifier>/", RealizedAmountView.as_view(), name="realized-amount"),
    path("gross_expected_amount/<str:identifier>/", GrossExpectedAmountView.as_view(), name="gross-expected-amount"),
    path(
        "remaining_invested_amount/<str:identifier>/", RemainingInvestedAmountView.as_view(),
        name="remaining-invested-amount"
    ),
    path("closing_date/<str:identifier>/", ClosingDateView.as_view(), name="closing-date"),
]
