from django.db import models
from datetime import datetime 

class LineUser(models.Model):
    userId = models.TextField(blank=True, null=True)

class LineRecord(models.Model):
    userId = models.TextField(blank=True , null=True)
    recordType = models.IntegerField(blank=True , null=True)
    recordContent = models.TextField(blank=True, null=True)
    recordCount = models.IntegerField(blank=True , null=True)
    recordDate = models.DateTimeField(default=datetime.now, blank=True)
