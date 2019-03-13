import falcon
import os
from apns2.errors import APNsException

from models import Database
from notification import APNs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite')
CERT_PATH = os.path.join(BASE_DIR, 'cert-20200229.pem')


class RequireJSON(object):
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                '此API仅支持编码为JSON的响应。',
                href='https://github.com/billzhong/py-bark')


class PingResource(object):
    def on_get(self, req, resp):
        resp.media = {
            'code': 200,
            'data': {
                'version': '1.0.0'
            },
            'message': 'pong'
        }


class RegisterResource(object):
    def __init__(self, _db):
        self.db = _db

    def on_get(self, req, resp):
        device_token = req.get_param('devicetoken')

        if not device_token:
            resp.media = {
                'code': 400,
                'data': None,
                'message': 'deviceToken 不能为空',
            }
            resp.status = falcon.HTTP_400
            return

        key = self.db.save_key(device_token, req.get_param('key'))

        if key:
            resp.media = {
                'code': 200,
                'data': {
                    'key': key
                },
                'message': '注册成功'
            }
        else:
            resp.media = {
                'code': 400,
                'data': None,
                'message': '注册失败',
            }
            resp.status = falcon.HTTP_400
            return


class IndexResource(object):
    def __init__(self, _db):
        self.db = _db
        self.apn = APNs(CERT_PATH)

    def on_get(self, req, resp, key, **kwargs):

        device_token = self.db.get_token(key)

        if not device_token:
            resp.media = {
                'code': 400,
                'data': None,
                'message': '找不到 Key 对应的 DeviceToken, 请确保 Key 正确! Key 可在 App 端注册获得。',
            }
            resp.status = falcon.HTTP_400
            return

        is_send = False

        if 'title' in kwargs:
            title = kwargs['title']
            is_send = True
        else:
            title = ''

        if 'body' in kwargs:
            body = kwargs['body']
            is_send = True
        else:
            body = ''

        # url中不包含 title body，或许可以从Form获取，现在让我们直接取消发送消息
        if not is_send:
            resp.media = {
                'code': 400,
                'data': None,
                'message': '标题和内容都为空，没有消息发送！',
            }
            # 这里返回的code和状态码，或许可以改成其他的
            resp.status = falcon.HTTP_400
            return

        if not body:
            body = '无推送文字内容'

        try:
            # 需要把参数转换为小写
            params = {k.lower(): v for k, v in req.params.items()}
            # print(title, body, device_token, params)
            self.apn.send(title, body, device_token, params)
            resp.media = {
                'code': 200,
                'data': {'title': title, 'body': body, 'params': params},
                'message': '发送成功！',
            }
        except APNsException as e:
            resp.media = {
                'code': 400,
                'data': None,
                'message': str(e),
            }
            resp.status = falcon.HTTP_400

    def on_post(self, req, resp, key, **kwargs):
        pass


def create_app(db_store):
    api = falcon.API(middleware=[
        RequireJSON(),
    ])

    ping = PingResource()
    register = RegisterResource(db_store)
    index = IndexResource(db_store)

    api.add_route('/ping', ping)
    api.add_route('/register', register)
    api.add_route('/{key}', index)
    api.add_route('/{key}/{title}', index)
    api.add_route('/{key}/{title}/{body}', index)
    return api


def get_app():
    # print(DB_PATH)
    db_store = Database(DB_PATH)
    return create_app(db_store)


if __name__ == '__main__':
    from wsgiref import simple_server
    from ilds.net import get_host_ip

    port = 8000
    print(f'访问地址: http://{get_host_ip()}:{port}')
    httpd = simple_server.make_server('0.0.0.0', port, get_app())
    httpd.serve_forever()
