import unittest

from form_json.script import FormDataJson as FormData


class TestFormDataJson:
    @classmethod
    def setUp(cls):
        cls.form_instance = FormData()