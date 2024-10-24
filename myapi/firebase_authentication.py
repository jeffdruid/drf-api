import firebase_admin
from firebase_admin import auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

firebase_admin.initialize_app()

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # No token provided

        try:
            # Extract token from header
            token = auth_header.split(' ')[1]
            decoded_token = auth.verify_id_token(token)
            user_id = decoded_token['uid']

            # Optionally, verify email and other fields
            email_verified = decoded_token.get('email_verified', False)
            if not email_verified:
                raise AuthenticationFailed("Email not verified.")

            # Return (user, token)
            return (user_id, token)
        except Exception as e:
            raise AuthenticationFailed(f'Invalid Firebase token: {str(e)}')
