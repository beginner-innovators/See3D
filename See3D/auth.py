from flask import url_for, current_app, redirect, request
from rauth import OAuth2Service

import json, urllib2


class AuthenticationException(Exception):
    pass


class OAuthSignIn:
    """Generic sign-in template that allows for more providers to be added later."""
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name

        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth2callback', provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(self, provider_name):
        """Return the instance of a provider class given its name."""
        if self.providers is None:
            self.providers = {}

            # For every provider class given, create an instance of that class and add it to the self.providers dictionary.
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider

        return self.providers[provider_name]


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        # Create an instance of OAuthSignIn with 'google' as the provider name.
        super(GoogleSignIn, self).__init__('google')

        # Pull info from Google's published list of information, so that info is always up to date.
        # NOTE: if the application is initialized without internet connection, this class will not work correctly.
        google_info = urllib2.urlopen('https://accounts.google.com/.well-known/openid-configuration')
        google_params = json.load(google_info)

        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id
            client_secret=self.consumer_secret
            authorize_url=google_params.get('authorization_endpoint')
            access_token_url=google_params.get('token_endpoint')
            base_url=google_params.get('userinfo_endpoint')
        )

    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                scope='email',
                response_type='code',
                redirect_uri=self.get_callback_url()
            )
        )

    def callback(self):
        if 'code' not in request.args:
            return None

        data = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': self.get_callback_url()
        }

        oauth_session = self.service.get_auth_session(data=data, decoder=json.loads)
        user_info = oauth_session.get('').json()

        if user_info[aud] != self.consumer_id:
            raise AuthenticationException("Given 'aud' claim does not match consumer id.")

        return user_info
