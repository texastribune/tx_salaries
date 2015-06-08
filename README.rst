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
Data is imported using the ``import_salary_data`` management command.  You can run it once
``tx_salaries`` is properly installed like this::

    python manage.py import_salary_data /path/to/some-salary-spreadsheet.xlsx

Data is imported using `csvkit`_, so it can import from any spreadsheet format
that csvkit's `in2csv`_ understands.


Start the salaries.texastribune.org server
""""""""""""""""""""""""""""""""""""""""""

In the terminal, go to [salaries.texastribune.org](https://github.com/texastribune/salaries.texastribune.org) repo. While the transformers live in tx_salaries, all of the data management happens in the salaries.texastribune repo, and that's where you'll run all of the commands in these instructions:

1. `workon salaries-dev`
2. `boot2docker down`
3. `boot2docker up`
4. `source .env`
5. `make docker/db` or `make docker/refresh-db`
6. `python salaries/manage.py runserver`

Check localhost:8000, should be up and running.


Writing a New Transformer
"""""""""""""""""""""""""
This section walks you through creating a new importer.  We're going to use
the fictional "Rio Grande County" (fictional in Texas at least).

Transformers require two things:

* An entry in the ``TRANSFORMERS`` map in ``tx_salaries/utils/transformers/__init__.py``
* An actual transformer capable of processing that file

Entries in the ``TRANSFORMERS`` dictionary are made up of a unique hash that
serves as the key to a given spreadsheet and a callable function that can
transform it.

To generate a key, run the following command in the [salaries.texastribune.org](https://github.com/texastribune/salaries.texastribune.org) virtualenv:

    python salaries/manage.py generate_transformer_hash path/to/rio_grande_county.xls --sheet=data_sheet --row=number_of_header_row

The output should be a 40-character string.  Copy that value and open the
``tx_salaries/utils/transformers/__init__.py`` file which contains all of the
known transformers.  Find the spot where ``rio_grande_county`` would fit in the
alphabetical dictionary in ``TRANSFORMERS`` and add this line::

    '{ generated hash }': [rio_grande_county.transform, ],

If the generated hash already exists with another transformer, provide a tuple with a text
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

    from datetime import date

    # add if necessary: --sheet="Request data" --row=3


    class TransformedRecord(mixins.GenericCompensationMixin,
            mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
            mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
            mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
            mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

        MAP = {
            'last_name': 'LABEL FOR LAST NAME',
            'first_name': 'LABEL FOR FIRST NAME',
            'department': 'LABEL FOR DEPARTMENT',
            'job_title': 'LABEL FOR JOB TITLE',
            'hire_date': 'LABEL FOR HIRE DATE',
            'status': 'LABEL FOR FT/PT STATUS',
            'compensation': 'LABEL FOR COMPENSATION',
            'gender': 'LABEL FOR GENDER',
            'race': 'LABEL FOR RACE',
        }

        NAME_FIELDS = ('first_name', 'last_name', )

        ORGANIZATION_NAME = 'Rio Grande County'

        ORGANIZATION_CLASSIFICATION = 'County'

        DATE_PROVIDED = date(2013, 10, 31)
        # Y/M/D agency provided the data

        URL = "http://raw.texastribune.org.s3.amazonaws.com/path/to/rio_grande_county.xls"

        @property
        def is_valid(self):
            # Adjust to return False on invalid fields.  For example:
            return self.last_name.strip() != ''

        @property
        def compensation_type(self):
            if self.status.upper() == 'FT':
                return 'FT'
            else:
                return 'PT'

        @property
        def description(self):
            if self.status.upper() == 'FT':
                return 'Full-time salary'
            else:
                return 'Part-time salary'

    transform = base.transform_factory(TransformedRecord)

Each of the ``LABEL FOR XXX`` fields should be adjusted to match the
appropriate column in the given spreadsheet. If the file requires special
sheet or row handling, note the ``--sheet`` and ``--row`` flags as a comment
at the top of the file.

``TransformedRecord`` now represents a generic record.  You may need to
customize the various properties added by the mixins or replace them with
custom properties in other cases.  See the mixins for further documentation on
what they add.

The last line generates a ``transform`` function that uses the ``TransformedRecord``
that you just created.  Now you're ready to run the importer.

Back on the command line, run this::

    python salaries/manage.py import_salary_data /path/to/rio_grande_county.xls

Pay attention to any error messages you receive. Most transformer errors are due
to missing data -- either the user didn't map to all the necessary fields,
didn't include a mixin to process a field or made an error in an overridden
property that is supposed to return an attribute.

Note the ``generate_transformer_hash`` and ``import_salary`` data
management commands can take ``--sheet`` and ``--row`` flags if the agency gave
you a spreadsheet with multiple sheets or a header row that isn't the first row.

Congratulations!  You just completed your first salary transformer.


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

That record is structured such that its keys and values match the models and kwargs
for storing tx_people and tx_salaries models. How do spreadsheets get structured?

The `import_salary_data`_ management command runs through several modules to store
spreadsheet data. First it uses transformer.`transform`_, which uses the header
row to identify the transformer necessary to import the spreadsheet.

That transformer turns each row of the spreadsheet into a structured record with
the help of `mixins`_.py and `base`_.py. ``base.py`` defines the template of the
record, and ``mixins.py`` provides functions to format the required data. Mixins
are included in the definition of ``TransformedRecord``. However, mixins cannot
handle all situations, and sometimes fields like ``CompensationType`` require
special logic. You can override mixins by writing a custom `@property` in the
transformer. Errors often happen at this stage when a transformer and its mixins
fail to provide all the fields required by base.

After each of the rows of the spreadsheet are converted to structured records,
a list of records is sent to `to_db`_.save(), which unpacks and stores the data.
``import_salary_data`` also keeps track of the unique organizations and positions
that are imported so it can denormalize the stats when the import finishes.

That's a high-level view of transformers. Read the comments in ``mixins.py`` and
check out the data template in ``base.py`` for more details on the specific attributes
transformers require.

Tasks
-----
* Document parallel usage once `Issue 2`_ is resolved.
* Document errors encountered when hitting an unknown parser (see `Issue 3`_).

.. _Issue 2: https://github.com/texastribune/tx_salaries/issues/2
.. _Issue 3: https://github.com/texastribune/tx_salaries/issues/3



.. _csvkit: http://csvkit.readthedocs.org/en/latest/
.. _in2csv: http://csvkit.readthedocs.org/en/latest/scripts/in2csv.html
.. _pip: http://www.pip-installer.org/en/latest/

.. _import_salary_data: tx_salaries/management/commands/import_salary_data.py
.. _transform: tx_salaries/utils/transformer.py
.. _transform: tx_salaries/utils/transformer.py
.. _mixins: tx_salaries/utils/transformers/mixins.py
.. _base: tx_salaries/utils/transformers/base.py
.. _to_db: tx_salaries/utils/to_db.py
