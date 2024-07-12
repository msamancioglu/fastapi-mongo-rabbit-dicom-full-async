import json
import logging
from db import db_manager
from aio_pika.abc import AbstractIncomingMessage
from pydantic import BaseModel
from typing import Optional

import boto3
import botocore
import pydicom
import datetime
from config.base import base_config 



async def message_router(
        message: AbstractIncomingMessage,
) -> None:
    async with message.process():
        body = json.loads(message.body.decode())
        if body.get('type') == 'file_dowloaded':
            file_name = body.get("file_name")    
            dicom = pydicom.dcmread('./raw_data/'+file_name, force=True)
            item = {
                "FileName":str(file_name),
                "PatientName":str(dicom.PatientName),
                "PatientID":str(dicom.PatientID),
                "StudyDate":str(dicom.StudyDate),
                "StudyDescription":str(dicom.StudyDescription),
                "StudySeriesUID":str(dicom.SeriesInstanceUID),
                "StudyID":str(dicom.StudyID),
                "PatientBirthDate":str(dicom.PatientBirthDate )           
            }
            new_item = await db_manager.create_item(item)
            logging.info("Created new item on mongodb ")
            logging.info(new_item)
            #Anonymize study
            dicom.PatientName = "Test^Firstname"
            dicom.PatientID = "123456"
            # Set creation date/time
            dt = datetime.datetime.now()
            dicom.ContentDate = dt.strftime('%Y%m%d')
            timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
            dicom.ContentTime = timeStr

            dicom.save_as('./anonymized_data/'+file_name, write_like_original=True)

            #Upload anonymized files to 
            session = boto3.Session(
            aws_access_key_id=base_config.S3_ACCESS_KEY, 
            aws_secret_access_key=base_config.S3_SECRET_KEY)

            s3 = session.resource('s3')

            my_bucket = s3.Bucket(base_config.S3_BUCKET_NAME)

            s3.Bucket(base_config.S3_ANONYMIZED_BUCKET_NAME).upload_file(
                './anonymized_data/'+file_name, 
                file_name)

            return None
        return logging.info('Not recognized task type')


__all__ = ['message_router']
