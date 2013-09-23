import hashlib

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from mock import patch

from tx_salaries.utils import transformers


sha1 = lambda a: hashlib.sha1(a).hexdigest()


class TestOf_generate_key(TestCase):
    def test_returns_hash_based_on_labels(self):
        labels = ("one", "two", "three")
        expected = sha1("::".join(labels))
        self.assertEqual(expected, transformers.generate_key(labels))

    def test_different_labels_produce_different_keys(self):
        first = transformers.generate_key(["one", "two", "three"])
        second = transformers.generate_key(["uno", "dos", "tres"])
        self.assertNotEqual(first, second)


class TestOf_get_transformers(TestCase):
    def test_raises_exception_when_unable_to_find_transformer(self):
        labels = ['unknown', 'and', 'unknowable', 'gibberish', ]
        with self.assertRaises(ImproperlyConfigured):
            transformers.get_transformers(labels)

    def test_returns_a_list_of_transformers_that_match(self):
        labels = ["one", "two", "three"]
        key = transformers.generate_key(labels)
        with patch.dict(transformers.TRANSFORMERS, {key: [self, ]}):
            result = transformers.get_transformers(labels)
            self.assert_(len(result) is 1)
            self.assert_(self in result)
