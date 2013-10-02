from copy import copy

from .import base


def transform(labels, source):
    data = []
    for raw_row in source:
        if len(raw_row[0].strip()) is 0:
            continue

        row = dict(zip(labels, raw_row))
        d = copy(base.DEFAULT_DATA_TEMPLATE)
        d["original"] = row
        d["tx_people.Person"] = {
            "family_name": row["LAST NAME"],
            "given_name": row['FIRST NAME'],
            "name": "%s %s %s" % (row["FIRST NAME"], row['MIDDLE'],
                    row["LAST NAME"]),
        }

        d["tx_people.Organization"] = {
            "label": row["DEPARTMENT"],
        }

        d["tx_people.Post"] = {
            "label": row["JOB TITLE"],
        }

        d["tx_people.Membership"] = {
            "start_date": row["HIRE DATE"],
        }

        d["tx_salaries.CompensationType"] = {
            "name": "{0} Time".format("Part" if row["PART FULL"].strip() == "P"
                    else "Full"),
        }

        if row["ANNUAL RATE"].strip() == "0":
            compensation_key = "PAY RATE"
        else:
            compensation_key = "ANNUAL RATE"
        d["tx_salaries.Employee"] = {
            "hire_date": row["HIRE DATE"],
            "compensation": row[compensation_key],
        }
        data.append(d)
    return data


