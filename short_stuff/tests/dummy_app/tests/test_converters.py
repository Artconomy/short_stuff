import re

import pytest

from short_stuff.django.converters import ShortCodeConverter


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


def test_short_uid_converter_to_url():
    converter = ShortCodeConverter()
    assert converter.to_url('kLOQaLheTs2A') == 'kLOQaLheTs2A'
