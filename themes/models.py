import uuid

from django.db import models


class Theme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
