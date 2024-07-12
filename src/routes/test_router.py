import pika
import os
import json
import boto3
import botocore
import pydicom

from typing import List, Optional
from pydantic import BaseModel
from config.base import base_config

from fastapi import APIRouter
from config import rabbit_connection
from db import db_manager


test_router = APIRouter(prefix='/test', tags=['Test routes'])


class Study(BaseModel):
   FileName:Optional[str]
   PatientName:Optional[str]
   PatientID:Optional[str]
   StudyDate:Optional[str]
   StudyDescription:Optional[str]
   SeriesInstanceUID:Optional[str]
   StudyID:Optional[str]
   PatientBirthDate:Optional[str]


@test_router.get('/studies', response_model=List[Study])
async def list_studies():
    items = await db_manager.read_items()
    return items


@test_router.get('/')
async def process_studies():

    session = boto3.Session(
        aws_access_key_id=base_config.S3_ACCESS_KEY, 
        aws_secret_access_key=base_config.S3_SECRET_KEY)

    s3 = session.resource('s3')

    my_bucket = s3.Bucket(base_config.S3_BUCKET_NAME)
    
    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object.key)
        try:
            target_file = './raw_data/'+my_bucket_object.key            
            s3.Bucket(base_config.S3_BUCKET_NAME).download_file(
                my_bucket_object.key, 
                target_file
                )
            print(f"file saved {target_file } ")
        
            
            message = {
                'type': 'file_dowloaded',
                "file_name" : my_bucket_object.key
            }
            await rabbit_connection.send_messages(
               messages=message
            )
            
            

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
    return "text message is sent"
