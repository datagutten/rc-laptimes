import requests


class MyLapsSpeedHive:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36'
        })

    def activities(self, mylaps_id: int):
        url = f'https://practice-api.speedhive.com/api/v1/locations/{mylaps_id}/activities?count=25&offset=0'
        response = self.session.get(url, headers={
            'Accept': 'application/json',
            'Origin': 'https://speedhive.mylaps.com',
            'Referer': 'https://speedhive.mylaps.com/'
        })
        response.raise_for_status()
        return response.json()['activities']
