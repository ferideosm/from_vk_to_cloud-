import requests
import json

class VK:

    def __init__(self, token, version):
        self.token = token
        self.url = 'https://api.vk.com/method/'
        self.version = version

    def _token_params(self):
        return {
            'access_token': self.token,
            'v': self.version}

    def photo_params(self):
        params = self._token_params()
        params['album_id'] = 'profile'
        params['extended'] = 1
        return params

    def _get_biggest_size_photo_url(self, items, likes):
        max_width = 0
        max_height = 0
        for item in items:
            if item['width'] > max_width:
                max_width = item['width']

        for item in items:
            if item['width']  == max_width and item['height'] > max_height:
                max_height = item['height']  
                url = item['url']

        photo = {
            'size': item['type'],
            'url': url,
            'file_name': f"{likes['count']}.jpg"}

        return photo


    def get_photo(self):
        METHOD = 'photos.get'
        url = f'{self.url}{METHOD}'
        params = self.photo_params()
        response = requests.get(url, params=params).json()
       
        photos = []
        if response.get('error'):
            print(response)
            return

        with open('data.txt', 'w') as file:
            for item in response['response']['items']:
                photo = self._get_biggest_size_photo_url(item['sizes'], item['likes'])
                photos.append(photo)  
                json.dump(photo, file, sort_keys = True, indent = 2, ensure_ascii = False)     
        return photos
       



        



