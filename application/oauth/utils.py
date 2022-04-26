from flask import redirect, render_template, url_for, flash
from fhirclient.server import FHIRUnauthorizedException
from fhirclient.models import patient
from functools import wraps
from application.fhir.connect import connector

def oauth_required(func):
    """Decorator to enforce the requirement of OAuth
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        smart = connector.source_client

        if smart:
            #Check smart client has already been set up.
            try:
                return func(*args, **kwargs)
            except Exception:
                flash("Please login first.")
                return redirect(url_for('oauth_bp.index', connection_type='source'))
            else:
                return render_template('error.html')
        else:
            flash("Please login first.")
            return redirect(url_for('oauth_bp.index', connection_type='source'))

        return func(*args, **kwargs)

    return decorated_view
