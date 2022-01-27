
import logging
import time
import json
import vk
import yadisk

from progress.bar import Bar


def get_url(photo: dict):
    max_copy_img = max(photo['sizes'],
                       key=lambda size: size['height'] * size['width'])
    return max_copy_img['url']


def get_size(photo: dict):
    max_copy_img = max(photo['sizes'],
                       key=lambda size: size['height'] * size['width'])
    return max_copy_img['type']


def get_likes(photo: dict):
    return str(photo['likes']['count'])


def get_date(photo: dict):
    return time.strftime('%d_%B_%Y_%H.%M.%S', time.gmtime(photo['date']))


def upload_from_vk(photos_list: list, token: str, number=5):
    files_list = []
    path = '/photo_from_VK'
    storage = yadisk.YaUploader(token)
    storage.create_directory(path)
    suffix = '%(index)d/%(max)d [%(elapsed)d / %(eta)d / %(eta_td)s]'
    bar = Bar('Сopying files to YandexDisk', suffix=suffix)
    for item in bar.iter(range(number)):
        photo = photos_list[item]
        file_name = get_likes(photo) + '.jpg'
        if file_name in [file['file_name'] for file in files_list]:
            file = {
                'file_name': get_date(photo) + '.jpg',
                'size': get_size(photo)
            }
        else:
            file = {
                'file_name': file_name,
                'size': get_size(photo)
            }
        url = get_url(photo)
        storage.post_upload(sourse_url=url, remote_path=path + '/' + file['file_name'])
        files_list.append(file)
        time.sleep(0.5)
    logging.info('Copying was successful')
    return files_list

def main(vk_id: int, vk_token: str, ydisk_token: str):
    user = vk.VK(vk_token)
    photos_list = user.get_full_list(vk_id)
    photos_list.sort(key=vk.max_px_img, reverse=True)
    files_json = upload_from_vk(photos_list, token=ydisk_token, number=10)
    with open('photo_vk.json', 'w') as f:
        json.dump(files_json, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    vk_user_id =
    vk_token = ''
    YaDisk_token = ''
    logging.basicConfig(level=logging.INFO)
    main(vk_user_id, vk_token, YaDisk_token)
