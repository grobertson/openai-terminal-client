#!/usr/bin/env python3
'''Represent a conversation as an object'''
# The concept is:
# PersonaChat() <-- Application
#   - Config()
#       - Persona()
#   - Conversation(config)
#       - Message(config) <- Each represents one request->api-response

import copy

from jinja2 import Environment
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
        self._context = ''
        self._assistant = ''
        self._user = ''
        self._system = ''
        self._messages = []
        self._environment = Environment()
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
        #data = data.replace(data, '')
        return data

    def create_completion_request(self, user_input=None, **kwargs) -> object:
        '''Assemble the completion request'''
        if kwargs:
            pass
        message=Message(config=self.config, user_input=user_input, context=self._context)
        self._messages.append(copy.copy(message))
        return message

    @property
    def get_context(self) -> str:
        '''Return the context data'''
        return self._context

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

    def _render_from_string(self, template_str):
        '''Render template from a string - used for second pass rendering'''
        # Second pass - render template tags inserted from the first pass
        template = self._environment.from_string(template_str)
        # user_input and context are already rendered in the first pass
        result = template.render(
            persona=self.config.persona
        )
        return result

    def send(self, user_input, persona) -> object:
        '''Wrap the api call for completion'''
        logger.info(f'Raw user_input : {user_input}')
        #
        # Post-user pre-request manipulation should happen here.
        #
        messages = self.create_completion_request(user_input)
        self.current_message = messages
        resp = self.request_completion(messages)
        try:
            self._context += self._render_from_string(
                f'\n#{ persona.user }: { user_input }\n')
            self._context += self._render_from_string(
                f'\n#{ persona.character.given_name }:')
            self._context += f'{ resp.choices[0].message.content }\n'
        except:
            pass
            #logger.error(f'Error: API response is {error}')
            #logger.error(f'{resp}')
            #return None
        if self.config.debug:
            logger.info(resp)
        #
        # Post-response pre-users manipulation should happen herea
        #
        return resp

    def request_completion(self, message=None, **kwargs) -> object:
        '''Make api request to get next response'''
        if kwargs:
            pass
        logger.info('Called Conversation-request_completion()')
        try:
            if message is None:
                click.echo('Error: No messages to send')
                logger.error('Error: No messages to send')
                return None
            messages=[
                    {"role": "system", "content": message.system},
                    {"role": "assistant", "content": message.assistant},
                    {"role": "user", "content": message.user}
                ]
            logger.debug(f'model={self.config.model_name}')
            logger.debug(f'messages: {messages}')
            logger.debug(f'temperature={self.config.temperature}')
            logger.debug(f'top_p={self.config.top_p}')
            logger.debug(f'n={self.config.n}')
            logger.debug(f'frequency_penalty={self.config.frequency_penalty}')
            logger.debug(f'presence_penalty={self.config.presence_penalty}')
            logger.debug(f'max_tokens={self.config.max_tokens}')
            completion = self.config.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                n=self.config.n,
                frequency_penalty=self.config.frequency_penalty
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
