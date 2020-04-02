import uuid
from typing import Any, Union

from rest_framework.fields import Field

from ..lib import unslugify, slugify


class ShortCodeField(Field):
    default_error_messages = {
        'invalid': '"{value}" is not a valid short code.',
    }

    def to_internal_value(self, data: Any) -> Union[str, None]:
        if data is None:
            return None
        if isinstance(data, uuid.UUID):
            return slugify(data)
        try:
            if not isinstance(data, str):
                self.fail('invalid', value=data)
            return unslugify(data) and data
        except ValueError:
            self.fail('invalid', value=data)

    def to_representation(self, value: Union[str, uuid.UUID, None]) -> Union[str, None]:
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return slugify(value)
        return value
