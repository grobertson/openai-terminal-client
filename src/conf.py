#!/usr/bin/env python3

import os
import sys
import yaml
import click

#   A class for reading configuration data from a yaml file and representing it as an object. 

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