import uuid
from typing import Any

from rest_framework.fields import Field

from .lib import unslugify, slugify

class ShortUIDConverter:
    """This can be plugged into Django by registering it as a URL Converter. See
    https://docs.djangoproject.com/en/2.2/_modules/django/urls/converters/ or the README for more information.
    """
    regex = r'[-a-zA-Z0-9_]{1,22}'

    def to_python(self, value: str) -> uuid.UUID:
        return unslugify(value)

    def to_url(self, value: uuid.UUID) -> str:
        return slugify(value)


class ShortUIDField(Field):
    default_error_messages = {
        'invalid': '"{value}" is not a valid short code.',
    }
    def to_internal_value(self, data: Any) -> uuid.UUID:
        if isinstance(data, uuid.UUID):
            return data
        try:
            if not isinstance(data, str):
                self.fail('invalid', value=data)
            return unslugify(data)
        except ValueError:
            self.fail('invalid', value=data)

    def to_representation(self, value: uuid.UUID) -> str:
        return slugify(value)