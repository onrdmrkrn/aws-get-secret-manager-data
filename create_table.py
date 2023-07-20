import pymysql
import boto3
import os
from requests_aws4auth import AWS4Auth
import rds_config

credentials = boto3.Session().get_credentials()
headers = {'Content-Type': "application/json"}
es_url = os.getenv("ES_URL")
region = os.getenv("REGION")
aws_auth = AWS4Auth(credentials.access_key, credentials.secret_key, "eu-west-1", 'es',
                    session_token=credentials.token)


def conopen(rasyonadb):
    db_username, db_password, db_name, db_host, db_port = rds_config.rdsdbconnect(rasyonadb)
    rds_host = db_host
    name = db_username
    password = db_password
    db_name = db_name
    port = int(db_port)
    mysqlconn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, port=port, connect_timeout=5)
    cursor = mysqlconn.cursor()
    return mysqlconn, cursor


def createschema(name, mysqlconn, cursor):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name};")

    mysqlconn.commit()
    cursor.execute(f"USE {name};")
    cursor.execute(f"""create table if not exists {name}(
                            log_time      datetime    not null,
                            objid         varchar(45) null,
                            groupname     varchar(45) null,
                            device        varchar(45) not null,
                            name_raw      varchar(45) null,
                            lastvalue     int         not null,
                            status_raw    varchar(45) not null,
                            type          varchar(45) null,
                            lastvalue_raw varchar(45) null,
                            tags          varchar(45) null,
                            primary key (device, lastvalue, status_raw, log_time)); """)
    mysqlconn.commit()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}.retantion(
                        `data_table` varchar(50) NOT NULL,
                        `stored_day` int DEFAULT NULL,
                        `ret_field` varchar(45) DEFAULT NULL,
                        PRIMARY KEY (`data_table`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")
    mysqlconn.commit()


def closeconn(conn, cursor):
    cursor.close()
    conn.close()
