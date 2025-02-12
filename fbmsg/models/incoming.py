import requests

class Types:
    TEXT_MESSAGE = 1
    POSTBACK_MESSAGE = 2
    REFERRAL_MESSAGE = 3


class Request(object):
    def __init__(self, object: str, entry: list, *args, **kwargs):
        if not isinstance(object, str):
            raise TypeError('obj must be an instance of str')
        if not isinstance(entry, list):
            raise TypeError('entry must be an instance of list')
        if len(entry) == 0:
            raise ValueError('empty entry list')
        self.object = object
        self.entries = []
        for entry in entry:
            self.entries.append(Entry(**entry))


class Entry(object):
    def __init__(self, id: str, time: int, messaging: list, *args, **kwargs):
        if not isinstance(id, str):
            raise TypeError('id must be an instance of str')
        if not isinstance(time, int):
            raise TypeError('time must be an instance of list')
        if not isinstance(messaging, list):
            raise TypeError('messaging must be an instance of list')
        if not len(messaging) == 1:
            raise ValueError('messaging list must contain only one element')
        self.id = id
        self.time = time
        for message in messaging:
            self.message = Message(**message)


class Referral(object):
    def __init__(self, *args, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])


class Message(object):
    def __init__(self, sender: dict, recipient: dict, timestamp: int, message: dict = None, postback: dict = None,
                 referral: dict = None, attachments: list = None, *args, **kwargs):
        if not isinstance(sender, dict):
            raise TypeError('sender must be an instance of dict')
        if not isinstance(recipient, dict):
            raise TypeError('recipient must be an instance of dict')
        if not isinstance(timestamp, int):
            raise TypeError('timestamp must be an instance of int')
        self.type = Types.TEXT_MESSAGE
        self.attachment = None
        if referral:
            if not isinstance(referral, dict):
                raise TypeError('referral must be an instance of dict')
            self.referral = Referral(**referral)
            self.type = Types.REFERRAL_MESSAGE
        if message:
            if not isinstance(message, dict):
                raise TypeError('message must be an instance of dict')
            self.mid = message.get('mid')
            self.text = message.get('text')
            self.seq = message.get('seq')
            quick_reply = message.get('quick_reply')
            if quick_reply is not None:
                self.payload = quick_reply.get('payload')
                self.type = Types.POSTBACK_MESSAGE
        if postback:
            if not isinstance(postback, dict):
                raise TypeError('postback must be an instance of dict')
            self.type = Types.POSTBACK_MESSAGE
            self.text = postback.get('title')
            self.payload = postback.get('payload')
            self.referral = postback.get('referral')
        if attachments:
            for att in attachments:
                if att['type'] == 'image':
                    self.attachment = requests.get(att['payload']['url'])
                    break
        self.sender_id = sender['id']
        self.recipient_id = recipient['id']
        self.timestamp = timestamp
