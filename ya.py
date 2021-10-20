from os import pardir
import requests
import json
import time
from progress.bar import IncrementalBar
import json
from datetime import datetime

class Ya():

    def __init__(self, token):
        self.token = token
        self.url = 'https://cloud-api.yandex.net'

    def _get_headers(self):
        return {
            'Authorization': f'OAuth {self.token}',
            'Accept': 'application/json'
        }

    def _create_new_folder(self, folder_name):
        headers = self._get_headers()
        url = f'{self.url}/v1/disk/resources'
        params={'path': folder_name}
        res = requests.put(url, headers=headers, params=params)

        if res.status_code == 201:
            print("Folder created on Yandex Disk!")
            return res.status_code
        elif res.status_code == 409:
            print("Folder exists on Yandex Disk!")
            return res.status_code
        else:
            print(res.text)
            return

    def upload(self, photos, folder_name):
        folder = self._create_new_folder(folder_name)
        check_log = False       

        if folder:
            headers = self._get_headers()
            url = f'{self.url}/v1/disk/resources/upload'
            bar = IncrementalBar('Upload to Yandex', max = len(photos))

            with open('log.txt', 'a') as file:
                for photo in photos:
                    time.sleep(2)
                    params = {
                        'path': f"{folder_name}/{photo['file_name']}",
                        'url': photo['url']
                        }
                    response = requests.post(url, headers=headers, params=params)  
                    date = datetime.now()
                    if response.status_code == 202:                                      
                        del photo['url']                        
                        photo['upload_datetime'] = date.strftime('%Y-%d-%m %H:%M:%S')
                        photo['to'] = 'ya_disk'  
                        bar.next()       
                        json.dump(photo, file, sort_keys = True, indent = 2, ensure_ascii = False)
                    else:
                        photo['error'] = response.text
                        photo['upload_datetime'] = date.strftime('%Y-%d-%m %H:%M:%S')                        
                        photo['to'] = 'ya_disk'  
                        check_log = True          
                    json.dump(photo, file, sort_keys = True, indent = 2, ensure_ascii = False)

            bar.finish()
            if check_log:
                print("Please, check log. The operation ended with an errors")

