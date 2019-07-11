import re
from uuid import uuid4, UUID

import pytest

from .lib import unslugify, slugify, gen_unique_id, ShortUIDConverter


def test_e2e_base():
    for i in range(100):
        thing = uuid4()
        assert thing == unslugify(slugify(thing))


def test_e2e_shortened():
    for i in range(100):
        thing = gen_unique_id()
        print(f"({repr(thing)}, '{slugify(thing)}')")
        assert thing == unslugify(slugify(thing))


@pytest.mark.parametrize(
    "value,result",
    [('hg56ivkhm-_', True), ('ad adaf', False), ('9hervo3&*', False), ('89fwkfnd=', False), ('_-87cnDF', True),
     ('aaaaaa', True), ('111111', True), ('______', True), ('-----', True)]
)
def test_short_uid_converter_regex(value, result):
    assert bool(re.match(f'^{ShortUIDConverter.regex}$', value)) is result


@pytest.mark.parametrize(
    "value,result", [
        ('rne6yjDWT5uA', UUID('ae77baca-30d6-4f9b-8000-000000000000')),
        ('7-G_5mpFQAKA', UUID('efe1bfe6-6a45-4002-8000-000000000000')),
        ('wfACxLnSTHGA', UUID('c1f002c4-b9d2-4c71-8000-000000000000')),
        ('IcyCZGO5T8eA', UUID('21cc8264-63b9-4fc7-8000-000000000000')),
        ('XEHJuizCR7-A', UUID('5c41c9ba-2cc2-47bf-8000-000000000000')),
        ('cMu1sRKDQsKA', UUID('70cbb5b1-1283-42c2-8000-000000000000')),
    ]
)
def test_short_uid_converter_to_python(value, result):
    converter = ShortUIDConverter()
    assert converter.to_python(value) == result


@pytest.mark.parametrize(
    "value,result", [
        (UUID('90b39068-b85e-4ecd-8000-000000000000'), 'kLOQaLheTs2A'),
        (UUID('f567b6d7-e283-4a47-8000-000000000000'), '9We21-KDSkeA'),
        (UUID('047c7259-d787-4859-8000-000000000000'), 'BHxyWdeHSFmA'),
        (UUID('3962ec0f-fe06-4770-8000-000000000000'), 'OWLsD_4GR3CA'),
        (UUID('d0c54a41-b56f-4f74-8000-000000000000'), '0MVKQbVvT3SA'),
        (UUID('39fe9fef-58ea-41a9-8000-000000000000'), 'Of6f71jqQamA'),
    ]
)
def test_short_uid_converter_to_url(value, result):
    converter = ShortUIDConverter()
    assert converter.to_url(value) == result

