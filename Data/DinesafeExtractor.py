import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import os
from datetime import datetime
import boto3
import logging
from io import BytesIO
import io

runtime = datetime.now().strftime("%d_%m_%y_%H_%M_%S")

logfilename = "logfiles/test" + runtime + ".log"

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO,
                    filename=logfilename
                    )
logging.getLogger().addHandler(logging.StreamHandler())


class DinesafeExtractor:

    def __init__(self):
        self.tree = None

    def get_tree_local_file(self, xml_file_path, enc="utf-8"):
        parser = ET.XMLParser(encoding=enc)
        self.tree = ET.parse(xml_file_path, parser=parser)

    def get_tree_from_S3(self, client, bucket_name='dinesafe-data', filename='dinesafe_v2.xml'):
        """
        Get Tree from S3.
        Useful Links : https://stackoverflow.com/questions/33962620/elementtree-returns-element-instead-of-elementtree
        :param xmldata:
        :return:
        """
        bucket = client.Bucket(bucket_name)
        for obj in bucket.objects.all():
            key = obj.key
            print(f"key in bucket object -> {key}")
            if key == filename:
                body = obj.get()['Body']
                print(f"Body type {type(body)}")
        self.tree = ET.ElementTree(ET.fromstring(body.read().decode('utf-8')))

    def get_col_names(self):
        root = self.tree.getroot()

        for child in root:
            print(child.tag)
            # break

        col_names = []
        for attr in child:
            # print (attr.tag)
            col_names.append(attr.tag)
        return col_names

    def get_dataframe(self, col_names):
        root = self.tree.getroot()

        data_dict = self.init_data_dict(col_names)
        for child in root:
            for element in child:
                for col_name, col_list in data_dict.items():
                    if element.tag == col_name:
                        col_list.append(element.text)
        df = pd.DataFrame(data_dict)
        df = self.clean_dataframe(df)
        return df

    @staticmethod
    def init_data_dict(col_names):
        # for col_name in col_names:
        data_dict = {col_name: [] for col_name in col_names}
        return data_dict

    @staticmethod
    def clean_dataframe(df):
        df['AMOUNT_FINED'] = pd.to_numeric(df['AMOUNT_FINED'], errors='coerce')
        df['INSPECTION_DATE'] = pd.to_datetime(df['INSPECTION_DATE'], errors='coerce')
        df['INSP_Year'] = df['INSPECTION_DATE'].dt.year
        df['INSP_Month'] = df['INSPECTION_DATE'].dt.month
        return df

    @staticmethod
    def write_file_to_S3(df, s3_client, bucket_name, filename):

        with io.StringIO() as csv_buffer:
            df.to_csv(csv_buffer, index=False)

            response = s3_client.put_object(
                Bucket=bucket_name, Key=filename, Body=csv_buffer.getvalue()
            )

            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            if status == 200:
                print(f"S3 Put Status. Status - {status}")
            else:
                print(f"Status - {status}")


if __name__ == '__main__':
    DSE = DinesafeExtractor()

    res_S3 = boto3.resource('s3',
                            aws_access_key_id=os.environ['ACCESS_ID_KEY'],
                            aws_secret_access_key=os.environ['YOUR_SECRET_ACCESS_KEY'])

    DSE.get_tree_from_S3(res_S3, 'dinesafe-data', 'dinesafe_v2.xml')

    logging.info(f"DSE.tree type -> {type(DSE.tree)}")

    col_names = DSE.get_col_names()
    logging.info(col_names)
    df = DSE.get_dataframe(col_names)
    logging.info(df.shape)
    logging.info(df.head)

    client_S3 = boto3.client('s3',
                            aws_access_key_id=os.environ['ACCESS_ID_KEY'],
                            aws_secret_access_key=os.environ['YOUR_SECRET_ACCESS_KEY'])
    DSE.write_file_to_S3(df, client_S3, 'dinesafe-data', 'dinesafe_xml_extracted.csv')