#!/usr/bin/env python3
'''Represent a conversation as an object'''
# The concept is:
# PersonaChat() <-- Application
#   - Config()
#       - Persona()
#   - Conversation(config)
#       - Message(config) <- Each represents one request->api-response

import os
from datetime import datetime

from openai import OpenAI
from openai import APIConnectionError, APIError, APIStatusError, APITimeoutError
import click

class Conversation():
    '''Represent the completion request message as an object'''

    def __init__(self, config, **kwargs):
        '''Message() Init'''
        if kwargs:
            pass
        self.config = config
        self.config.set_persona(self.config.persona_default)
        self._client = OpenAI(base_url=self.config.base_url, api_key=self.config.api_key)
        self._assistant = ''
        self._user = ''
        self._system = ''
        if self.config.logging:
            self.config.logger.info('Conversation started.')

    #@property
    #def messages(self, **kwargs):
    #    '''Return a completion request message, a list of objects'''
    #    if kwargs:
    #        pass
    #    return self.create_message()

    def clean_data(self, data, **kwargs):
        '''Remove common junk from response before using'''
        if kwargs:
            pass
        strip='<|im_end|>'
        data = data.replace(strip, '')
        strip = f'### {CHARACTER}: '
        data = data.replace(strip, '')
        return data

    def create_message(self, user_input=None, **kwargs):
        '''Assemble the completion request'''
        if kwargs:
            pass
        messages=[
            {"role": "system", "content": self._system},
            {"role": "assistant", "content": self._assistant},
            {"role": "user", "content": user_input}
        ]
        return messages

    def send(self, user_input):
        '''Wrap the api call for completion'''
        self.config.logger.info(f'user_input : {user_input}')
        #
        # Post-user pre-request manipulation should happen here.
        #
        messages = self.create_message(user_input)
        resp = self.request_completion(messages)
        #
        # Post-response pre-user manipulation should happen here
        #
        return resp

    def request_completion(self, messages=None, **kwargs):
        '''Make api request to get next response'''
        if kwargs:
            pass
        self.config.logger.info('Called Conversation-request_completion()')
        try:
            if messages is None:
                messages = self.create_message()
            completion = self._client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                )
        except APITimeoutError:
            click.echo('Timeout while making API request')
            self.config.logger.error('Timeout while making API request')
            completion = None
        except APIConnectionError:
            click.echo('Error: Connection error during API request')
            self.config.logger.error('Error: Connection error during API request')
            completion = None
        #except APIError:
        #    click.echo('Error: Generic API error')
        #    self.config.logger.error('Error: Generic API error')
        #    completion = None
        return completion

    class Message():
        '''Stores and renders the three message components used to request completion'''
        def __init__(self, config, **kwargs):
            '''Message() Init'''
            self.config = config           
            self.config.logger.info('New Message instance')
            # log the time the Message was created
            self.timestamp = time.time()
            if kwargs:
                pass
            self._assistant = None
            self._user = None
            self._system = None
            self._completion = None

        @property
        def assistant(self):
            '''Renders the current assistant message using template'''
            self.config.logger.info(self._assistant)
            return self._assistant

        @property
        def system(self):
            '''Renders the current system message using template'''
            self.config.logger.info(self._assistant)
            return self._system

        @property
        def user(self):
            '''Renders the current user message using template'''
            self.config.logger.info(self._assistant)
            return self._user
