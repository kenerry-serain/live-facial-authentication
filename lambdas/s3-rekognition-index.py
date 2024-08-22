from __future__ import print_function
import os

import boto3

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
rekognition = boto3.client('rekognition')

dynamoDbCollectionId = os.environ['DYNAMODB_COLLECTION_ID']
rekognitionCollectionId = os.environ['REKOGNITION_COLLECTION_ID']


def handler(event, context):
    print(event)
    bucketName = event['Records'][0]['s3']['bucket']['name']
    bucketObjectKey = event['Records'][0]['s3']['object']['key']
    bucketObjectKeyUrl = f's3://{bucketName}/{bucketObjectKey}'
    try:

        # Indexando foto do usuário no Amazon Rekognition
        response = indexUserFace(bucketName, bucketObjectKey)
        
        # Salvando RekognitionId associado ao UserId no DynamoDB
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            s3Response = s3.head_object(Bucket=bucketName,Key=bucketObjectKey)
            userId = s3Response['Metadata']['user-id']
            saveUserInformationOnDynamoDb(dynamoDbCollectionId,faceId, userId) 
        return response
    except Exception as exception:
        print("Error processing object {} from bucket {}. ".format(bucketObjectKeyUrl, bucketName))
        raise exception
    

def indexUserFace(bucket, key):
    response = rekognition.index_faces(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            }
        },
        CollectionId=rekognitionCollectionId)
    return response

def saveUserInformationOnDynamoDb(tableName,faceId, userId):
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'RekognitionId': {'S': faceId},
            'UserId': {'S': userId}
        })
    return response
    