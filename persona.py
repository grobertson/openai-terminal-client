#!/usr/bin/env python3

import click
import nltk

from src.conf import Conf
from src.persona import Persona
from src.personachat import PersonaChat

# Simple kickstart to glue objects together into application
# Keep app logic out of this file. 
def cmd(persona):
    ''' Application bootstrap '''
    app = PersonaChat()
    app.load_persona(persona)
    if app.config.debug:
        click.echo(app.persona)
    app.chat()

@click.command()
@click.argument('persona', default='default')
def stub(persona):
    ''' Dev use loader '''
    config = Conf()
    persona = Persona(config, persona)
    print(persona.system)
    print(persona.system_rules)
    print(persona.assistant)
    print(persona.context_template)
    print(len(nltk.word_tokenize(persona.system)))

if __name__ == '__main__':
    stub()
