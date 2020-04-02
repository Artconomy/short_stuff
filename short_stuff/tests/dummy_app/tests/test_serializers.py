import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, ModelSerializer

from short_stuff.django.serializers import ShortCodeField
from short_stuff.tests.dummy_app.models import ShortStuffModel
from uuid import UUID


class ShortCodeSerializer(Serializer):
    test_field = ShortCodeField()


class ShortCodeNullableSerializer(Serializer):
    test_field = ShortCodeField(allow_null=True)


class ShortStuffModelSerializer(ModelSerializer):
    id = ShortCodeField()
    test_token = ShortCodeField(allow_null=True)

    class Meta:
        fields = ('id', 'test_token')
        model = ShortStuffModel


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
    assert serializer.errors['test_field'] == [
        '"nsdfv87b34wyebfvzxucyvaso8regfamwer9tvq3w74" is not a valid short code.'
    ]


def test_null_not_allowed():
    serializer = ShortCodeSerializer(data={'test_field': None})
    assert serializer.is_valid() is False
    assert serializer.errors['test_field'] == [
        'This field may not be null.'
    ]


def test_null_allowed():
    serializer = ShortCodeNullableSerializer(data={'test_field': None})
    assert serializer.is_valid() is True
    assert serializer.validated_data['test_field'] is None


@pytest.mark.django_db
def test_load_from_model():
    new = ShortStuffModel()
    new.save()
    instance = ShortStuffModelSerializer(instance=new)
    assert instance.data['test_token'] is None
    assert instance.data['id'] == new.id


def test_null_to_internal_value():
    # Can't figure out how to make this happen through normal APIs, but it seems required.
    serializer = ShortCodeSerializer()
    assert serializer.fields['test_field'].to_internal_value(None) is None


def test_null_to_representation():
    # Ditto.
    serializer = ShortCodeSerializer()
    assert serializer.fields['test_field'].to_representation(None) is None


def test_bogus_value():
    serializer = ShortCodeSerializer()
    with pytest.raises(ValidationError):
        serializer.fields['test_field'].to_internal_value(1)


def test_uuid_representation():
    # Once again, not sure how this is supposed to happen normally, but it is required.
    serializer = ShortCodeSerializer()
    output = serializer.fields['test_field'].to_representation(UUID('90b39068-b85e-4ecd-8000-000000000000'))
    assert output == 'kLOQaLheTs2A'
