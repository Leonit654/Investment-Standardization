# sync_app/admin.py
from django.contrib import admin
from .models import CardoTrade, ColumnMapping

admin.site.register(CardoTrade)
admin.site.register(ColumnMapping)
