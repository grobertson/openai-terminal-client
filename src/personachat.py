#!/usr/bin/env python3
'''Object to contain the application logic. Nearly everything happens in here, or from here.'''
import os
import glob
import yaml

from openai import OpenAI
import click

from .conf import Conf
from .persona import Persona
from .conversation import Conversation

class PersonaChat():
    '''Object to contain the application logic. Nearly everything happens in here, or from here.'''
    def __init__(self, persona='default'):
        '''Do as little as possible in init -- makes testing easier!'''
        self.config = Conf()
        self.client = OpenAI(base_url=self.base_url, api_key=self.config.api_key)
        self.personas = None # Will hold list of persona
        self.persona = None # Will hold initialized Persona
        self.conversation = None # Hold the conversation
        self.user_query = None # The user's input
        self.scan_personas(self.config.persona_path)

    def run(self, **kwargs):
        '''Loop the chat()'''
        if kwargs:
            pass
        # A "run" is a Conversation, so init a new one before the loop
        self.conversation = Conversation(self.config, self.persona)
        while 1:
            click.echo('[You]:\t', nl=False)
            self.user_query = input()
            self.chat()
            #click.echo(f'[{CHARACTER}]:\t{response}')

    def chat(self, **kwargs):
        '''A single roundtrip'''
        if kwargs:
            pass
        completion = self.request_completion()
        response = completion.choices[0].message
        response = self.clean_data(response.content)

    def request_completion(self, **kwargs):
        '''Make api request to get next response'''
        if kwargs:
            pass
        #messages = self.build_message()
        req = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.config.max_tokens,
                )
        return req

    def scan_personas(self, persona_path, **kwargs):
        '''Find all persona files and attempt to load each of them.'''
        if kwargs:
            pass
        personas = []
        for filename in glob.glob(os.path.join(persona_path, f'*.{self.config.persona_extension}')):
            try:
                '''Attempt to open and parse each file. If it looks valid, add it to the list'''
                with open(filename, "r", encoding='utf-8') as f:
                    persona = yaml.safe_load(f)
                    if not persona:
                        if self.config.debug:
                            click.echo(' '.join(['Invalid persona file detected!: ', filename]))
                    else:
                        personas.append((persona['persona']['display_name'], persona['persona']['name']))
            except FileNotFoundError:
                pass
        self.personas = personas

    def load_persona(self, name='default'):
        '''Load/reload a persona into the application'''
        self.config.persona_name = name
        self.config.persona = Persona(config=self.config)

    def clean_data(self, data, **kwargs):
        '''Remove common junk from response before using'''
        if kwargs:
            pass
        # TODO Validation
        # Strip <|im_end|>
        strip='<|im_end|>'
        data = data.replace(strip, '')
        strip = f'### {CHARACTER}: '
        data = data.replace(strip, '')
        return data
