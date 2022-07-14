from datetime import date
from django_pydantic_field import fields
from django.db import models

from .conftest import InnerSchema


def test_sample_field():
    sample_field = fields.PydanticSchemaField(schema=InnerSchema)
    existing_instance = InnerSchema(stub_str="abc", stub_list=[date(2022, 7, 1)])
    expected_encoded = '{"stub_str": "abc", "stub_int": 1, "stub_list": ["2022-07-01"]}'

    assert sample_field.get_prep_value(existing_instance) == expected_encoded
    assert sample_field.to_python(expected_encoded) == existing_instance


def test_sample_field_with_raw_data():
    sample_field = fields.PydanticSchemaField(schema=InnerSchema)
    existing_raw = {"stub_str": "abc", "stub_list": [date(2022, 7, 1)]}
    expected_encoded = '{"stub_str": "abc", "stub_int": 1, "stub_list": ["2022-07-01"]}'

    assert sample_field.get_prep_value(existing_raw) == expected_encoded
    assert sample_field.to_python(expected_encoded) == InnerSchema(**existing_raw)


def test_simple_model_field():
    class SampleModel(models.Model):
        sample_field = fields.PydanticSchemaField(schema=InnerSchema)

        class Meta:
            app_label = "sample_app"


    existing_raw = {"stub_str": "abc", "stub_list": [date(2022, 7, 1)]}
    expected_decoded = InnerSchema(stub_str="abc", stub_list=[date(2022, 7, 1)])

    instance = SampleModel(sample_field=existing_raw)
    assert instance.sample_field == expected_decoded
