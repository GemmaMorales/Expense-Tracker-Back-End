import os, urllib, requests, base64

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

from flask import Flask, request, jsonify, url_for, redirect
from models import db, User
from utils import APIException
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity, decode_jwt
)

def add_endpoints(app):

    auth_client = AuthClient(
        os.environ.get('QB_ID'),
        os.environ.get('QB_SECRET'),
        os.environ.get('QB_REDIRECTURL'),
        os.environ.get('QB_ENVIRONMENT'),

    )
    @app.route('/quickbooks/connect', methods=['GET'])
    def get_quickbooks_credentials():
        token = request.args.get("token")
        decoded_payload = decode_jwt(token)
      
        url = auth_client.get_authorization_url([Scopes.ACCOUNTING], state_token=decoded_payload["sub"])

        return redirect(url), 200

    @app.route('/quickbooks/callback', methods=['GET'])
    def quickbooks_callback():
        url = "https://appcenter.intuit.com/connect/oauth2"
        code = request.args.get('code')
        user_id = request.args.get('state')
        realmId = request.args.get('realmId')
        print(f"These are your quickbooks credentials: code: {code} realm: {realmId}")
        user1 = User.query.get(user_id)
        user1.qb_code = code
        user1.qb_realmID = realmId
        db.session.commit()

        sync_token(user_id)
        return jsonify(f"Hello {user1.name}!! Redirecting to private view."), 200

    def sync_token(user):
        url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

        auth_client.get_bearer_token(user.qb_code, realm_id=user.qb_realmID)
        user.qb_token = auth_client.access_token
        db.session.commit()

        return auth_client.access_token
    return app

# def save_credentials(quickbooks_code, quickbooks_realmid): ?


class QuickBooks():
    def __init__(token, realm_id):
        self.token = token
        self.realm_id = realm_id
        self.base_url = 'https://sandbox-quickbooks.api.intuit.com'

    def get_company_info():
        url = f'{self.base_url}/v3/company/{self.realm_id}/companyinfo/{self.realm_id}'
        auth_header = 'Bearer {0}'.format(self.token)
        headers = {
            'Authorization': auth_header,
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        payload = response.json()

        return payload