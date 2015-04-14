from django.db import models


class ImportantManager(models.Manager):
    def get_queryset(self):
        return super(ImportantManager, self).get_queryset().filter(is_important=True)
