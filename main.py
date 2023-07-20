import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import create_table
def lambda_handler(event, context):
    switch = event['switch']
    conn, cursor = create_table.conopen(event['rasyonadb'])
    db = event['database']
    if switch == 0:
        create_table.createschema(event['database'].split("-")[0], conn, cursor)
