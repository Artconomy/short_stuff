from uuid import uuid4

from .lib import unslugify, slugify, gen_unique_id, pad_guid_bytes


def test_e2e_base():
    for i in range(100):
        thing = uuid4()
        assert thing == unslugify(slugify(thing))


def test_e2e_shortened():
    for i in range(100):
        thing = gen_unique_id()
        print(f"({repr(thing)}, '{slugify(thing)}')")
        assert thing == unslugify(slugify(thing))
