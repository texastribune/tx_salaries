from . import base
from . import mixins

import string

from datetime import date

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericIdentifierMixin,
    mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Date of Hire',
        'gender': 'Gender',
        'given_race': 'Race',
        'status': 'Full or Part-Time',
        'compensation': 'Salary',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    #  so double check it!
    ORGANIZATION_NAME = 'Texas Tech University Health Sciences Center'

    # What type of organization is this? This MUST match what we use on the
    # site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2018, 01, 22)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'texas_tech_health_science/salaries/2018-01/TTUHSC_EMPLOYEE_ROSTER_1.22.2018.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M'}


    # This is how the loader checks for valid people. Defaults to checking to
    # see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()],
        }

        return r

    # def get_raw_name(self):
    #     split_name = self.full_name.split(', ')
    #     last_name = split_name[0]
    #     split_firstname = split_name[1].split(' ')
    #     first_name = split_firstname[0]
    #     if len(split_firstname) == 2 and len(split_firstname[1]) == 1:
    #         middle_name = split_firstname[1]
    #     else:
    #         first_name = split_name[1]
    #         middle_name = ''

    #     return u' '.join([first_name, middle_name, last_name])

    @property
    def compensation(self):
        salary = self.get_mapped_value('compensation')

        return salary

    @property
    def compensation_type(self):
        status = self.status

        if status == 'F':
            return 'FT'

        if status == 'P':
            return 'PT'

    @property
    def description(self):
        status = self.status

        if status == 'F':
            return "Salary"

        if status == 'P':
            return "Part-time salary"

    @property
    def race(self):
        listed_race = self.get_mapped_value('given_race').strip()

        if listed_race:
            return { 'name': listed_race }
        else:
            return { 'name': 'Unknown' }

    @property
    def organization(self):
        return {
            'name': self.ORGANIZATION_NAME,
            'classification': self.ORGANIZATION_CLASSIFICATION,
            'children': self.department_as_child,
        }

    @property
    def department_as_child(self):
        fullDept = self.department

        #department specifications
        if 'SON' in fullDept:
            fullDept = fullDept.replace('SON', 'School of Nursing')
        if 'SOM' in fullDept:
            fullDept = fullDept.replace('SOM', 'School of Medicine')
        if 'SOP' in fullDept:
            fullDept = fullDept.replace('SOP', 'School of Pharmacy')
        if 'GGH' in fullDept:
            fullDept = fullDept.replace('GGH', 'Gayle Greve Hunt ')
        if 'MPIP' in fullDept:
            fullDept = fullDept.replace('MPIP', 'Medical Practice Income Plan')
        if 'GME' in fullDept:
            fullDept = fullDept.replace('GME', 'Graduate Medical Education')
        if 'LARC' in fullDept:
            fullDept = fullDept.replace('LARC', 'Laboratory Animal Resource Center')
        if 'RMF' in fullDept:
            fullDept = fullDept.replace('RMF', 'John Montford Unit')
        if 'CBB' in fullDept:
            fullDept = fullDept.replace('CBB', 'Cell Biology and Biochemistry')
        if 'ATACS' in fullDept:
            fullDept = fullDept.replace('ATACS', 'Advanced Teaching and Assessment Clinical Simulation')
        if 'SSRFA' in fullDept:
            fullDept = fullDept.replace('SSRFA', 'Student Services and Financial Aid')
        if 'ITSC PC' in fullDept:
            fullDept = fullDept.replace('ITSC PC', 'Information Technology Services Personal Computer')
        if 'TTP' in fullDept:
            fullDept = fullDept.replace('TTP', 'Texas Tech Physicians')
        if 'CME' in fullDept:
            fullDept = fullDept.replace('CME', 'Continuing Medical Education')
        if 'SIM' in fullDept:
            fullDept = fullDept.replace('SIM', 'Simulation Center')
        if 'OIRE' in fullDept:
            fullDept = fullDept.replace('OIRE', 'Office of Institutional Research')
        if fullDept.endswith(' Genl'):
            fullDept = fullDept.replace('Genl', 'General')
        if 'Med ' in fullDept:
            fullDept = fullDept.replace('Med', 'Medicine')

        #location specifications
        if ' Ama ' in fullDept or fullDept.endswith(' Ama'):
            fullDept = fullDept.replace(' Ama', ' Amarillo')
        if ' Lbk ' in fullDept or fullDept.endswith(' Lbk'):
            fullDept = fullDept.replace(' Lbk', ' Lubbock')
        if ' Elp ' in fullDept or fullDept.endswith(' Elp'):
            fullDept = fullDept.replace(' Elp', ' El Paso')
        if ' Ode ' in fullDept or fullDept.endswith(' Ode'):
            fullDept = fullDept.replace(' Ode', ' Odessa')
        if ' Abi ' in fullDept or fullDept.endswith(' Abi'):
            fullDept = fullDept.replace(' Abi', ' Abilene')
        if ' Dal ' in fullDept or fullDept.endswith(' Dal'):
            fullDept = fullDept.replace(' Dal', ' Dallas')

        return [{'name': unicode(fullDept), }, ]

transform = base.transform_factory(TransformedRecord)
