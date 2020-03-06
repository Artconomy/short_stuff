import uuid

from django.core import exceptions
from django.db.models import UUIDField
from django import forms

from ..lib import unslugify, slugify


class ShortCodeField(UUIDField):
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.to_python(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return unslugify(value)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            value = value
        elif isinstance(value, str):
            value = unslugify(value)
        else:
            raise ValueError(f'Cannot convert {repr(value)} to UUD.')

        if connection.features.has_native_uuid_field:
            return value
        return value.hex

    def from_db_value(self, value, expression, connection):
        return value and slugify(value)

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if not isinstance(value, uuid.UUID):
            input_form = 'int' if isinstance(value, int) else 'hex'
            try:
                value = uuid.UUID(**{input_form: value})
            except (AttributeError, ValueError):
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return slugify(value)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.CharField,
            **kwargs,
        })
