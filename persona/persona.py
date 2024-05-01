#!/usr/bin/env python3
'''Read a persona file and represent it as an object'''
import os
import sys
import yaml
import click
from loguru import logger
class Persona:
    '''Read a persona file and represent it as an object'''
    home = os.environ.get('HOME')
    config_path = os.environ.get("OPENAI_TERMINAL_CONFIG_PATH", f'{home}')
    _instance = None
    config = None

    def __init__(self, config=None, persona_name=False):
        self.config = config
        if not persona_name:
            if self.config.persona_default:
                persona_name = self.config.persona_default
            else:
                persona_name = 'default'
        try:
            persona_file = f'{self.config.persona_full_path}/{persona_name}.{self.config.persona_extension}'
            logger.info(f'Loading persona file: {persona_file}')
            with open(
                persona_file, 
                encoding='utf-8') as f:
                # use safe_load instead load
                config = yaml.safe_load(f)
                self.__dict__.update(config['persona'])
        except FileNotFoundError:
            click.echo(
                f"ERROR: Unable to read persona file '{persona_file}'. Exiting.")
            sys.exit()
        #Replace the character dict with an object, too
        self.character = self.Character(self.character)

    def __new__(cls, config, persona_name=None):
        '''Singleton pattern for Persona'''
        if cls._instance is None:
            cls._instance = super(Persona, cls).__new__(cls)
        return cls._instance

    def switch_persona(self, persona_name):
        '''Switch to a different persona'''
        try:
            persona_file = f'{self.config.persona_full_path}/{persona_name}.'
            persona_file += f'{self.config.persona_extension}'
            logger.info(f'Loading persona file: {persona_file}')
            with open(persona_file, encoding='utf-8') as f:
                # use safe_load instead load
                config = yaml.safe_load(f)
                self.__dict__.update(config['persona'])
        except FileNotFoundError:
            click.echo(
                f"ERROR: Unable to read persona file '{persona_file}'. Exiting.")
        #Replace the character dict with an object, too
        self.character = self.Character(self.character)

    @property
    def name(self):
        '''Shorthand for config.character.given_name'''
        return self.character.given_name

    class Character():
        '''Handle the character stanza in the persona file'''
        given_name = ''
        middle_name = ''
        sir_name = ''

        def __init__(self, character):
            self.__dict__.update(character)

        @property
        def get(self) -> dict:
            '''Return the character object'''
            return self.__dict__

        @property
        def full_name(self):
            '''Helper to return full name'''
            return ' '.join([self.given_name, self.middle_name, self.sir_name])
