# config file containing credentials for RDS MySQL instance
from requests_aws4auth import AWS4Auth
import json
import boto3


def rdsdbconnect(rasyonadb):
    secret_name = rasyonadb
    region_name = "eu-west-1"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    parametersdb = json.loads(secret)

    db_username = parametersdb["db_username"]
    db_password = parametersdb["db_password"]
    db_name = parametersdb["db_name"]
    db_host = parametersdb["db_host"]
    db_port = parametersdb["db_port"]
    return db_username, db_password, db_name, db_host, db_port


def prtg_connect(rasyonadb):
    secret_name = rasyonadb
    region_name = "eu-west-1"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    parametersdb = json.loads(secret)

    prtg_ip = parametersdb["ip"]
    prtg_username = parametersdb["username"]
    prtg_passhash = parametersdb["passhash"]
    prtg_port = parametersdb["port"]
    prtg_count = parametersdb["count"]
    prtg_id = parametersdb["id"]
    return prtg_ip, prtg_username, prtg_passhash, prtg_port, prtg_count, prtg_id

