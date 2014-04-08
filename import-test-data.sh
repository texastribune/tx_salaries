#! /bin/bash

curl http://raw.texastribune.org.s3.amazonaws.com/state_of_texas/salaries/2014-04/TEXAS%20TRIBUNE%20JANUARY%202014_State%20Agencies%20only.xlsx -o sos.xlsx
in2csv sos.xlsx > sos.csv
csvgrep -c 5 -m "ATTORNEY" sos.csv | sed "1002,1923d" > attorneys.csv
python example/manage.py import_salary_data attorneys.csv
rm sos*
