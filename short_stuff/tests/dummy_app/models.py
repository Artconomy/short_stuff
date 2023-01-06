from django.db import models
from short_stuff.django.models import ShortCodeField


class ShortStuffModel(models.Model):
    id = ShortCodeField(primary_key=True)
    test_token = ShortCodeField(null=True)

