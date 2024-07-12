import os
from pydantic import BaseSettings


class Base(BaseSettings):
    RABBITMQ_DEFAULT_USER: str =  os.environ['RABBITMQ_DEFAULT_USER']
    RABBITMQ_DEFAULT_PASS: str = os.environ['RABBITMQ_DEFAULT_PASS']
    RABBITMQ_LOCAL_HOST_NAME: str =  os.environ['RABBITMQ_LOCAL_HOST_NAME']
    RABBITMQ_LOCAL_PORT: int = os.environ['RABBITMQ_LOCAL_PORT']
    RABBITMQ_QUEUE: str =  os.environ['RABBITMQ_QUEUE']

    S3_ACCESS_KEY : str =  os.environ['S3_ACCESS_KEY']
    S3_SECRET_KEY : str =  os.environ['S3_SECRET_KEY']
    S3_REGION : str =  os.environ['S3_REGION']
    S3_BUCKET_NAME : str =  os.environ['S3_BUCKET_NAME']
    S3_ANONYMIZED_BUCKET_NAME : str =  os.environ['S3_ANONYMIZED_BUCKET_NAME']

                                      



    CLIENT_ORIGIN: str = 'http://localhost:3000'


base_config = Base()

RABBIT_URL = f'amqp://{base_config.RABBITMQ_DEFAULT_USER}:' \
             f'{base_config.RABBITMQ_DEFAULT_PASS}@' \
             f'{base_config.RABBITMQ_LOCAL_HOST_NAME}:' \
             f'{base_config.RABBITMQ_LOCAL_PORT}/'
