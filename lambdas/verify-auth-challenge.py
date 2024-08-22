import json
import os
import boto3
from botocore.exceptions import ClientError

rekognition = boto3.client('rekognition')
userFacesBucket = os.environ['USER_FACES_BUCKET']
rekognitionCollectionId = os.environ['REKOGNITION_COLLECTION_ID']

def handler(event, context):
    print(event)

    userSignUpPicture = ''
    event['response']['answerCorrect'] = False

    # Parâmetros para buscar fotos indexadas no Amazon Rekognition baseado na foto tirada do usuário durante login (S3 Object Key)
    s3ObjectKey = event['request']['challengeAnswer']
    params = {
        'CollectionId': rekognitionCollectionId,
        'Image': {
            'S3Object': {
                'Bucket': userFacesBucket,
                'Name': s3ObjectKey
            }
        },
        'MaxFaces': 1,
        'FaceMatchThreshold': 90
    }

    try:
        rekognitionItems = rekognition.search_faces_by_image(**params)
        userFaceMatches = rekognitionItems.get('FaceMatches', [])

        # Verificando se encontrou algum match
        print('Face Matches: %s', userFaceMatches)

        if userFaceMatches:
            print('Face Id: %s', userFaceMatches[0]['Face']['FaceId'])
            print('Similarity: %s', userFaceMatches[0]['Similarity'])

            userSignUpPicture = userFaceMatches[0]['Face']['FaceId']
            
            # Verificando se o RekognitionId identificado como match na foto de sign in é o mesmo que foi indexado na foto de sign up
            if userSignUpPicture:
                if event['request']['privateChallengeParameters']['answer'] == userSignUpPicture:
                    print('User provided the correct answer')
                    event['response']['answerCorrect'] = True

    except ClientError as exception:
        print("Unable to query. Error: %s", json.dumps(exception.response, indent=2))
        raise exception

    return event
