from copy import copy

from .base import DEFAULT_DATA_TEMPLATE


def transform(labels, source):
    data = []
    for raw_row in source:
        # Brownsville likes to include the employee count as a row by
        # itself.  No need to process that.
        if raw_row[0].strip() == "EMPLOYEE COUNT:":
            continue

        row = dict(zip(labels, raw_row))
        d = copy(DEFAULT_DATA_TEMPLATE)
        d["original"] = raw_row
        d["tx_people.Person"] = {
            "family_name": row["LAST NAME"],
            "given_name": row["FIRST NAME"],
            "name": "%s %s %s" % (row["FIRST NAME"], row["MI"],
                    row["LAST NAME"]),
        }

        d["tx_people.Organization"] = {
            "label": row["CAMPUS/DEPT"],
        }

        d["tx_people.Post"] = {
            "label": row["POSITION"],
        }

        d["tx_people.Membership"] = {
            "start_date": row["HIRE_DATE"],
        }

        d["tx_salaries.CompensationType"] = {
            "name": "Full Time Teacher",
        }

        d["tx_salaries.Employee"] = {
            "hire_date": row["HIRE_DATE"],
            "compensation": row["SALARY"],
        }
        data.append(d)
    return data
