
from botocore.exceptions import ClientError, ParamValidationError
from django.conf import settings
import uuid

from thistothat.common.aws import exceptions, get_boto_client


def change_password(old_password, new_password, access_token):

    client = get_boto_client('cognito-idp')

    try:
        client.change_password(
            PreviousPassword=old_password,
            ProposedPassword=new_password,
            AccessToken=access_token
        )
    except client.exceptions.NotAuthorizedException:
        raise exceptions.NotAuthorizedException
    except client.exceptions.LimitExceededException:
        raise exceptions.LimitExceededException
    except ParamValidationError:
        raise exceptions.ParamValidationError



def confirm_account(email):

    client = get_boto_client('cognito-idp')

    client.admin_confirm_sign_up(
        UserPoolId=settings.COGNITO_USER_POOL_ID,
        Username=email
    )


def create_user(email, name, password):

    client = get_boto_client('cognito-idp')

    try:
        response = client.sign_up(
            ClientId=settings.COGNITO_APP_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                }
            ]
        )
    except ParamValidationError:
        raise exceptions.ParamValidationError
    except client.exceptions.InvalidParameterException:
        raise exceptions.InvalidParameterException
    except client.exceptions.UsernameExistsException:
        raise exceptions.UsernameExistsException
    else:
        return response['UserSub']


def delete_all_users():
    assert settings.STAGE != 'production'

    client = get_boto_client('cognito-idp')
    response = client.list_users(
        UserPoolId=settings.COGNITO_USER_POOL_ID,
        AttributesToGet=[
            'email',
        ],
    )
    users = response['Users']
    print(f'...removing {len(users)} Cognito users')
    for user in users:
        client.admin_delete_user(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=user['Username']
        )


def delete_user(sub):

    client = get_boto_client('cognito-idp')
    client.admin_delete_user(
        UserPoolId=settings.COGNITO_USER_POOL_ID,
        Username=sub
    )



def get_is_email_verified(email):

    client = get_boto_client('cognito-idp')
    cognito_response = client.admin_get_user(
        UserPoolId=settings.COGNITO_USER_POOL_ID,
        Username=email
    )

    is_email_verified = False
     # TODO: better way to loop through dictionary to compare a value?
    for attr in cognito_response['UserAttributes']:
        if attr['Name'] == 'email_verified':
            is_email_verified = attr['Value'] == 'true'
            break

    return is_email_verified


def refresh_access_token(refresh_token):

    client = get_boto_client('cognito-idp')

    try:
        response = client.initiate_auth(
            ClientId=settings.COGNITO_APP_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
            }
        )
    except client.exceptions.NotAuthorizedException:
        raise exceptions.NotAuthorizedException

    return response['AuthenticationResult']['AccessToken'] # fixme: is this safe?


def reset_password_start(email):

    client = get_boto_client('cognito-idp')

    try:
        client.forgot_password(
            ClientId=settings.COGNITO_APP_ID,
            Username=email
        )
    except client.exceptions.NotAuthorizedException:
        raise exceptions.NotAuthorizedException
    except client.exceptions.InvalidParameterException:
        raise exceptions.InvalidParameterException
    except client.exceptions.LimitExceededException:
        raise exceptions.LimitExceededException
    except client.exceptions.UserNotFoundException:
        raise exceptions.UserNotFoundException


def reset_password_confirm(email, code, password):
    
    client = get_boto_client('cognito-idp')

    try:
        client.confirm_forgot_password(
            ClientId=settings.COGNITO_APP_ID,
            Username=email,
            ConfirmationCode=code,
            Password=password
        )
    except client.exceptions.CodeMismatchException:
        raise exceptions.CodeMismatchException
    except client.exceptions.ExpiredCodeException:
        raise exceptions.ExpiredCodeException
    except client.exceptions.UserNotFoundException:
        raise exceptions.UserNotFoundException
    except ParamValidationError:
        raise exceptions.ParamValidationError


def sign_in_user(email, password):

    client = get_boto_client('cognito-idp')

    try:
        response = client.admin_initiate_auth(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            ClientId=settings.COGNITO_APP_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH', # must configure app client
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
    except client.exceptions.NotAuthorizedException:
        raise exceptions.NotAuthorizedException
    except client.exceptions.UserNotConfirmedException:
        raise exceptions.UserNotConfirmedException
    except client.exceptions.UserNotFoundException:
        raise exceptions.UserNotFoundException

    # check if password change required
    if response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
        raise exceptions.NewPasswordRequiredError

    return {
        'access_token': response['AuthenticationResult']['AccessToken'],
        'refresh_token': response['AuthenticationResult']['RefreshToken'],
    }


def sign_out_user(email):

    client = get_boto_client('cognito-idp')
    client.admin_user_global_sign_out(
        UserPoolId=settings.COGNITO_USER_POOL_ID,
        Username=email
    )


def update_account(email, attrs):

    client = get_boto_client('cognito-idp')
    try:
        client.admin_update_user_attributes(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=email,
            UserAttributes=attrs
        )
    except client.exceptions.AliasExistsException:
        raise exceptions.AliasExistsException


def verify_email(email):

    client = get_boto_client('cognito-idp')
    client.admin_update_user_attributes(
        UserPoolId=settings.COGNITO_USER_POOL_ID,
        Username=email,
        UserAttributes=[
            {
                'Name': 'email_verified',
                'Value': 'true'
            },
        ]
    )


def verify_user_attribute(attribute, code, access_token):

    client = get_boto_client('cognito-idp')

    try:
        client.verify_user_attribute(
            AccessToken=access_token,
            AttributeName=attribute,
            Code=code
        )
    except client.exceptions.CodeMismatchException:
        raise exceptions.CodeMismatchException

