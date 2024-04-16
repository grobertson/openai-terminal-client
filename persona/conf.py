#!/usr/bin/env python3
'''A class for reading configuration data from a yaml file and representing it as an object'''
import os
import sys
import yaml
from loguru import logger
import click

from .persona import Persona
class Conf:
    '''Represent the configuration as an object'''
    #Config vars needed to load a config file
    home = os.environ.get('HOME')
    _api_key = os.environ.get("OPENAI_KEY", None)
    config_path = os.environ.get("OPENAI_TERMINAL_CONFIG_PATH", f'{home}')
    config_file = os.environ.get("OPENAI_TERMINAL_CONFIG_FILE", 'persona.conf.yaml')
    def __init__(self):
        '''Read and parse yaml config file, create object properties'''
        if not self._api_key:
            click.echo("ERROR: OPENAI_KEY environment variable not set. Exiting.")
            sys.exit(255)
        self.config_filename = f'{self.config_path}/etc/{self.config_file}'
        try:
            with open(self.config_filename, encoding='utf-8') as f:
                # use safe_load instead load
                config = yaml.safe_load(f)
                self.__dict__.update(config)
                if self._api_key:
                    self.api_key = self._api_key
        except FileNotFoundError:
            click.echo("ERROR: Unable to read configuration file \
                        f'{self.config_filename}'. Exiting.")
            sys.exit(255)
        self.log_file = f'{self.config_path}/{self.log_path}/persona.log'
        logger.remove() # Remove stderr sink
        if self.logging:
            # This leaves us with one sink, the logfile
            # If logger.add is never called the log > /dev/null
            logger.add(f'{self.log_file}')
        self.logger = logger
        self.logger.info(f'Configuration loaded from: {self.config_filename} bound to Conf.logger')
        if self.insecure:
            self.logger.warning('Insecure mode enabled. API requests will be unencrypted.')
            self.proto = 'http'
        else:
            self.proto = 'https'
        self.persona_path = f'{self.config_path}/etc/{self.persona_path}'
        self.personas = [None] ## Gets set from PersonChat.__init__
        self.persona_name = None
        self.persona = None

    def __repr__(self) -> str:
        '''Represent the Conf object with the full path to the loaded configuration file'''
        return ''.join([self.config_path, self.config_file])

    @property
    def base_url(self):
        '''Return the base url using the config'''
        if not self.port and self.insecure:
            self.port = 80
        if not self.port and not self.insecure:
            self.port = 443
        return f"{self.proto}://{self.host}:{self.port}/v1"

    def set_persona(self, name='default'):
        '''Load/reload a persona into the application'''
        if self.persona_name == name:
            self.logger.info(f'Ignoring attempt to load previously loaded Persona: \
                {self.persona_name}')
            return False
        if name in self.personas:
            self.persona_name = name
            self.persona = Persona(config=self)
            self.logger.info(f'Loaded Persona: {self.persona_name}.')
            return True
        self.logger.info(f'Ignoring attempt to load non-existent Persona: \
            {self.persona_name}')
        return False
