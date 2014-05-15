tx_salaries
===========
This Django application was generated using the `Texas Tribune's`__ Generic
Django app template.

.. __: http://www.texastribune.org/


Installation & Configuration
----------------------------
You can install this using `pip`_ like this:

::

    pip install tx_salaries

Once installed, you need to add it to your ``INSTALLED_APPS``.  You can do that
however you like or you can copy-and-paste this in after your
``INSTALLED_APPS`` are defined.

::

    INSTALLED_APPS += ['tx_salaries', ]

Now you're ready to start using ``tx_salaries``.


Usage
-----
``tx_salaries`` is meant to be used in conjunction with data received from
various departments around the state.  You must request this data yourself if
you want to use ``tx_salaries``.

Importing Data
""""""""""""""
Data is imported using the ``import_salary_data``.  You can run it once
``tx_salaries`` is properly installed like this::

    python manage.py import_salary_data /path/to/some-salary-spreadsheet.xlsx

Data is imported using `csvkit`_, so it can import from any spreadsheet format
that csvkit's `in2csv`_ understands.


Writing a New Transformer
"""""""""""""""""""""""""
This sections walks you through creating a new importer.  We're going to use
the fictional "Rio Grande County" (fictional in Texas at least).

Transformers require two things:

* An entry in the ``TRANSFORMERS`` map in ``tx_salaries/utils/transformers/__init__.py``
* An actual transformer capable of processing that file

Entries in the ``TRANSFORMERS`` dictionary are made up of a unique hash that
servers as the key to a given spreadsheet and a callable function that can
transform it.

To generate a key, run the following command on your spreadsheet::

    python manage generate_transformer_hash path/to/rio_grande_county.xls --sheet="sheet name"

The output should be a 40 character string.  Copy that value and open the
``tx_salaries/utils/transformers/__init__.py`` file which contains all of the
known transformers.  Find the spot where ``rio_grande_county`` would fit in the
alphabetical dictionary in ``TRANSFORMERS`` and add this line::

    '{ generated hash }': [rio_grande_county.transform, ],

If the generated hash already exists, provide a tuple with a text
label for the transformer and the transformer module like this::

    '{ generated hash }': [('Rio Grande County', rio_grande_county.transform),
                            ('Other Existing County', other_county.transform), ],

Note that the second value isn't a string -- instead it's a module.  Now you need to
import that module.  Go up to the top of the ``__init__.py`` file and add an
import::

    from . import rio_grande_county

Save that file.  Next up, you need to create the new module that you just
referenced.  Inside the ``tx_salaries/utils/transformers/`` directory, create a
new file call ``rio_grande_county.py``  At the first pass, it should look like
this::

    from . import base
    from . import mixins


    class TransformedRecord(mixins.GenericCompensationMixin,
            mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
            mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
            mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
            base.BaseTransformedRecord):
        MAP = {
            'last_name': 'LABEL FOR LAST NAME',
            'first_name': 'LABEL FOR FIRST NAME',
            'department': 'LABEL FOR DEPTARTMENT',
            'job_title': 'LABEL FOR JOB TITLE',
            'hire_date': 'LABEL FOR HIRE DATE',
            'status': 'LABEL FOR FT/PT STATUS',
            'compensation': 'LABEL FOR COMPENSATION',
        }

        NAME_FIELDS = ('first_name', 'last_name', )

        ORGANIZATION_NAME = 'Rio Grande County'

        @property
        def is_valid(self):
            # Adjust to return False on invalid fields.  For example:
            return self.last_name.strip() != ''

        @property
        def compensation_type(self):
            if self.status.upper() == 'FT':
                return 'Full Time'
            else:
                return 'Part Time'

Each of the ``LABEL FOR XXX`` fields should be adjusted to match the
appropriate column in the given spreadsheet.

``TransformedRecord`` now represents a generic record.  You may need to
customize the various properties added by the mixins or replace them with
custom properties in other cases.  See the mixins for further documentation on
what they add.

Next you need to add the actual ``transform`` function.  At the end of the
``rio_grande_county.py`` file, add this line::

    transform = base.transform_factory(TransformedRecord)

This generates a ``transform`` function that uses the ``TransformedRecord``
that you just created.  Now you're ready to run the importer.

Back on the command line, run this::

    python manage import_salary_data /path/to/rio_grande_county.xls --sheet="sheet name"

Pay attention to any error messages you receive and make the appropriate
adjustments.  Congratulations!  You just completed your first salary
transformer.


Understanding Transformers
""""""""""""""""""""""""""
.. _warning: This section is under development

Transformers are callable functions that take two arguments and return an array
of data to be processed.  At its simplest, it would look like this::

    def transform(labels, source):
        data = []
        for raw_record in source:
            record = dict(zip(labels, raw_record))
            # ... create the structure required ...
            data.append(structured_record)
        return data

The data contained in the fictitious ``structured_record`` variable is a
dictionary that must look something like this::

    structured_record = {
        'original': ...,  # dictionary of key/value pairs for the data
        'tx_people.Identifier': ...,  # dictionary of attributes for the Identifier
        'tx_people.Organization': ...,  # dictionary of attributes for the Organization
        'tx_people.Post': ...,  # dictionary of attributes for the Post
        'tx_people.Membership': ...,  # dictionary of attributes for the Membership
        'compensations': [
            # first dictionary of compensation and type
            # should contain at least one, can contain as many as necessary
        ]

    }}

Tasks
-----
* Document parallel usage once `Issue 2`_ is resolved.
* Document errors encountered when hitting an unknown parser (see `Issue 3`_).

.. _Issue 2: https://github.com/texastribune/tx_salaries/issues/2
.. _Issue 3: https://github.com/texastribune/tx_salaries/issues/3



.. _csvkit: http://csvkit.readthedocs.org/en/latest/
.. _in2csv: http://csvkit.readthedocs.org/en/latest/scripts/in2csv.html
.. _pip: http://www.pip-installer.org/en/latest/

