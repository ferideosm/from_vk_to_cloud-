from vk import VK
from ya import Ya
import pathlib
from pathlib import Path
import requests


version_vk = '5.131'

def get_token_vk():
    path = Path(pathlib.Path.cwd(), 'tokens.txt')
    with open(path, 'r', encoding='utf-8') as file:
        for token in file:
            if token.find('token_vk') != -1:
                return file.readline().replace("\n","")


def get_token_ya():
    path = Path(pathlib.Path.cwd(), 'tokens.txt')
    i = 0
    with open(path, 'r', encoding='utf-8') as file:
        for token in file:
            if token.find('token_ya') != -1:
                return file.readline().replace("\n","")

if __name__ == "__main__":
    
    token_vk = get_token_vk() 
    token_ya = get_token_ya()    

    vk = VK(token_vk, version_vk)
    ya = Ya(token_ya)
    photos = vk.get_photo()
    if photos:
        ya.upload(photos, 'New folder')    

        
