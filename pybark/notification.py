from apns2.client import APNsClient
from apns2.payload import Payload, PayloadAlert
from apns2.errors import APNsException


class APNs():
    def __init__(self, credentials):
        ...
        self.badge = 0
        self.sound = '1107'
        self.category = 'myNotificationCategory'
        self.mutable_content = True
        self.credentials = credentials
        self.topic = 'me.fin.bark'

    def send(self, title, body, device_token, params):
        payload = Payload(PayloadAlert(
            title=title,
            body=body),
            sound=self.sound, badge=int(params['badge']) if 'badge' in params else self.badge,
            category=self.category, mutable_content=self.mutable_content, custom=params)

        client = APNsClient(self.credentials)
        # 这里可能会发送失败，需要处理失败的结果
        client.send_notification(device_token, payload, self.topic)
