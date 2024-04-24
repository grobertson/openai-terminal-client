#!/usr/bin/env python3
'''Object to contain the application logic. Nearly everything happens in here, or from here.'''
import random

import click
from colored import Fore, Style
from loguru import logger
from pprint import pprint

from .config import Settings
from .commands import Cmd
from .conversation import Conversation
from .console import center_multiline_string, colorize_chat
from .extras import LOGO

class PersonaChat():
    '''Glues all the objects together into an app.'''

    LINE_PROMPT = f'{Fore.BLUE}[{Fore.WHITE}You{Fore.BLUE}] {Fore.WHITE}:{Style.RESET}\n'
    _instance = None 
    
    def __init__(self,
                config=None):
        '''Do as little as possible in init -- makes testing easier!'''
        if config:
            #Allow passing in a preloaded configuration instead of initializing it here
            self.config = config
        else:
            self.config = Settings()
        logger.info('PersonaChat started')
        self.persona = None # Will hold initialized Persona
        self.conversation = None # Hold the conversation
        self.user_query = None # The user's last input
        self._commands = Cmd()
        disp_logo = center_multiline_string(random.choice(LOGO))
        disp_logo = f'{Fore.BLUE}{disp_logo}{Style.RESET}'
        if self.config.splash:
            click.echo(disp_logo)

    def __new__(cls, config=None):
        if cls._instance is None:
            cls._instance = super(PersonaChat, cls).__new__(cls)
        return cls._instance

    def get_user_input(self, line_prompt):
        '''Wrap input() with a handler for EOF * KeyboardInterrupt'''
        try:
            print(line_prompt, end='')
            return input()
        except (EOFError, KeyboardInterrupt):
            return ".quit"

    def run_once(self, user_input) -> object:
        '''A single roundtrip'''
        logger.info('Starting a single roundtrip')
        self.conversation = Conversation(self.config)
        resp = self.conversation.send(user_input)
        if self.config.debug:
            logger.info(resp.model_dump())
        return resp

    def run(self, **kwargs) -> None:
        '''Loop the chat()'''
        if kwargs:
            pass
        logger.info('Starting the chat loop')
        # A "run" is a Conversation, so init a new one before the loop
        self.conversation = Conversation()
        while 1:
            user_input = self.get_user_input(line_prompt=self.LINE_PROMPT)
            if not self._commands.dispatch_or_false(cmd=user_input):
                resp = self.send(user_input=user_input)
                if resp is not None:
                    logger.debug(resp.model_dump())
                assistant_visible_prompt = f'{Fore.WHITE}--{Fore.BLUE}[{Fore.GREEN}'
                assistant_visible_prompt += f'{ self.config.persona.character.given_name }'
                assistant_visible_prompt += f'{Fore.BLUE}]{Fore.WHITE}--- :{Style.RESET}'
                if resp is not None:
                    colorized_response_text = colorize_chat(resp.choices[0].message.content)
                    pprint(f'\n{assistant_visible_prompt}\n{ colorized_response_text }\n')
                else:
                    click.echo('Error: API response is None')

    def send(self, user_input, **kwargs):
        '''Send the user input to the current Conversation'''
        if kwargs:
            pass
        # Preproc is the domain of Message, and a Conversation
        # Holds a chain of Message(s)
        # Don't do preprocessing here unless *somehow* it
        # doesn't make sense as a member of Message, or Conversation
        logger.info('Passing user input to current Conversation')
        logger.info(f'User Message: {user_input}')
        # Push the user query to the current Conversation to create a new Message instance
        return self.conversation.send(user_input)
