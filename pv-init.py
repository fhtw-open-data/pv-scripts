#!/usr/bin/env python
import pprint
from ckanapi import RemoteCKAN

host = "http://10.64.54.1"
key = "INSERT_KEY_HERE"

answer = input(
    "This is a script to initialize the CKAN structure for the PV Module. Continue? (y/n) ")
if answer.lower() != "y" and answer.lower() != "yes":
    exit()
else:
    ua = 'ckanapi/1.0'
    ckan = RemoteCKAN(host, apikey=key, user_agent=ua)

    # ------------------------------ #
    # ------ FHTW Organization ----- #

    try:
        ckan.action.organization_create(
            name="fhtw",
            title="FHTW",
            description="FH Technikum Wien",
            image_url="https://cis.technikum-wien.at/cms/dms.php?id=168756")

        pprint.pprint("Organization 'FHTW' successfully created.")

    except Exception as e:
        pprint.pprint("Creation of organization 'FHTW' wasn't successful. Check if it's already existing.")
        pprint.pprint(e)

    # ------------------------------ #
    # ------ FHTW PV Group ----- #

    try:
        ckan.action.group_create(
            name="fhtw-pv",
            title="FHTW PV",
            description="PV Data Group",
            image_url="https://cdn.pixabay.com/photo/2017/03/13/07/34/photovoltaic-2138992_960_720.jpg")

        pprint.pprint("Group 'FHTW PV' successfully created.")

    except Exception as e:
        pprint.pprint("Creation of group 'FHTW PV' wasn't successful. Check if it's already existing.")
        pprint.pprint(e)

    # ------------------------------ #
    # ------ PV Data Package ------- #

    try:
        ckan.action.package_create(
            name="pv-data",
            title="PV Data",
            notes="PV Data",
            private="False",
            owner_org="fhtw",
            groups=[{"name": "fhtw-pv"}],
            license_id="cc-by")

        pprint.pprint("Package 'PV Data' successfully created.")

    except Exception as e:
        pprint.pprint("Creation of package 'PV Data' wasn't successful. Check if it's already existing.")
        pprint.pprint(e)
