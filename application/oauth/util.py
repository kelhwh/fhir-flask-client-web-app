from flask import redirect, render_template, url_for, flash
from fhirclient.server import FHIRUnauthorizedException
from fhirclient.models import patient
from functools import wraps
from application.fhir.connect import smart

def oauth_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            flash("Please login first.")
            return redirect(url_for('oauth_bp.index'))
        else:
            return render_template('error.html')
        return func(*args, **kwargs)
    return decorated_view
