from django.core.files.storage import FileSystemStorage
from django.db import models


fs = FileSystemStorage(location="./uploads/")


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RawData(TimeStamp):
    file_title = models.CharField(max_length=255, unique=True)
    file = models.FileField(storage=fs)

class File(models.Model):
    file_identifier = models.CharField(max_length=400, unique=True)
    file = models.FileField(storage=fs)