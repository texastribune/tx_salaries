from copy import copy

from .base import DEFAULT_DATA_TEMPLATE


def transform(labels, source):
    data = []
    for raw_row in source:
        row = dict(zip(labels, raw_row))
        d = copy(DEFAULT_DATA_TEMPLATE)

        job_title = row["JOB TITLE"].strip()
        compensation_type = "Full Time"
        if job_title[-2:].upper() == "PT":
            compensation_type = "Part Time"
            job_title = job_title[:-2].strip()

        # Clean up any issues with the "- PT" suffix, but do it by
        # splitting on "-" to ensure that we catch as many as possible
        split_department = row['DEPARTMENT'].split('-')[:-1]
        department = '-'.join([a.strip() for a in split_department])

        d["original"] = raw_row
        d["tx_people.Person"] = {
            "family_name": row["LAST NAME"],
            "given_name": row["FIRST NAME"],
            "name": "%s %s" % (row["FIRST NAME"], row["LAST NAME"]),
            "gender": row["SEX"],
        }
        d["tx_people.Organization"] = {
            "label": "Collin College",
            "children": [{
                "label": department,
            }],
        }

        d["tx_people.Post"] = {
            "label": job_title,
        }

        d["tx_people.Membership"] = {
            "start_date": row["CURRENT HIRE DATE"],
        }

        compensation = row["ANNUAL SALARY (HOURLY RATE FOR PT)"]
        compensation
        if compensation == 'See "Explanations" tab':
            if row["JOB TITLE"] == "Assoc Professor":
                compensation = "719"
                compensation_type = "Part Time Associate Professor"
            else:
                compensation = None
        d["tx_salaries.CompensationType"] = {
            "name": compensation_type
        }

        d["tx_salaries.Employee"] = {
            "hire_date": row["CURRENT HIRE DATE"],
            "compensation": compensation,
        }
        data.append(d)
    return data
