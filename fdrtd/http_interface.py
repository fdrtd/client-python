import json as _json
import requests as _requests
import urllib3 as _urllib3


class HttpInterface:

    # enable the following line if e.g. SSL verification fails on localhost
    _urllib3.disable_warnings(category=_urllib3.exceptions.InsecureRequestWarning)

    # enable the following line if SSL verification fails on Android devices
    _urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:" \
                                         "TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT "

    # set to False to disable, set to True to enable SSL verification
    ssl_verify = False

    @staticmethod
    def post(url, body):
        return HttpInterface._call(_requests.post, url, body)

    @staticmethod
    def put(url, body):
        return HttpInterface._call(_requests.put, url, body)

    @staticmethod
    def patch(url, body):
        return HttpInterface._call(_requests.patch, url, body)

    @staticmethod
    def get(url):
        return HttpInterface._call(_requests.get, url)

    @staticmethod
    def delete(url):
        return HttpInterface._call(_requests.delete, url)

    @staticmethod
    def _call(hook, url, body=None):

        if body is None:
            response = hook(url=url, verify=HttpInterface.ssl_verify)
        else:
            response = hook(url=url, json=body, verify=HttpInterface.ssl_verify)

        if response.status_code == 400:
            raise Exception("HTTP error code 400 (bad request): {}".format(url))
        if response.status_code == 403:
            raise Exception("HTTP error code 403 (forbidden): {}".format(url))
        if response.status_code == 404:
            raise Exception("HTTP error code 404 (not found): {}".format(url))
        if response.status_code == 405:
            raise Exception("HTTP error code 405 (not allowed): {}".format(url))
        if response.status_code == 500:
            raise Exception("HTTP error code 500 (server error): {} {}".format(url, response.text))
        if response.status_code == 501:
            raise Exception("HTTP error code 501 (not implemented): {}".format(url))
        if response.status_code == 502:
            raise Exception("HTTP error code 502 (bad gateway): {}".format(url))
        if response.status_code != 200 and response.status_code != 201 and response.status_code != 202 and response.status_code != 204:
            raise Exception("HTTP status code {}: {}".format(response.status_code, url))
        if response.status_code == 202:
            return {}
        if response.status_code == 204:
            return {}

        try:
            ret = response.json()
        except:
            return None

        if isinstance(ret, str):
            if ret == '':
                return None
            if ret[0] == '{':
                return _json.loads(ret)
            if ret[0] == '\"':
                return ret[1:-1]
            if ret[0] == '\'':
                return ret[1:-1]
        return ret
