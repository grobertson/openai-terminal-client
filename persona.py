#!/usr/bin/env python3
'''Loader for Persona console OpenAI API client'''
import sys

import click

from persona.conf import Conf
from persona.personachat import PersonaChat
from persona.console import colorize_chat, wraptext

# Simple kickstart to glue objects together into application
# Keep app logic out of this file.
# This is just a loader for the application.
@click.command()
@click.option('--persona', default='default', help='Persona to load')
@click.option('--debug', default=False, help='Debug mode')
@click.option('--no_splash', default=False, help='Disable splash screen')
@click.option('--question', default=None, help='User message to send to API')
def app(persona, debug, no_splash, question):
    '''Persona - A flexible client for the OpenAI API'''
    config = Conf()
    config.debug = False
    if debug:
        config.debug = True
    if question is None:
        config.splash = not no_splash
    else:
        # If we're running a single-shot request, don't show the splash screen
        config.splash = False
    config.logger.info('Dev loader started from persona.py ')
    config.persona_default = persona
    p = PersonaChat(config=config)
    config.logger.info(f'Personas found: {p.config.personas}')
    if question:
        if config.debug:
            config.logger.info(f'Making single-shot request: {question}')
        completion = p.run_once(question)
        content = completion.choices[0].message.content
        #content = wraptext(content)
        content = colorize_chat(content)
        click.echo(f'\n{content}\n')
    else:
        config.logger.info('Starting interactive mode')
        p.run()
    config.logger.info('Dev loader exiting.')
    sys.exit()

if __name__ == '__main__':
    app()
