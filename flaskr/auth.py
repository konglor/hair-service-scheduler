import functools

from flask import Blueprint, flash, g, redirect, jsonify, request, json, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

# from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# /auth/register
@bp.route('/register', methods=['POST'])
def register():

    from flaskr.models import db, UserAccount
    json = request.get_json()
    transaction_keys = ['username' , 'email', 'password', 'passwordConfirm']

    if not all (key in json for key in transaction_keys):
      return '400 Bad Request - missing fields', 400

    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    passwordConfirm = request.get_json()['passwordConfirm']

    # check if there is already a user logged in
    # check if useraccount already exist
    useraccount_username = UserAccount.query.filter_by(username=username).first()
    if  useraccount_username:
      return '409 User already exist', 409

    # check if email already exist
    useraccount_email = UserAccount.query.filter_by(email=email).first()
    if useraccount_email:
      return '409 Existing account with associated email', 409

    # check if the password is equal to passwordConfirm
    if password != passwordConfirm:
      return '401 Password mismatch', 401

    # create the useraccount
    newaccount = UserAccount(username, email, password)

    # add the user to database
    db.session.add(newaccount)
    db.session.commit()

    # tell the user to complete registration through email
    result = {
      "status": "asd"
    }
    return jsonify({"results": result}), 201