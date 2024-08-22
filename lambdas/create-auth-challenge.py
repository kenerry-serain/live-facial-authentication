import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
dynamoDbCollectionId = os.environ['DYNAMODB_COLLECTION_ID']

def handler(event, context):
    print(event)

    # Verificando se é o fluxo de autenticação customizado
    if event['request']['challengeName'] == 'CUSTOM_CHALLENGE':
        
        challengeAnswer = ''
        event['response']['publicChallengeParameters'] = {}
        userFacesTable = dynamodb.Table(dynamoDbCollectionId)
        
        # Parâmetros para varrer a tabela do Dynamo procurando UserId
        params = {
            'IndexName': "UserId-index",
            'ProjectionExpression': "RekognitionId",
            'KeyConditionExpression': "UserId = :UserId",
            'ExpressionAttributeValues': {
                ':UserId': event['userName']
            }
        }
        
        try:
            
            queryResponse = userFacesTable.query(**params)
            userFoundFacesByUserId = queryResponse.get('Items', [])
            
            for item in userFoundFacesByUserId:
                # Se encontrar uma foto indexada, marca aquele RekognitionId como resposta certa
                challengeAnswer = item.get('RekognitionId', '')
                event['response']['publicChallengeParameters']['captchaUrl'] = challengeAnswer
                event['response']['privateChallengeParameters'] = {'answer': challengeAnswer}
                event['response']['challengeMetadata'] = 'REKOGNITION_CHALLENGE'
                
                print("Create Challenge Output: %s", json.dumps(event))
                return event
                
        except ClientError as exception:
            print("Unable to query. Error: %s", json.dumps(exception.response, indent=2))
            raise exception
    
    return event
