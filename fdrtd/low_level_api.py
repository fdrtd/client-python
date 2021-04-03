from .http_interface import HttpInterface


class LowLevelApi:

    def __init__(self, root):
        self.root = root
        self.http_interface = HttpInterface()

    def post(self, *path, body=None):
        return self.http_interface.post(self._build_url(path), body if body is not None else {})

    def put(self, *path, body=None):
        return self.http_interface.put(self._build_url(path), body if body is not None else {})

    def patch(self, *path, body=None):
        return self.http_interface.patch(self._build_url(path), body if body is not None else {})

    def get(self, *path):
        return self.http_interface.get(self._build_url(path))

    def delete(self, *path):
        return self.http_interface.delete(self._build_url(path))

    def _build_url(self, path):
        url = self.root
        for item in path:
            if item[0] == '/':
                url = url + item
            else:
                url = url + '/' + item
        return url
