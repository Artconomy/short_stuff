from django.db import models
from short_stuff.lib import gen_shortcode
from short_stuff.django.models import ShortCodeField


class ShortStuffModel(models.Model):
    id = ShortCodeField(default=gen_shortcode, primary_key=True)
    test_token = ShortCodeField(null=True)

