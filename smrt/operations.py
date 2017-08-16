
from .protocol import *

def query_port_mirror_payload():
    return { get_id('port_mirror'): b'' }

def login_payload(username, password):
    username = username.encode('utf-8') + b'\x00'
    password = password.encode('utf-8') + b'\x00'
    return { get_id('username'): username, get_id('password'): password }

def get_token_id_payload():
    return { get_id('get_token_id'): b'' }
