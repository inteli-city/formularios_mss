import json
from src.modules.get_form_by_user_id.app.get_form_by_user_id_presenter import lambda_handler


class Test_GetFormByUserPresenter:
     def test_get_form_by_user_id_presenter(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": {
                "parameter1": "1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "claims":
                        {
                            "sub": "1",
                            "name": "Gabriel Godoy",
                            "email": "gabriel.godoy@gmail.com",
                            "cognito:groups": "FORMULARIOS"
                        }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }
        
        response = lambda_handler(event, None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["message"] == 'Formulários retornados com sucesso!'