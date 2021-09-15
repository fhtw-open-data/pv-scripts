import urllib
import urllib.request
import json
import pprint
from ckanapi import RemoteCKAN
import datetime

host = "http://10.64.54.1"
key = "INSERT_KEY_HERE"
ua = 'ckanapi/1.0'

ckan = RemoteCKAN(host, apikey=key, user_agent=ua)

day_limit = 0


def import_data():
    # request to influx api
    # no limitation to get all available data
    request = urllib.request.Request('http://pvvisu-n1.cs.technikum-wien.at:8086/query?u=apiuser&p=UZaXh4YPx7_x2cQxAxppNgYbA8&db=pvlog&q=select%20*%20from%20pvlog01%20order%20by%20time%20desc%20limit%20'+str(day_limit*17280))
    response = urllib.request.urlopen(request)

    # parse response data
    response_dict = json.loads(response.read())["results"][0]
    data = response_dict["series"][0]["values"]
    pprint.pprint("Data received. "+str(len(data))+" entries")

    # --- fields of response data + array index of relevant fields ---
    #     "time"        ---> [0]
    #     "freq"        ---> [1]
    #     "fscale"
    #     "nans"
    #     "power"       ---> [4]
    #     "pscale"
    #     "u1"          ---> [6]
    #     "u2"
    #     "u3"
    #     "vscale"

    now = datetime.datetime.now()

    years = []

    for pv in data:
        if pv[0][0:4] not in years:
            years.append(pv[0][0:4])

    for year in years:

        res = {
            "package_id": "pv-data-full",
            "name": "PV Data "+str(year),
            "description": "This resource was generated automatically ("+str(now)+")."
        }

        try:
            ckan.action.datastore_create(
                resource=res,
                aliases=["pv-" + str(year) + "-full"],
                primary_key=["time"],
                fields=[
                    {"type": "timestamp", "id": "time"},
                    {"type": "int", "id": "power"},
                    {"type": "float", "id": "freq"},
                    {"type": "float", "id": "u1"},
                    {"type": "float", "id": "nans"}
                ]
            )
        except:
            pass

        resource_id = ckan.action.datastore_search(
            resource_id="pv-" + str(year) + "-full"
        )["resource_id"]

        for month in range(12, 0, -1):

            records = []
            minutes = []

            # remove 'not in minutes' clause to receive complete data (12 entries per minute) instead of 1 per minute
            # caution: removed limitation can lead to server time out error
            for pv in data:
                if pv[0][0:4] == year and pv[0][5:7] == "{:02d}".format(month) and pv[0][0:16] not in minutes:
                    records.append({"time": pv[0], "power": pv[4], "freq": pv[1], "u1": pv[6], "nans": pv[3]})
                    minutes.append(pv[0][0:16])
                    pprint.pprint(pv[0][0:16])

            # with open('data.json', 'w') as fp:
            #     json.dump(records, fp)

            res = {"package_id": "pv-data", "name": "PV Data 24h", "description": "PV Data 24h"}

            try:
                with ckan as session:
                    session.action.datastore_upsert(
                        resource_id=resource_id,
                        records=records,
                        method="upsert"
                    )
                pprint.pprint("pv-"+str(year)+"-"+str(month)+" updated in DataStore")
            except Exception as e:
                pprint.pprint("pv-"+str(year)+"-"+str(month)+" update failed (DataStore)")
                pprint.pprint(e)

    # upload json file additionally

    # ckan.action.resource_create(
    #     package_id="pv-data",
    #     url="pv-data",
    #     name="PV Dummy 24h (JSON)",
    #     description="Dummy Import PV Data",
    #     mimetype="application/json",
    #     format="JSON",
    #     upload=open('data.json', 'rb'))


import_data()
