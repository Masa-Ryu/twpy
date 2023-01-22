import json
from os.path import isfile

from requests_oauthlib import OAuth1Session


class Authentication:
    def from_file_authentication(self, file_name):
        if isfile(f'./{file_name}'):
            with open(f'./{file_name}', 'r') as file_name:
                api_information = json.load(file_name)
                api_key = api_information['api_key']
                api_key_secret = api_information['api_key_secret']
                bearer_token = api_information['bearer_token']
                access_token = api_information['access_token']
                access_token_secret = api_information['access_token_secret']
            return OAuth1Session(
                    api_key,
                    api_key_secret,
                    access_token,
                    access_token_secret,
                    bearer_token,
                    ), {'Authorization': f'Bearer {bearer_token}'}
            # bearer_token = api_information['APIV2']['bearer_token']  # Todo: no need?
            # self._HEADERS = {'Authorization': f'Bearer {bearer_token}'}   #todo: no need?
        else:
            raise FileNotFoundError('Api file not found. Prepare "apis.json". ')

    def from_non_file_authentication(self, guest, **kwargs):
        api_key = kwargs['api_key']
        api_key_secret = kwargs['api_key_secret']
        access_token = kwargs['access_token']
        access_token_secret = kwargs['access_token_secret']
        if guest:
            return OAuth1Session(
                    api_key,
                    api_key_secret,
                    access_token,
                    access_token_secret,
                    ), None
        else:
            bearer_token = kwargs['bearer_token'],
            return OAuth1Session(
                    api_key,
                    api_key_secret,
                    access_token,
                    access_token_secret,
                    bearer_token,
                    ), {'Authorization': f'Bearer {bearer_token}'}
