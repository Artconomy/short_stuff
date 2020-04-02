import json
from unittest.mock import Mock
from uuid import uuid4

import pytest

from django.core import serializers
from django.core.exceptions import ValidationError
from django.forms.fields import CharField, IntegerField
from short_stuff.lib import unslugify, slugify, gen_shortcode, gen_shortcode_uuid
from short_stuff.tests.dummy_app.models import ShortStuffModel

pytestmark = pytest.mark.django_db


def test_primary_key():
    new = ShortStuffModel()
    new.save()
    model_id = new.id
    assert type(model_id) == str
    assert slugify(unslugify(model_id)) == model_id
    new.refresh_from_db()
    assert model_id == new.id


def test_serialize_to_string():
    new = ShortStuffModel()
    new.save()
    data = serializers.serialize("json", ShortStuffModel.objects.all())
    assert json.loads(data) == [{"model": "dummy_app.shortstuffmodel", "pk": new.id, "fields": {"test_token": None}}]


def test_get_prep_null():
    null_token = ShortStuffModel()
    null_token.save()
    ShortStuffModel(test_token=gen_shortcode())
    results = ShortStuffModel.objects.filter(test_token=None)
    assert results.count() == 1
    assert results[0] == null_token


def test_uuid_query():
    ShortStuffModel().save()
    new = ShortStuffModel()
    new.save()
    results = ShortStuffModel.objects.filter(id=unslugify(new.id))
    assert results.count() == 1
    assert results[0] == new


def test_fail_bogus_value():
    new = ShortStuffModel()
    new.test_token = 1
    with pytest.raises(ValueError):
        new.save()


def test_non_native_uuid():
    mock_connection = Mock()
    mock_connection.features.has_native_uuid_field = False
    input_uuid = uuid4()
    result = ShortStuffModel._meta.fields[0].get_db_prep_value(input_uuid, mock_connection, prepared=False)
    assert result == input_uuid.hex


def test_native_uuid():
    # SQLite does not have a native UUID field as of the current Django version.
    mock_connection = Mock()
    mock_connection.features.has_native_uuid_field = True
    input_uuid = uuid4()
    result = ShortStuffModel._meta.fields[0].get_db_prep_value(input_uuid, mock_connection, prepared=False)
    assert result == input_uuid


def test_to_python_null():
    # Can't find a way to make this happen via natural APIs, but docs require it to be handled.
    assert ShortStuffModel._meta.fields[1].to_python(None) is None


def test_to_python_not_null():
    # Should not be handled if the field cannot be nulled
    with pytest.raises(ValidationError):
        ShortStuffModel._meta.fields[0].to_python(None)


def test_to_python_uuid():
    shortcode = gen_shortcode_uuid()
    assert ShortStuffModel._meta.fields[0].to_python(shortcode) == slugify(shortcode)


def test_form_field_default():
    field = ShortStuffModel._meta.fields[0].formfield()
    assert type(field) == CharField


def test_form_field_additional():
    field = ShortStuffModel._meta.fields[0].formfield(max_length=42)
    assert type(field) == CharField
    assert field.max_length == 42


def test_form_field_override():
    field = ShortStuffModel._meta.fields[0].formfield(form_class=IntegerField, max_value=5)
    assert type(field) == IntegerField
    assert field.max_value == 5
