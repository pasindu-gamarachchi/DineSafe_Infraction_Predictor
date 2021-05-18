import numpy as np
import json
import os
import pandas as pd
from pandas.io.json import json_normalize
from  datetime import datetime
import logging
import io
import boto3

runtime = datetime.now().strftime("%d_%m_%y_%H_%M_%S")

logfilename = "logfiles/test_yelp_extraction_" + runtime + ".log"

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO,
                    filename=logfilename
                    )
logging.getLogger().addHandler(logging.StreamHandler())


class YelpDataExtractor:

    def __init__(self):
        self.json_data = None

    def get_json_from_S3(self, S3_resource, bucket, key):
        obj = S3_resource.Object(bucket, key)
        data = obj.get()['Body'].read().decode('utf-8')
        # self.json_data = json.loads(data)
        # logging.info(f"{type(self.json_data)}")
        lines = data.splitlines()
        dat = []
        for line in lines:
            dat.append(json.loads(line))
        self.json_data = dat
        logging.info(f"{type(self.json_data)}, len -> {len(self.json_data)}")


    def write_data_to_S3(self, s3_client, bucket_name, filename):
        df = pd.json_normalize(self.json_data)

        with io.StringIO() as csv_buffer:
            df.to_csv(csv_buffer, index=False, sep= ',')

            response = s3_client.put_object(
                Bucket=bucket_name, Key=filename, Body=csv_buffer.getvalue()
            )

            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            if status == 200:
                print(f"S3 Put Status. Status - {status}")
            else:
                print(f"Status - {status}")


if __name__ == '__main__':

    YDE = YelpDataExtractor()
    res_S3 = boto3.resource('s3',
                            aws_access_key_id=os.environ['ACCESS_ID_KEY'],
                            aws_secret_access_key=os.environ['YOUR_SECRET_ACCESS_KEY'])
    YDE.get_json_from_S3(res_S3, bucket='dinesafe-data', key='ON_bus_v2.json' )
    # df = json_normalize(data )
    # df =df.set_index('business_id')
    # df.to_csv('Yelp_Businesses.csv',sep= ',')

    client_S3 = boto3.client('s3',
                             aws_access_key_id=os.environ['ACCESS_ID_KEY'],
                             aws_secret_access_key=os.environ['YOUR_SECRET_ACCESS_KEY'])
    YDE.write_data_to_S3(client_S3, 'dinesafe-data', 'yelp_data.csv')