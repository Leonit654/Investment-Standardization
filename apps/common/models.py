from django.core.files.storage import FileSystemStorage
from django.db import models

fs = FileSystemStorage(location="./Investment_Management/uploads/")


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class File(models.Model):
    file_identifier = models.CharField(max_length=400, unique=True)
    file = models.FileField(storage=fs)