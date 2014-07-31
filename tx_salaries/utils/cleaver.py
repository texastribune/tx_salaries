import re

from name_cleaver import cleaver, names

regex_i = lambda a: re.compile(a, re.IGNORECASE)


class DepartmentName(names.OrganizationName):
    def upper_repl(match):
        return match.group(0).upper()

    MAP = (
        (regex_i(r' OF '), ' of '),
        (regex_i(r' AT '), ' at '),
        (regex_i(r' THE '), ' the '),
        (regex_i(r' TO '), ' to '),
        (regex_i(r' FOR '), ' for '),
        (regex_i(r"'S"), "'s"),
        (regex_i(r' & '), ' and '),
        (regex_i(r' AND '), ' and '),
        (regex_i(r'\b([IXV]{1,3})\b'), upper_repl), # roman numerals
    )

    def case_name_parts(self):
        super(DepartmentName, self).case_name_parts()
        self.expand_abbreviations()
        return self

    def expand_abbreviations(self):
        for pattern, replacement in self.MAP:
            self.name = re.sub(pattern, replacement, self.name)


class DepartmentNameCleaver(cleaver.OrganizationNameCleaver):
    """
    Custom ``OrganizationNameCleaver`` for entity and job titles

    """
    object_class = DepartmentName

    def __init__(self, name, object_class=None):
        super(DepartmentNameCleaver, self).__init__(name)
        if object_class is not None:
            self.object_class = object_class


class EmployeeName(names.PersonName):
    middle = ''


class EmployeeNameCleaver(cleaver.IndividualNameCleaver):
    """
    Custom ``IndividualNameCleaver`` for dealing with employees

    """
    object_class = EmployeeName
