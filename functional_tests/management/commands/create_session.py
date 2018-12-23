from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    '''command'''

    def add_arguments(self, parser):
        '''add arguments'''
        parser.add_argument('email')

    def handle(self, *args, **options):
        '''handle'''
        session_key = create_pre_authenticated_session(options['email'])
        self.stdout.write(session_key)


def create_pre_authenticated_session(email):
    '''create pre authenticated session'''
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key
