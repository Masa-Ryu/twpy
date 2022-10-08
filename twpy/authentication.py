import json
from os.path import isfile

from requests_oauthlib import OAuth1Session


class Authentication:
    def __init__(self, file_name=None):
        if file_name is None:
            self.file_name = 'apis.json'
        else:
            self.file_name = file_name

    def set_api(self):
        if isfile(f'./{self.file_name}'):
            with open(f'./{self.file_name}', 'r') as file_name:
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
            raise FileNotFoundError('Api file not found')
