import boto3
import botocore
from env.cons import Constantes
from botocore.exceptions import ClientError
import os
import logging
import requests

class aws:

    def subir_S3(ruta,rutaS3):

        s3 = boto3.resource('s3',
        region_name=Constantes.AWS_REGION_NAME
         
        )

        bucket=Constantes.AWS_BUCKET

        ruta=os.path.abspath(ruta)
        archivo=os.path.basename(ruta)
        rutas3f=rutaS3+'/'+archivo

        data = open(ruta, 'rb')
        s3.Bucket(bucket).put_object(Key=rutas3f, Body=data)

        return (rutas3f)

    def descargar_S3(rutaS3):
        try :
            s3 = boto3.resource('s3',
            region_name=Constantes.AWS_REGION_NAME
             
            )
            bucket=Constantes.AWS_BUCKET
            archivo=os.path.basename(rutaS3)
            ruta=Constantes.DOCUMENTOS+'/'+archivo
            s3.Bucket(bucket).download_file(rutaS3,ruta)
            print("se descargo archivo en:  ", ruta)
        except ClientError as e:

            print(e.response['Error']['Message'])
            return "error al descargar archivo"
        except:
            return "error al descargar archivo"

        return ruta
        
    def url_S3(rutas3):
        s3 = boto3.client('s3',
        region_name=Constantes.AWS_REGION_NAME
         
        )

        s3r = boto3.resource('s3',
        region_name=Constantes.AWS_REGION_NAME
         
        )

        try:
            s3r.Object( Constantes.AWS_BUCKET, rutas3).load()
        except botocore.exceptions.ClientError as e:
            return str(e)

        url = s3.generate_presigned_url(
        ClientMethod='get_object', 
        Params={'Bucket': Constantes.AWS_BUCKET, 'Key': rutas3},
        # ExpiresIn=3600
        )
        return url


    def send_sqs(idSolicitud,queue_url):

        # import boto3
        # AWS_ACCESS_KEY = 'AKIAUDBWMVIT2W3HCNMR'
        # AWS_REGION_NAME = 'us-east-1'
        # AWS_SECRET_KEY = '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'
        # sqs = boto3.client('sqs',
        # region_name=AWS_REGION_NAME,
        # aws_access_key_id=AWS_ACCESS_KEY, 
        # aws_secret_access_key=AWS_SECRET_KEY)   

        sqs = boto3.client('sqs',
        region_name=Constantes.AWS_REGION_NAME
         
        )     

        # queue_url = 'https://sqs.us-east-1.amazonaws.com/281434434087/nuevaEPS'

        # Send message to SQS queue
        mensaje={}
        mensaje["idSolicitud"]=idSolicitud
        
        time=0
        if Constantes.url_envioCorreos==queue_url:
            time=900

        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=time,
            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': 'Nueva EPS validacion derechos'
                },
                'Author': {
                    'DataType': 'String',
                    'StringValue': 'Cristian Rodríguez'
                },
            },
            MessageBody=(
                str(mensaje).replace("'",'"')
            )
        )

        print(response['MessageId'])

    def get_file_s3( key):

        s3 = boto3.client('s3',
        region_name=Constantes.AWS_REGION_NAME
         
        )   
        bucket=Constantes.AWS_BUCKET
        response = s3.get_object(Bucket=bucket, Key=key)
        archivo = response['Body'].read()

        return archivo

    def get_file_cloudFront( key):

        urlDescarga=Constantes.cloudFront+'/'+key
        file = requests.get(urlDescarga, allow_redirects=True)

        return file.content


    def create_presigned_post(bucket_name, object_name,
                            fields=None, conditions=None, expiration=60):
        """Generate a presigned URL S3 POST request to upload a file

        :param bucket_name: string
        :param object_name: string
        :param fields: Dictionary of prefilled form fields
        :param conditions: List of conditions to include in the policy
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Dictionary with the following keys:
            url: URL to post to
            fields: Dictionary of form fields and values to submit with the POST
        :return: None if error.
        """

        # Generate a presigned S3 POST URL 
        s3_client = boto3.client('s3',
            region_name=Constantes.AWS_REGION_NAME
             
            )  
        
        try:
            response = s3_client.generate_presigned_post(bucket_name,
                                                        object_name,
                                                        Fields=fields,
                                                        Conditions=conditions,
                                                        ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None

        return response
        
