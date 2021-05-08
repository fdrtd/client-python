import requests as _requests
import urllib3 as _urllib3
import datetime as _datetime
import logging as _logging


def _human_readable(status):
    return {
        100: 'Continue',
        101: 'Switching Protocols',
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        307: 'Temporary Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Payload Too Large',
        414: 'URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Range Not Satisfiable',
        417: 'Expectation Failed',
        426: 'Upgrade Required',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported'
    }.get(status, 'n/a')


def _WDlogfile960323_line(method="-", uri="-", status="-", comment="-"):
    date = _datetime.date.today().strftime("%Y-%m-%d")
    time = _datetime.datetime.now().strftime("%H:%M:%S")
    return f'{date}\t{time}\t{method}\t{uri}\t{status}\t{_human_readable(status)}\t{comment}'


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
        return HttpInterface._call(_requests.post, url, body, method="POST")

    @staticmethod
    def put(url, body):
        return HttpInterface._call(_requests.put, url, body, method="PUT")

    @staticmethod
    def patch(url, body):
        return HttpInterface._call(_requests.patch, url, body, method="PATCH")

    @staticmethod
    def get(url):
        return HttpInterface._call(_requests.get, url, method="GET")

    @staticmethod
    def delete(url):
        return HttpInterface._call(_requests.delete, url, method="DELETE")

    @staticmethod
    def _call(hook, url, body=None, method="-"):

        _logging.getLogger(__name__).debug(f'Sending request: {method} {url} {body}')
        response = hook(url=url, json=body, verify=HttpInterface.ssl_verify)
        _logging.getLogger(__name__).debug(f'Receiving response: {response.status_code} {response.text}')

        if response.status_code not in [200, 201, 202, 204]:
            message = _WDlogfile960323_line(method, url, response.status_code, response.text)
            _logging.getLogger(__name__).error(message)
            raise Exception(message)

        message = _WDlogfile960323_line(method, url, response.status_code)
        _logging.getLogger(__name__).info(message)
        return None if response.text == '' else response.json()
