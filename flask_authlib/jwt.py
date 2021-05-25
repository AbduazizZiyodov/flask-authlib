import os
import json
from flask import Flask
from flask import jsonify
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from .exceptions import AuthError


class JWT(object):
    def __init__(self,
                 app: Flask,
                 AUTH0_DOMAIN: str = None,
                 API_AUDIENCE: str = None,
                 ALGORITHMS: list = ["RS256"],
                 ) -> None:
        self.app = app
        self.AUTH0_DOMAIN = AUTH0_DOMAIN
        self.API_AUDIENCE = API_AUDIENCE
        self.ALGORITHMS = ALGORITHMS
        self.JSON_URL = f'https://{self.AUTH0_DOMAIN}/.well-known/jwks.json'
        self.setup()
        self.required = self.get_requires_auth_decorator()
    def setup(self):
        @self.app.errorhandler(AuthError)
        def auth_error_handler(AuthError):
            return (jsonify(
                {
                    "error": AuthError.status_code,
                    "message": AuthError.error["message"],
                    "success": False,
                }
            ), AuthError.status_code,)

    def get_token_auth_header(self):
        header = request.headers.get('Authorization', None)
        if header is None:
            raise AuthError({
                'code': 401,
                'message': 'Authorization not in header'
            }, 401)

        result = header.split('Bearer ')
        if len(result) != 2:
            raise AuthError({
                'code': 401,
                'message': 'Authorization header is invalid. Bearer token not found'
            }, 401)
        token = result[1]

        if not token:
            raise AuthError({
                'code': 401,
                'message': 'Authorization header is invalid. Bearer token is empty'
            }, 401)

        return token

    def check_permissions(self, permission, payload):
        permissions = payload.get('permissions', None)
        if permissions is None:
            raise AuthError({
                'code': 401,
                'message': 'Any permissions not in token'
            }, 401)
        if permission not in permissions:
            raise AuthError({
                'code': 401,
                'message': 'Permission not found this action'
            }, 401)

    def verify_decode_jwt(self, token):
        json_url = urlopen(self.JSON_URL)
        jwks = json.loads(json_url.read())

        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise AuthError({
                'code': 401,
                'message': 'Error decoding token headers.'
            }, 401)
        rsa_key = {}

        if 'kid' not in unverified_header:
            raise AuthError({
                'code': 401,
                'message': 'Authorization malformed.'
            }, 401)

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=self.ALGORITHMS,
                    audience=self.API_AUDIENCE,
                    issuer='https://' + self.AUTH0_DOMAIN + '/'
                )

                return payload
            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 401,
                    'message': 'Token expired.'
                }, 401)
            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 401,
                    'message': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
            except Exception:
                raise AuthError({
                    'code': 401,
                    'message': 'Unable to parse authentication token.'
                }, 401)

        raise AuthError({
            'code': 401,
            'message': 'Unable to find the appropriate key.'
        }, 401)

    def get_requires_auth_decorator(self):
        def requires_auth(permission=''):
            def requires_auth_decorator(f):
                @wraps(f)
                def wrapper(*args, **kwargs):
                    token = self.get_token_auth_header()
                    payload = self.verify_decode_jwt(token)
                    self.check_permissions(permission, payload)
                    return f(payload, *args, **kwargs)
                return wrapper
            return requires_auth_decorator
        return requires_auth
