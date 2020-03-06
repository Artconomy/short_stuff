import re

import pytest
from rest_framework.serializers import Serializer

from .django.converters import ShortCodeConverter
from .django.serializers import ShortCodeField
from uuid import UUID


@pytest.mark.parametrize(
    "value,result",
    [('hg56ivkhm-_', True), ('ad adaf', False), ('9hervo3&*', False), ('89fwkfnd=', False), ('_-87cnDF', True),
     ('aaaaaa', True), ('111111', True), ('______', True), ('-----', True)]
)
def test_short_uid_converter_regex(value, result):
    assert bool(re.match(f'^{ShortCodeConverter.regex}$', value)) is result

def test_short_uid_converter_to_python():
    converter = ShortCodeConverter()
    assert converter.to_python('rne6yjDWT5uA') == 'rne6yjDWT5uA'


class ShortCodeSerializer(Serializer):
    test_field = ShortCodeField()


def test_short_uid_converter_to_url():
    converter = ShortCodeConverter()
    assert converter.to_url('kLOQaLheTs2A') == 'kLOQaLheTs2A'


def test_short_field_from_string():
    serializer = ShortCodeSerializer(data={'test_field': 'kLOQaLheTs2A'})
    assert serializer.is_valid() is True
    assert serializer.validated_data['test_field'] == 'kLOQaLheTs2A'


def test_short_field_to_representation():
    serializer = ShortCodeSerializer(data={'test_field': UUID('90b39068-b85e-4ecd-8000-000000000000')})
    assert serializer.is_valid() is True
    assert serializer.data['test_field'] == 'kLOQaLheTs2A'


def test_short_field_wrong_data_type():
    serializer = ShortCodeSerializer(data={'test_field': 2})
    assert serializer.is_valid() is False
    assert serializer.errors['test_field'] == ['"2" is not a valid short code.']


def test_short_field_bad_length():
    serializer = ShortCodeSerializer(data={'test_field': 'nsdfv87b34wyebfvzxucyvaso8regfamwer9tvq3w74'})
    assert serializer.is_valid() is False
    assert serializer.errors['test_field'] == ['"nsdfv87b34wyebfvzxucyvaso8regfamwer9tvq3w74" is not a valid short code.']
