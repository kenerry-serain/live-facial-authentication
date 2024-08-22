
def handler(event, context):
    print(event)
    response = {}

    # Usuário colocou a resposta errada 3 vezes - Falha Autenticação
    if 'session' in event['request'] and \
        len(event['request']['session']) >= 3 and \
        event['request']['session'][-1]['challengeResult'] == False:
            response['issueTokens'] = False
            response['failAuthentication'] = True

    # Usuário colocou a resposta certa - Sucesso Autenticação
    elif 'session' in event['request'] and \
         len(event['request']['session']) > 0 and \
         event['request']['session'][-1]['challengeResult'] == True:
            response['issueTokens'] = True
            response['failAuthentication'] = False
    
    # Nenhuma resposta provida ainda
    else:
        response['issueTokens'] = False
        response['failAuthentication'] = False
        response['challengeName'] = 'CUSTOM_CHALLENGE'

    event['response'] = response
    return event
