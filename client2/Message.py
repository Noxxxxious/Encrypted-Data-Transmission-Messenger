import json


class Message:
    def __init__(self, text, msg_type, cipher_type=None):
        self.text = text
        self.msg_type = msg_type
        self.cipher_type = cipher_type

    def to_json(self):
        return json.dumps({
            'text': self.text,
            'msg_type': self.msg_type,
            'cipher_type': self.cipher_type
        })

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        return cls(data['text'], data['msg_type'], data['cipher_type'])
