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
from .message import Message

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

    def clean_data(self, data, **kwargs):
        '''Remove common junk from response before using'''
        if kwargs:
            pass
        strip='<|im_end|>'
        data = data.replace(strip, '')
        strip = f'### {self.config.persona}: '
        data = data.replace(strip, '')
        return data

    def create_message(self, user_input=None, **kwargs):
        '''Assemble the completion request'''
        if kwargs:
            pass
        message=Message(self.config, user_input)
        return message

    def send(self, user_input):
        '''Wrap the api call for completion'''
        self.config.logger.info(f'Raw user_input : {user_input}')
        #
        # Post-user pre-request manipulation should happen here.
        #
        messages = self.create_message(user_input)
        resp = self.request_completion(messages)
        if self.config.debug:
            self.config.logger.info(resp)
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
                click.echo('Error: No messages to send')
                self.config.logger.error('Error: No messages to send')
                return None
            completion = self._client.chat.completions.create(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": messages.system},
                    {"role": "assistant", "content": messages.assistant},
                    {"role": "user", "content": messages.user}
                ],
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
        except APIError:
            click.echo('Error: Generic API error')
            self.config.logger.error('Error: Generic API error')
            completion = None
        return completion
