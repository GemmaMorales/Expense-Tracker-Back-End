import os, urllib
from flask import Flask, request, jsonify, url_for, redirect
from models import db, User
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity, decode_jwt
)

def add_endpoints(app):
    @app.route('/quickbooks/connect', methods=['GET'])
  
    def get_quickbooks_credentials():
        token = request.args.get("token")
        decoded_payload = decode_jwt(token)
        print(decoded_payload)
      
        url = "https://appcenter.intuit.com/connect/oauth2"
        params = {
            "client_id": os.environ.get('QB_ID'),
            "scope": "com.intuit.quickbooks.accounting",
            "redirect_uri": os.environ.get('QB_REDIRECTURL'),
            "response_type": "code",
            "state": decoded_payload["sub"]
        }
        return redirect(url+"?"+urllib.parse.urlencode(params)), 200
    @app.route('/quickbooks/callback', methods=['GET'])
    def quickbooks_callback():
        url = "https://appcenter.intuit.com/connect/oauth2"
        code = request.args.get('code')
        user_id = request.args.get('state')
        realmId = request.args.get('realmId')
        print(f"This are your quickbooks credentials: code: {code} realm: {realmId}")
        user1 = User.query.get(user_id)
        user1.qb_code = code
        user1.qb_realmID = realmId
        db.session.commit()
        return jsonify("Redirecting back to the front end."), 200
    return app
# def save_credentials(quickbooks_code, quickbooks_realmid):