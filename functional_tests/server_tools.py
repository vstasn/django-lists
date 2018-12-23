from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(host):
    '''get manage dot py'''
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'


def reset_database(host):
    '''reset database'''
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'vt@{host}'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    '''create session on server'''
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'vt@{host}'):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()
