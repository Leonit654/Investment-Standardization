from django.core.files.storage import FileSystemStorage
from django.db import models
from apps.organization.models import Organization

fs = FileSystemStorage(location="./Investment_Management/uploads/")





class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class File(models.Model):
    file_identifier = models.CharField(max_length=400, unique=True)
    file = models.FileField(storage=fs)


class Configuration(models.Model):
    config_name = models.CharField(max_length=100, unique=True)
    trades_file = models.FileField(storage=fs, null=True, blank=True)
    cashflows_file = models.FileField(storage=fs, null=True, blank=True)
    file_title = models.CharField(max_length=255, null=True, blank=True)
    column_mapping = models.JSONField()
    values_to_replace = models.JSONField(null=True, blank=True)
    sheet_mapping = models.JSONField(null=True, blank=True)
    merge_columns = models.JSONField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, related_name='configurations')