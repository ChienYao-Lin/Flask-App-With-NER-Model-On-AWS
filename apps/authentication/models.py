# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from boto3.dynamodb.conditions import Key
from apps import db, login_manager

from apps.authentication.util import hash_pass

class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if not user_exist(username):
        return

    user = User()
    user.username = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if not user_exist(username):
        return

    user = User()
    user.username = username
    return user


def user_exist(username):
    table = db.Table("Users")
    if not username:
        return
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
        )
    return response['Items']


def add_user(username, password):
    table = db.Table("Users")
    response = table.put_item(
        Item={
            'username' : username,
            'password': hash_pass(password),
        }
    )
    return response 

def ch_password(username, new_password):
    table = db.Table("Users")
    response = table.update_item(
    Key={
        'username': username,
    },
    UpdateExpression="set #password = :val1 ",
    ExpressionAttributeValues={
        ':val1': hash_pass(new_password),
    },
    ExpressionAttributeNames={
    "#password": "password"
    },
    ReturnValues="UPDATED_NEW"
    )
        
    return response 