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
import copy

from openai import OpenAI
from openai import APIConnectionError, APIError, APIStatusError, APITimeoutError
from loguru import logger
import click
from .message import Message
from .config import Settings

class Conversation():
    '''Represent the completion request message as an object'''

    _instance = None

    def __init__(self, **kwargs):
        '''Message() Init'''
        if kwargs:
            pass
        self.config = Settings()
        self._client = OpenAI(base_url=self.config.base_url, api_key=self.config.api_key)
        self._context = ''
        self._assistant = ''
        self._user = ''
        self._system = ''
        self._messages = []
        self.current_message = None
        if self.config.logging:
            logger.info('Conversation started.')

    def __new__(cls, config=None):
        '''Singleton pattern for Conversation'''
        if cls._instance is None:
            cls._instance = super(Conversation, cls).__new__(cls)
        return cls._instance

    def clean_data(self, data, **kwargs) -> str:
        '''Remove common junk from response before using'''
        if kwargs:
            pass
        strip='<|im_end|>'
        data = data.replace(strip, '')
        strip = f'###{self.config.persona}:'
        data = data.replace(strip, '')
        return data

    def create_message(self, user_input=None, **kwargs) -> object:
        '''Assemble the completion request'''
        if kwargs:
            pass
        message=Message(config=self.config, user_input=user_input, context=self._context)
        self._messages.append(copy.copy(message))
        return message

    def reset_context(self, **kwargs) -> None:
        '''Reset the context'''
        if kwargs:
            pass
        self._context = ''
        self._assistant = ''
        self._user = ''
        self._system = ''
        self._messages = []
        self.current_message = None
        click.echo('Context reset.')

    def send(self, user_input) -> object:
        '''Wrap the api call for completion'''
        logger.info(f'Raw user_input : {user_input}')
        #
        # Post-user pre-request manipulation should happen here.
        #
        messages = self.create_message(user_input)
        self.current_message = messages
        resp = self.request_completion(messages)
        try:
            self._context += f'\n#{ self.config.persona.user }: { user_input }\n'
            self._context += f'\n#{ self.config.persona.character.given_name }: { resp.choices[0].message.content }'
        except AttributeError:
            logger.error('Error: API response is None')
            logger.error(f'{resp}')
            return None
        if self.config.debug:
            logger.info(resp)
        #
        # Post-response pre-users manipulation should happen here
        #
        return resp

    def request_completion(self, messages=None, **kwargs) -> object:
        '''Make api request to get next response'''
        if kwargs:
            pass
        logger.info('Called Conversation-request_completion()')
        try:
            if messages is None:
                click.echo('Error: No messages to send')
                logger.error('Error: No messages to send')
                return None
            completion = self._client.chat.completions.create(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": messages.system},
                    {"role": "assistant", "content": messages.assistant},
                    {"role": "user", "content": messages.user}
                ],
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                n=self.config.n,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
                stop=self.config.stop,
                max_tokens=self.config.max_tokens,
                )
        except APITimeoutError as error:
            click.echo('Timeout while making API request')
            logger.error('Timeout while making API request')
            print(error)
            completion = None
        except APIConnectionError as error:
            click.echo('Error: Connection error during API request')
            logger.error('Error: Connection error during API request')
            print(error)
            completion = None
        except APIStatusError as error:
            click.echo('Error: API returned a status error')
            logger.error('Error: API returned a status error')
            print(error)
            completion = None
        except APIError as error:
            click.echo('Error: Generic API error')
            logger.error('Error: Generic API error')
            print(error)
            completion = None
        return completion
