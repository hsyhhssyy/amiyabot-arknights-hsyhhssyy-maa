import re

from core.util import read_yaml

serve_conf = read_yaml('config/server.yaml')

def is_strong_password():

    password = serve_conf.authKey

    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

def get_password():
    return serve_conf.authKey