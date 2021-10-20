from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import json
import traceback
import sys
from progress.bar import IncrementalBar
import time


# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

class Ggle():

    def main(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        # service = build('drive', 'v3', credentials=creds)

        return build('drive', 'v3', credentials=creds)


    def get_all_files(self):
        service = self.main()
        results = service.files().list(pageSize=100, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))


    def create_folder(self, folder_name):
        service = self.main()

        find_folder = False
        page_token = None
        response = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)').execute()

        for folder in response.get('files', []):
            if folder.get('name') == folder_name:
                find_folder = True   
                print("Folder exists on Google Drive!")         
                return folder.get('id')
          
        if not find_folder:            
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
                }
            folder = service.files().create(body=file_metadata, fields='id, name').execute()      
            print("Folder created on Google Drive!") 
            return folder.get('id')


    def get_local_photos(self):
        path = 'Files' 
        photos_names = os.listdir(path)       
        photos = [os.path.join(path, f) for f in os.listdir(path)]   
        return zip(photos_names, photos), len(photos_names)


    def upload_photos(self, folder_name):
        service = self.main()
        folder_id = self.create_folder(folder_name)
        check_log = False
        date = datetime.now()
        photos, len_photos = self.get_local_photos()
        bar = IncrementalBar('Upload to Google', max = len_photos)

        with open('log.txt', 'a') as file_:   
            for photo in photos:   
                time.sleep(2)    
                photo_logs = {}
                try:
                    file_metadata = {'name': photo[0],
                                    'parents': [folder_id]
                                    }
                    media = MediaFileUpload(photo[1], mimetype='image/jpeg')
                    file = service.files().create(body=file_metadata,
                                                        media_body=media,
                                                        fields='id').execute()  
                    
                    photo_logs = {
                        'path': photo[1],
                        'file_name': photo[0],
                        'upload_datetime': date.strftime('%Y-%d-%m %H:%M:%S'),
                        'to': 'google cloud' }
       
                    bar.next()    
                    json.dump(photo_logs, file_, sort_keys = True, indent = 2, ensure_ascii = False)
                    bar.next()       

                except Exception as e:
                    exc_info = sys.exc_info()

                    photo_logs = {
                        'path': photo[1],
                        'file_name': photo[0],
                        'upload_datetime': date.strftime('%Y-%d-%m %H:%M:%S'),
                        'to': 'google cloud',
                        'error': ''.join(traceback.format_exception(*exc_info))}

                    check_log = True          
                    json.dump(photo_logs, file_, sort_keys = True, indent = 2, ensure_ascii = False)
                    pass

        bar.finish()
        if check_log:
            print("Please, check log. The operation ended with an errors")

