
import logging
import requests

from time import sleep


def max_px_img(photo: dict):
    max_copy_img = max(photo['sizes'],
                       key=lambda size: size['height'] * size['width'])
    return max_copy_img['height'] * max_copy_img['width']


class VK:
    url ='https://api.vk.com/method/'
    def __init__(self, token, version='5.131'):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos(self, owner_id: str):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id': owner_id,
            'album_id': 'saved'
        }
        response = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        return response['response']

    def get_all_photos(self, owner_id: int, extended=None, offset=0, count=None):
        get_allphotos_url = self.url + 'photos.getAll'
        get_allphotos_params = {
            'owner_id': owner_id,
            'extended': extended,
            'offset': offset,
            'count': count,
            'photo_sizes': 1,
            'no_service_albums': 0
        }
        response = requests.get(get_allphotos_url, params={**self.params, **get_allphotos_params}).json()
        return response['response']

    def get_full_list(self, owner_id: int):
        all_photos_list = []
        count = self.get_all_photos(owner_id=owner_id,
                                   extended=0,
                                   offset=0,
                                   count=0)['count']
        offset = 0
        logging.info('Getting a list of photos')
        sleep(0.5)
        while count - offset >= 0:
            res = self.get_all_photos(owner_id=owner_id,
                                     extended=1,
                                     offset=offset,
                                     count=200)['items']
            all_photos_list.extend(res)
            offset += 200
            sleep(0.5)
        logging.info(f'Received {len(all_photos_list)} objects')
        return all_photos_list


