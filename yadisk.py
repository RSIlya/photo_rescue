
import  requests

class YaUploader:
    url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth ' + self.token
        }

    def _get_upload_link(self, file_path: str):
        upload_url = self.url + 'resources/upload'
        params = {
            'path': file_path,
            'overwrite': 'true'
        }
        response = requests.get(upload_url, headers=self.headers, params=params).json()
        return response['href']

    def get_upload(self, file_path: str, remote_path=None, file_name=None):
        """Метод загружает файл на яндекс диск"""
        if file_name is None:
            file_name = file_path.rsplit('/', 1)[-1]
        href =  self._get_upload_link(remote_path + '/' + file_name)
        with open(file_path, 'rb') as file:
            response = requests.put(href, data=file)
        return response

    def post_upload(self, sourse_url: str, remote_path: str=None):
        """ """
        upload_url = self.url + 'resources/upload'
        params = {
           'path': remote_path,
           'url': sourse_url
        }
        response = requests.post(upload_url, headers=self.headers, params=params, timeout=10)
        return response

    def create_directory(self, path: str):
        """ """
        create_url = self.url + 'resources'
        params = {
            'path': path
        }
        response = requests.put(create_url, params=params, headers=self.headers, timeout=10)
        return response

