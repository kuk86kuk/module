import requests
import base64

class MoySkladBaseClient:
    def __init__(self, login, password, base_url, entity_name, verify_ssl=True):
        self.login = login
        self.password = password
        self.base_url = base_url
        self.entity_name = entity_name
        self.session = requests.Session()
        self.session.verify = verify_ssl  # Управление верификацией SSL

    def _get_auth_header(self):
        credentials = f"{self.login}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        return {"Authorization": f"Basic {encoded_credentials}"}

    def get(self, id=None):
        url = f"{self.base_url}/entity/{self.entity_name}{f'/{id}' if id else ''}"
        response = self.session.get(url, headers=self._get_auth_header())
        self._handle_response(response)
        return response.json()
    
    def post(self, data):
        url = f"{self.base_url}/entity/{self.entity_name}"
        response = self.session.post(url, headers=self._get_auth_header(), json=data)
        self._handle_response(response)
        return response.json()

    def put(self, id, data):
        url = f"{self.base_url}/entity/{self.entity_name}/{id}"
        response = self.session.put(url, headers=self._get_auth_header(), json=data)
        self._handle_response(response)
        return response.json()

    def delete(self, id):
        url = f"{self.base_url}/entity/{self.entity_name}/{id}"
        response = self.session.delete(url, headers=self._get_auth_header())
        self._handle_response(response)
        return True

    def _handle_response(self, response):
        if response.status_code != 200 and response.status_code != 204: # 204 - No Content for DELETE
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")