from uuid import uuid4

import pytest

from .lib import unslugify, slugify, gen_unique_id, pad_guid_bytes, gen_guid


def test_e2e_base():
    for i in range(100):
        thing = uuid4()
        assert thing == unslugify(slugify(thing))


def test_e2e_shortened():
    for i in range(100):
        thing = gen_unique_id()
        print(f"({repr(thing)}, '{slugify(thing)}')")
        assert thing == unslugify(slugify(thing))


def test_pad_guid_bytes():
    with pytest.raises(ValueError):
        pad_guid_bytes(b'')


def test_gen_guid_limit():
    with pytest.raises(ValueError):
        gen_guid(0)
