from accounts.models import User, Token


class PasswordlessAuthenticationBackend(object):
    '''passwordless authentication backend'''

    def authenticate(self, request, uid):
        '''authenticate'''
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        '''get user'''
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
