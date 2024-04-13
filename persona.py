#!/usr/bin/env python3
'''Loader for Persona console OpenAI API client'''
import click

from src.conf import Conf
from src.personachat import PersonaChat

# Simple kickstart to glue objects together into application
# Keep app logic out of this file. 
def cmd(persona):
    ''' Persona - A flexible client for the OpenAI API '''
    app = PersonaChat()
    app.load_persona(persona)
    if app.config.debug:
        click.echo(app.persona)
    app.chat()

@click.command()
@click.option('--persona', default='default')
def stub(persona):
    '''Persona - Development testing loader'''
    config = Conf()
    config.load_persona(persona)
    print(config.persona.system)
    print(config.persona.system_rules)
    print(config.persona.assistant)
    print(config.persona.context_template)
    p = PersonaChat()
if __name__ == '__main__':
    stub()
