#!/usr/bin/env python3

import os
import glob
import yaml

from openai import OpenAI
import click

from .conf import Conf
from .persona import Persona

class PersonaChat():
    '''Object to contain the application logic. Nearly everything happens in here, or from here.'''
    def __init__(self, persona='default'):
        self.config = Conf()
        self.base_url = f"http://{self.config.host}:{self.config.port}/v1"
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.config.api_key)
        self.personas = []
        self.persona = False
        self.load_personas(self.config.persona_path)
        self.assistant = str('')
        self.usermsg = str('')
        self.character = str("")
        self.config.user = str("User")
        self.conv_log = f'{self.assistant}\n'
        #An array to contain each individual message as an element.
        self.conversation_history = [] 
        ## Original Assistant text will always be element 0 of conversation_history
        self.conversation_history.append(self.assistant) 
        self.system = ''

    def chat(self, **kwargs):
        '''The main chat loop'''
        while 1:
            click.echo('[You]:\t', nl=False)
            self.usermsg = input()
            self.conv_log = f'\n{self.assistant}\n### {self.config.user}: {self.usermsg}\n'
            self.conversation_history.append(f'### {self.config.user}: {self.usermsg}')
            completion = self.fetch_completion()
            msg = completion.choices[0].message
            msg = self.clean_data(msg.content)
            # TODO Replace conv_log with conversation_history as properly concatenated string
            click.echo(f'[{CHARACTER}]:\t{msg}')
            self.conversation_history.append(f'### {CHARACTER}: {msg}')
            self.conv_log = f'{self.conv_log}\n### {CHARACTER}: {msg}\n'
            self.assistant = self.conv_log

    def fetch_completion(self, **kwargs):
        '''Make api request to get next response'''
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "assistant", "content": ASSISTANT},
            {"role": "user", "content": USERMSG}
        ]
        if self.config.debug:
            #Show the assembled message
            click.echo(messages)
        req = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.config.max_tokens,
                )
        return req

    def load_personas(self, persona_path, **kwargs):
        '''Find all persona files and attempt to load each of them.'''
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
        self.persona = Persona(config=self.config)

    def clean_data(self, data, **kwargs):
        '''Remove common junk from response before using'''
        # TODO Validation
        # Strip <|im_end|>
        strip='<|im_end|>'
        data = data.replace(strip, '')
        strip = f'### {CHARACTER}: '
        data = data.replace(strip, '')
        return data
