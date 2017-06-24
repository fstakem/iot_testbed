# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    6.12.17   
#
# -----------------------------------------------------------------------------------------------


# Libraries
from functools import wraps
from flask import g, request, redirect, url_for, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session :
            return redirect('login')
        return f(*args, **kwargs)
    return decorated_function