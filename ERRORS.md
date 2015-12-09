Having problems?
----------------

Here's a running list of common and uncommon errors to help you build transformers.


ERROR: AttributeError
`AttributeError: is_valid is unknown. Are all of its attributes available?`

WHAT IT MEANS: The `is_valid` function can't find the attributes based on the field it's checking. Check if you've set the correct field. For example, perhaps your map contains `full_name` and the `is_valid` function is checking for `last_name`.


ERROR: KeyError
```
line 59, in person
    'gender': self.gender_map[self.gender.strip()]
KeyError: u'F'
```

```
in race
    'name': self.race_map[self.nationality.strip()]
KeyError: u''
```

WHAT IT MEANS: Your function doesn't understand the map you've provided. In the first error example, the `person` function isn't finding the right key to map `'gender'` &mdash; i.e. it can't interpret 'F'. Check `gender_map`, and make sure you've provided the right key information.

In the second example, the user provided a `race_map` that was incomplete &mdash; it did not account for blank or '' entries. The solution was to add another entry to `race_map` for blank entries:

```
race_map = {
        'AMIND': 'American Indian',
        'WHITE': 'White',
        'HISPA': 'Hispanic',
        'ASIAN': 'Asian',
        '2+RACE': 'Mixed Race',
        'PACIF': 'Pacific Islander',
        'BLACK': 'Black',
        '': 'Not given',
    }
```

ERROR: SyntaxError: Non-ASCII character
```
SyntaxError: Non-ASCII character '\xc3' in file /.../transformer.py on line 24, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
```

WHAT IT MEANS: You have a weird typo. Maybe something like `â€“` ? Delete that.


ERROR: ValueError: An employee was hired after the data was provided.
Is DATE_PROVIDED correct?

WHAT IT MEANS: Someone in your data has a hire date AFTER the date you obtained the data. First, check with the entity that this information is correct. If it is, and that person just hasn't started working yet, you'll need to include a function to ignore them.

Add this function:
```    
    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('-'))
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            tenure = 0
        return tenure
```