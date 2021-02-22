import unittest
import random

import pandas as pd

from form_json.script import FormDataJson as FormData


class TestFormDataJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.form_names = [
            'Form W-2', 'Form 1095-C', 'Form W-8IMY', 'Form W-8EXP',
            'Form W-8ECI'
        ]
        cls.form_data_instance = FormData(cls.form_names)

    def test_generate_urls(self):
        form_name = random.choice(self.form_names)
        urls = self.form_data_instance.generate_urls(form_name)

        self.assertIsInstance(urls, dict)

        self.assertIn('asc', urls)
        self.assertIn('desc', urls)

        self.assertIn('isDescending=true', urls['desc'])
        self.assertIn('isDescending=false', urls['asc'])

    def test_get_extrema(self):
        data = [['Form W-2', 'Wage and Tax Statement (Info Copy Only)', 1988],
                ['Form W-2', 'Wage and Tax Statement (Info Copy Only)', 2002],
                ['Form W-2', 'Wage and Tax Statement (Info Copy Only)', 2011],
                ['Form W-2', 'Wage and Tax Statement (Info Copy Only)', 1999]]

        df = pd.DataFrame(data,
                          columns=['Product Number', 'Title', 'Revision Date'])

        # When form name is not in dataframe
        result = self.form_data_instance._get_extrema(df=df,
                                                      form_name='Form 1098-C')

        self.assertIsInstance(result, dict)
        self.assertFalse(result, {})

        # Get maximum year
        result = self.form_data_instance._get_extrema(df=df,
                                                      form_name='Form W-2')

        self.assertIsInstance(result, dict)
        self.assertEqual(
            result.get(
                ('Form W-2', 'Wage and Tax Statement (Info Copy Only)')), 2011)

        # Get minimum year
        result = self.form_data_instance._get_extrema(df=df,
                                                      form_name='Form W-2',
                                                      max_=False)

        self.assertIsInstance(result, dict)
        self.assertEqual(
            result.get(
                ('Form W-2', 'Wage and Tax Statement (Info Copy Only)')), 1988)
