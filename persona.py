#!/usr/bin/env python3

# import shutil
import os
import sys
import glob
from openai import OpenAI
import click
import yaml
import nltk

class Conf:
    '''Represent the configuration as an object'''

    '''Config vars needed to load a config file'''
    home = os.environ.get('HOME')
    config_path = os.environ.get("OPENAI_TERMINAL_CONFIG_PATH", f'{home}/etc/')
    config_file = os.environ.get("OPENAI_TERMINAL_CONFIG_FILE", 'persona.conf.yaml')

    def __init__(self):
        '''Read and parse yaml config file, create object properties'''
        try:
            with open(f'{self.config_path}/{self.config_file}', encoding='utf-8') as f:
                # use safe_load instead load
                config = yaml.safe_load(f)
        except FileNotFoundError:
            click.echo(
                f"ERROR: Unable to read configuration file \
                    '{self.config_path}/{self.config_file}'. Exiting.")
            sys.exit(255) 
        self.__dict__.update(config)
        #Set initial persona
        self.persona_name = None

    def __repr__(self) -> str:
        return ''.join([self.config_path, self.config_file])

class Persona:
    '''Read a persona file and represent it as an object'''
    
    home = os.environ.get('HOME')
    config_path = os.environ.get("OPENAI_TERMINAL_CONFIG_PATH", f'{home}/etc/')
    def __init__(self, config, persona_name=False):
        if not persona_name:
            persona_name = config.persona_name
        try:
            with open(
                f'{self.config_path}/{config.persona_path}/{persona_name}.{config.persona_extension}', 
                encoding='utf-8') as f:
                # use safe_load instead load
                config = yaml.safe_load(f)
                self.__dict__.update(config['persona'])
        except FileNotFoundError:
            click.echo(
                f"ERROR: Unable to read persona file '{config.persona_path}/{config.persona_name}.{config.persona_extension}'. Exiting.")
            sys.exit()
        #Replace the character dict with an object, too
        self.character = self.Character(self.character)

    def __repr__(self) -> str:
        return str(self.character)

    @property
    def name(self):
        '''Shorthand for config.character.given_name'''
        return self.character.given_name

    class Character():
        '''Handle the character stanza in the persona file'''
        def __init__(self, character):
            self.__dict__.update(character)

        def __repr__(self) -> str:
                return self.given_name
        @property
        def full_name(self):
            '''Helper to return full name'''
            return ' '.join([self.given_name, self.middle_name, self.sir_name])

class PersonaChat():
    '''Object to contain the application logic. Nearly everything happens in here, or from here.'''
    def __init__(self, persona='default'):
        self.config = Conf()
        self.base_url = f"http://{self.config.host}:{self.config.port}/v1"
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.config.api_key)
        self.personas
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


def cmd(persona):
    app = PersonaChat()
    app.load_persona(persona)
    if app.config.debug:
        click.echo(app.persona)
    app.chat()



@click.command()
@click.argument('persona', default='default')
def stub(persona):
    config = Conf()
    persona = Persona(config, persona)
    
    print(persona.system)
    print(persona.system_rules)
    print(persona.assistant)
    print(persona.context_template)
    print(len(nltk.word_tokenize(persona.system)))
    
    

if __name__ == '__main__':
    stub()
