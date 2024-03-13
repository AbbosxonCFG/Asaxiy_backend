
import jwt, datetime
from .models import User
from rest_framework.exceptions import  NotAcceptable
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import  NotAcceptable, AuthenticationFailed

def create_access_token(id):
    return jwt.encode({
        "user_id": id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
    }, "access_secret", algorithm="HS256")


def decode_access_token(token):
    try:
        payload = jwt.decode(token, "access_secret", algorithms=["HS256"])
        return payload['user_id']
    except jwt.ExpiredSignatureError as ex:
        raise NotAcceptable("Token was expired")
    except jwt.DecodeError as ex:
        raise NotAcceptable("Token is invalid")


def create_refresh_token(id):
    return jwt.encode({
        "user_id": id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=60),
        "iat": datetime.datetime.utcnow(),
    }, "refresh_secret", algorithm="HS256")


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, "refresh_secret", algorithms=["HS256"])
        return payload['user_id']
    except:
        raise NotAcceptable("unauthenticated")
    



class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):

        auth = get_authorization_header(request).split()
        
        if len(auth) != 2:
            raise AuthenticationFailed("unauthenticated")

        token = auth[1].decode('utf-8')
        id = decode_access_token(token)
        print(id, "id")
        try:
            user = User.objects.get(id=id)
            return (user, token)
            
        except User.DoesNotExist as no_user:
            raise AuthenticationFailed("No such user")