from functools import wraps
from flask import session, redirect

def loginRequried(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated

def noLoginRequried(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated