import requests
import json
import datetime

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

    def _get_biggest_size_photo_url(self, items):

        photo_set = set() 
        photos = []

        for item in items:                     
            max_width = 0
            max_height = 0
            for i in item['sizes']:
                if i['width'] > max_width:
                    max_width = i['width']

            for i in item['sizes']:
                if i['width']  == max_width and i['height'] > max_height:
                    max_height = i['height']  
                    url = i['url']

            if item['likes']['count'] in photo_set:
                date = datetime.datetime.fromtimestamp(item['date'])
                file_name = f"{item['likes']['count']}_{date:%Y-%m-%d-%H-%M-%S}.jpg"
            else:
                photo_set.add(item['likes']['count'])
                file_name =  f"{item['likes']['count']}.jpg"

            photo = {
                'size': i['type'],
                'url': url,
                'file_name': file_name }
            photos.append(photo)  

        return photos


    def get_photo(self):
        METHOD = 'photos.get'
        url = f'{self.url}{METHOD}'
        params = self.photo_params()
        response = requests.get(url, params=params).json()
       
        
        if response.get('error'):
            print(response)
            return

        with open('data.txt', 'w') as file: 
            photos = self._get_biggest_size_photo_url(response['response']['items'])
            json.dump(photos, file, sort_keys = True, indent = 2, ensure_ascii = False)     
        return photos
       



        



