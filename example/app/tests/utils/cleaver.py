from django.test import TestCase
from tx_salaries.utils import cleaver


class DepartmentCleaverTest(TestCase):
    def test_roman_numerals(self):
        cleave = lambda a: unicode(cleaver.DepartmentNameCleaver(a).parse())
        self.assertEqual(cleave('Degree Plan Evaluator Iii'),
                         'Degree Plan Evaluator III')
        self.assertEqual(cleave('Coordinator Ii, Special Programs'),
                         'Coordinator II, Special Programs')
        self.assertEqual(cleave('Director Of Investments'),
                         'Director of Investments')
        self.assertEqual(cleave('Investigator Iv'), 'Investigator IV')
        self.assertEqual(cleave('Associate Vice President'),
                         'Associate Vice President')

    def test_apostrophe_s(self):
        cleave = lambda a: unicode(cleaver.DepartmentNameCleaver(a).parse())
        self.assertEqual(cleave("Basketball - Men'S "), "Basketball - Men's")
        self.assertEqual(cleave("President'S Office "), "President's Office")
