Having problems?
----------------

Here's a running list of common &amp; uncommon errors to help you build transformers.

ERROR: AttributeError
`AttributeError: is_valid is unknown. Are all of its attributes available?`

WHAT IT MEANS: The `is_valid` function can't find the attributes based on the field it's checking. Check if you've set the correct field. For example, perhaps your map contains `full_name` and the `is_valid` function is checking for `last_name`.

ERROR: KeyError
```
line 59, in person
    'gender': self.gender_map[self.gender.strip()]
KeyError: u'F'
```

WHAT IT MEANS: The `person` function isn't finding the right key to map `'gender'`. Check `gender_map`, and make sure you've provided the right key information.