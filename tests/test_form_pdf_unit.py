import unittest
import random

from form_pdf.script import FormDataPdf as FormData


class TestFormDataPdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.form_names = [
            'Form W-2', 'Form 1095-C', 'Form W-8IMY', 'Form W-8EXP',
            'Form W-8ECI'
        ]

        cls.form_name = random.choice(cls.form_names)

        cls.form_data_instance = FormData(form_name=cls.form_name,
                                          start=2008,
                                          end=2011)

    def test_gen_form_url_name(self):
        url_form_name_pairs = {
            'Form W-2': 'fw2',
            'Form 1095-C': 'f1095c',
            'Form W-8IMY': 'fw8imy',
            'Form W-8EXP': 'f28exp',
            'Form W-8ECI': 'fw8eci'
        }

        url_name = self.form_data_instance._gen_form_url_name()
        self.assertEqual(url_name, url_form_name_pairs[self.form_name])

    def test_gen_download_url(self):
        url_name = self.form_data_instance._gen_form_url_name()

        url = self.form_data_instance._gen_download_url(url_name=url_name,
                                                        year=2008)

        self.assertEqual(
            url, f'https://www.irs.gov/pub/irs-prior/{url_name}--2008.pdf')
