import identity.web
import requests
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from dotenv import load_dotenv

load_dotenv()

import app_config

__version__ = "0.1.0"  

app = Flask(__name__)

app.config.from_object(app_config)
assert app.config["REDIRECT_PATH"] != "/", "REDIRECT_PATH must not be /"
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

auth = identity.web.Auth(
    session=session,
    authority=app.config["AUTHORITY"],
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)

TARGETS = [
    {
        'id':1,
        'name':'Kathy Petersen',
        'relationship':'Mother',
        'DoB':'05/05/5555',
        'Interests': [
            {
                'id':1,
                'name':'gardening'
            },
            {
                'id':2,
                'name':'rv'
            }
        ]
    },
    {
        'id':2,
        'name':'Dan Petersen',
        'relationship':'Father',
        'DoB':'05/05/5555',
        'Interests': [
            {
                'id':1,
                'name':'fishing'
            },
            {
                'id':2,
                'name':'rv'
            }
        ]
    },
    {
        'id':3,
        'name':'Shaina Petersen',
        'relationship':'Wife',
        'DoB':'05/05/5555',
        'Interests': [
            {
                'id':1,
                'name':'reading'
            },
            {
                'id':2,
                'name':'sewing'
            }
        ]
    },
    {
        'id':4,
        'name':'Renee Wilson',
        'relationship':'Sister',
        'DoB':'05/05/5555',
        'Interests': [
            {
                'id':1,
                'name':'teaching'
            },
            {
                'id':2,
                'name':'gardening'
            }
        ]
    }
]


@app.route("/fnf")
def friend_and_family_list():
    if not (app.config["CLIENT_ID"] and app.config["CLIENT_SECRET"]):
        # This check is not strictly necessary.
        # You can remove this check from your production code.
        return render_template('config_error.html')
    if not auth.get_user():
        return redirect(url_for("login"))
    return render_template("target_list.html", title="Friends and Family", targets=TARGETS)

@app.route("/api/targets")
def return_target_list():
    return jsonify(TARGETS)

# Brought this in to support AADB2C
@app.route("/login")
def login():
    return render_template("login.html", version=__version__, **auth.log_in(
        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Azure Portal
        ))


@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    return redirect(url_for("friend_and_family_list"))


@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))


@app.route("/")
def index():
    if not (app.config["CLIENT_ID"] and app.config["CLIENT_SECRET"]):
        # This check is not strictly necessary.
        # You can remove this check from your production code.
        return render_template('config_error.html')
    if not auth.get_user():
        return redirect(url_for("login"))
    return render_template('index.html', user=auth.get_user(), version=__version__)


@app.route("/call_downstream_api")
def call_downstream_api():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))
    # Use access token to call downstream api
    api_result = requests.get(
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).json()
    return render_template('display.html', result=api_result)


# if __name__ == "__main__":
#     app.run()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)