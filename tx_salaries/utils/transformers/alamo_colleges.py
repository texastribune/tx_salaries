from copy import copy

from .base import DEFAULT_DATA_TEMPLATE


def transform(labels, source):
    data = []
    for raw_row in source:
        # Check to see if the row contains a status column as those are
        # always included in a valid record.  This ignores various theh
        if len(raw_row[2].strip()) is 0:
            continue

        row = dict(zip(labels, raw_row))
        d = copy(DEFAULT_DATA_TEMPLATE)
        d["original"] = raw_row
        d["tx_people.Person"] = {
            "family_name": row["Last Name"],
            "given_name": row["First Name"],
            "name": "%s %s" % (row["First Name"], row["Last Name"]),
        }

        d["tx_people.Organization"] = {
            "label": row["Department"],
        }

        d["tx_people.Post"] = {
            "label": row["Position Title"],
        }

        d["tx_people.Membership"] = {
            "start_date": row["Hire Date"],
        }

        d["tx_salaries.CompensationType"] = {
            "name": "%s Time" % "Part" if row["FT or PT Status"] == "PT" else "Full",
        }

        if row["Hourly Rate"].strip():
            compensation_key = "Hourly Rate"
        else:
            compensation_key = "FT  or PT Semester Salary"
        d["tx_salaries.Employee"] = {
            "hire_date": row["Hire Date"],
            "compensation": row[compensation_key],
        }
        data.append(d)
    return data
