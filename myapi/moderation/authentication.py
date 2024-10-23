import firebase_admin
from firebase_admin import auth
from rest_framework import authentication, exceptions

class FirebaseAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        token = auth_header.split(' ').pop()

        try:
            decoded_token = auth.verify_id_token(token)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid token')

        uid = decoded_token['uid']
        user = self.get_or_create_user(uid)

        return (user, None)

    def get_or_create_user(self, uid):
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(username=uid)
        except User.DoesNotExist:
            user = User.objects.create_user(username=uid)
        return user
