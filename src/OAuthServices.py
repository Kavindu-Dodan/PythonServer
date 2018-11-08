import json
import time

import oauth2 as oauth

_URL_FIELD = "url"
_TOKEN_KEY_FIELD = "tokenkey"
_TOKEN_SECRET_FIELD = "tokensecret"
_CONSUMER_KEY_FIELD = "consumerkey"
_CONSUMER_SECRET_FIELD = "consumersecret"
_REALM_FIELD = "realm"
_METHOD_FIELD = "method"


class OAuth1:

    def __init__(self, app, flask_request):
        self.app = app
        self.request = flask_request

    def process(self):
        if self.request.is_json:
            payload = json.loads(self.request.data)
            self.verify_fields(payload)

            return self.gen_header(payload)
        else:
            raise Exception("Payload must be JSON")

    def gen_header(self, payload):
        url = payload[_URL_FIELD]
        token = oauth.Token(key=payload[_TOKEN_KEY_FIELD],
                            secret=payload[_TOKEN_SECRET_FIELD])
        consumer = oauth.Consumer(key=payload[_CONSUMER_KEY_FIELD],
                                  secret=payload[_CONSUMER_SECRET_FIELD])

        http_method = payload[_METHOD_FIELD]
        realm = payload[_REALM_FIELD]

        params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': str(int(time.time())),
            'oauth_token': token.key,
            'oauth_consumer_key': consumer.key
        }

        req = oauth.Request(method=http_method, url=url, parameters=params)
        signature_method = oauth.SignatureMethod_HMAC_SHA1()

        req.sign_request(signature_method, consumer, token)
        header = req.to_header(realm)
        return header['Authorization']

    @staticmethod
    def verify_fields(payload):
        if _URL_FIELD not in payload:
            raise Exception("URL not provided")

        if _REALM_FIELD not in payload:
            raise Exception("Realm not provided")

        if _METHOD_FIELD not in payload:
            raise Exception("Method not provided")

        if _TOKEN_KEY_FIELD not in payload:
            raise Exception("Token Key not provided")

        if _TOKEN_SECRET_FIELD not in payload:
            raise Exception("Token Secret not provided")

        if _CONSUMER_KEY_FIELD not in payload:
            raise Exception("Consumer Key not provided")

        if _CONSUMER_SECRET_FIELD not in payload:
            raise Exception("Consumer Secret not provided")
