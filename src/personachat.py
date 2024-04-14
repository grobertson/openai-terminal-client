#!/usr/bin/env python3
'''Object to contain the application logic. Nearly everything happens in here, or from here.'''
import os
import glob
import random
import yaml

import click

from .conf import Conf
from .commands import Cmd
from .conversation import Conversation
from .console import center_multiline_string
from .extras import LOGO

class PersonaChat():
    '''Glues all the objects together into an app.'''
    def __init__(self,
                persona='default',
                config=None,
                **kwargs):
        '''Do as little as possible in init -- makes testing easier!'''
        if config:
            #Allow passing in a preloaded configuration instead of initializing it here
            self.config = config
        else:
            self.config = Conf()
        self.config.logger.info('PersonaChat started')
        self.config.personas = None # Will hold list of persona
        self.persona = None # Will hold initialized Persona
        self.conversation = None # Hold the conversation
        self.user_query = None # The user's input
        self._commands = Cmd(self.config)
        self._commands.config = self.config
        self.scan_personas(self.config.persona_path)
        #super().__init__(full_screen=True)
        click.echo(center_multiline_string(random.choice(LOGO)))

    def get_user_input(self, line_prompt):
        '''Wrap input() with a handler for EOF * KeyboardInterrupt'''
        try:
            print(line_prompt, end='')
            return input()
        except (EOFError, KeyboardInterrupt):
            return ".quit"

    def _run(self, **kwargs):
        '''Loop the chat()'''
        if kwargs:
            pass
        self.config.logger.info('Starting the chat loop')
        # A "run" is a Conversation, so init a new one before the loop
        self.conversation = Conversation(self.config)
        while 1:
            line_prompt = '[You] :\t'
            user_input = self.get_user_input(line_prompt)
            if self._commands.is_command(user_input):
                # Handle internal command
                self.config.logger.info(f'Found a command in user_input: {user_input}')
                self.route_command(user_input)
            else:
                resp = self.send(user_input)
                self.config.logger.info(resp.model_dump())
                print(f'\n\n\t\t{resp.choices[0].message.content}\n')

    def route_command(self, cmd):
        '''Dispatch calls to handle user commands'''
        if cmd=='.quit' or cmd=='.exit':
            self._commands.quit()
        if cmd=='.new_conversation':
            print(self._commands.new_conversation())
        if cmd=='.save_conversation':
            print(self._commands.save_conversation())
        if cmd=='.list_conversations':
            print(self._commands.list_conversations())
        if cmd=='.load_conversation':
            print(self._commands.load_conversation())
        if cmd=='.show_persona':
            print(self._commands.show_persona())
        if cmd=='.list_personas':
            print(self._commands.list_personas())
        if cmd=='.load_persona':
            print(self._commands.load_persona())
        if cmd=='.show_context':
            print(self._commands.show_context())
        if cmd=='.help' or cmd=='?':
            print(self._commands.help)
        return None

    def send(self, user_input, **kwargs):
        '''A single roundtrip'''
        if kwargs:
            pass
        # Preproc is the domain of Message, and a Conversation
        # Holds a chain of Message(s)
        # Don't do preprocessing here unless *somehow* it
        # doesn't make sense as a member of Message, or Conversation
        self.config.logger.info('Passing user input to current Conversation')
        self.config.logger.info(f'User Message: {user_input}')
        # Push the user query to the current Conversation to create a new Message instance
        return self.conversation.send(user_input)

    def scan_personas(self, persona_path, **kwargs):
        '''Find all persona files and attempt to load each of them.'''
        self.config.logger.info(f'Scanning for persona files in: {persona_path}')
        if kwargs:
            pass
        personas = []
        for filename in glob.glob(os.path.join(persona_path, f'*.{self.config.persona_extension}')):
            self.config.logger.info(f'Checking Persona file: {filename}')
            try:
                # Attempt to open and parse each file. If it looks valid, add it to the list
                with open(filename, "r", encoding='utf-8') as f:
                    persona = yaml.safe_load(f)
                    if not persona:
                        if self.config.debug:
                            self.config.logger.error(' '.join(
                                ['Invalid persona file detected!: ', filename]))
                    else:
                        disp_name = persona['persona']['display_name']
                        personas.append(persona['persona']['name'])
                        self.config.logger.info(f'Found Persona "{disp_name}" : {filename}')
            except FileNotFoundError:
                pass
        self.config.personas = personas
