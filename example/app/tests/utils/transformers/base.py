import random

from django.test import TestCase

from tx_salaries.utils.transformers import base


class TestOfBaseTransformedRow(TestCase):
    def test_returns_mapped_value_as_an_attribute(self):
        some_random_key = 'some-key-{0}'.format(random.randint)

        class MyRow(base.BaseTransformedRow):
            MAP = {
                'compensation': some_random_key
            }

        instance = MyRow()
        self.assertEqual(instance.compensation_key, some_random_key)

    def test_returns_actual_data_if_mapped(self):
        some_random_key = 'some-key-{0}'.format(random.randint)
        some_random_value = random.randint(100000, 2000000)
        data = {some_random_key: some_random_value}

        class MyRow(base.BaseTransformedRow):
            MAP = {
                'compensation': some_random_key
            }

        instance = MyRow(data)
        self.assertEqual(instance.compensation, some_random_value)
