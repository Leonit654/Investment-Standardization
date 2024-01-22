"""
URL configuration for Investment_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.trades.api.views import *

urlpatterns = [
    path("trades_columns/", GetTradeColumns.as_view(), name="upload-trade-files"),

    path("realized_amount/<str:identifier>/", RealizedAmountView.as_view(), name="realized-amount"),
    path("gross_expected_amount/<str:identifier>/", GrossExpectedAmountView.as_view(), name="gross-expected-amount"),
    path("remaining_invested_amount/<str:identifier>/", RemainingInvestedAmountView.as_view(), name="remaining-invested-amount"),
    path("closing_date/<str:identifier>/", ClosingDateView.as_view(), name="closing-date"),
    path('trades/', TradeListView.as_view(), name='trade-list'),
    path('trade/<str:identifier>/', TradeDetailView.as_view(), name='trade-detail'),


    path("trade_mapping/", TradeMappingView.as_view(), name="mapping"),
]
