#!/usr/bin/env python3

import os
import sys
import yaml
import click

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
