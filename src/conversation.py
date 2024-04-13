'''Represent the completion request message as an object'''

import time

class Conversation():
    '''Represent the completion request message as an object'''

    def __init__(self, **kwargs):
        '''Message() Init'''
        if kwargs:
            pass
        self.assistant = ''
        self.user = ''
        self.system = ''

    @property
    def get_message(self, **kwargs):
        '''Return a completion request message, a list of objects'''
        if kwargs:
            pass
        return self.build_message()

    def build_message(self, **kwargs):
        '''Assemble the completion request'''
        if kwargs:
            pass
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "assistant", "content": ASSISTANT},
            {"role": "user", "content": USERMSG}
        ]
        return messages

    class Message():
        '''a simple Message object'''
        def __init__(self, **kwargs):
            '''Message() Init'''
            self.timestamp = time.time()
            if kwargs:
                pass
            self.assistant = ''
            self.user = ''
            self.system = ''