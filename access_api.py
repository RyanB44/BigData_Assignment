import string
import json
import requests as req
from redis_connect import get_redis_connection

r = get_redis_connection()
r.flushdb()


class ApiConnect:

    def __init__(self):
        token = self.authorize_api()
        if token != "FAIL":
            self.access_api_and_upload(token)

    def authorize_api(self):
        """Connect to spotify API and authenticate using client id and secret key

         Returns:
             Access token to perform GET calls to API
         """
        clientID = "085ac6d56e0d4ee89afb60de37a0f11f"
        secretID = "INSERT_SECRET_KEY_HERE"
        auth_url = "https://accounts.spotify.com/api/token"

        response = req.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': clientID,
            'client_secret': secretID
        })
        if response.status_code != 200:
            return 'FAIL'
        jsonresp = response.json()
        return jsonresp['access_token']

    def access_api_and_upload(self, auth_token: string):
        """Perform Get call into the API and insert into redis database

         Returns:
             n/a
         """
        base_url = "https://api.spotify.com/v1/"
        track_offset = 0
        httpget_headers = {
            'Authorization': 'Bearer {token}'.format(token=auth_token)
        }
        for i in range(100):
            response = req.get(
                base_url + 'playlists/37i9dQZF1DX1cJWWyylDuw/tracks?market=US&limit=1&offset={offset}'.format(
                    offset=track_offset), headers=httpget_headers)
            data = response.json()
            r.json().set('playlist:tracks:track{offset}'.format(offset=track_offset), '.', json.dumps(data))
            track_offset += 1
