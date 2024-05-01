#!/usr/bin/env python3
'''Represent a message as an object'''
from time import time

from jinja2 import Environment, FileSystemLoader
from loguru import logger

class Message():
    '''Stores and renders the three message components used to request completion'''
    def __init__(self, config, user_input, context):
        '''Message() Init'''
        self.config = config
        self._context = context
        logger.info('New Message instance')
        # log the time the Message was created
        self.timestamp = str(time())
        # store the user input
        self.user_input = user_input
        # store the rendered message components
        self._assistant = None
        self._user = None
        self._system = None
        self._completion = None
        self._environment = Environment(loader=FileSystemLoader(
            f"{self.config.config_path}/etc/templates/"))
        

    def __repl__(self):
        '''REPL representation'''
        return f'Message(): {self.user_input}'

    def _render_from_string(self, template_str):
        '''Render template from a string - used for second pass rendering'''
        # Second pass - render template tags inserted from the first pass
        template = self._environment.from_string(template_str)
        # user_input and context are already rendered in the first pass
        message = template.render(
            persona=self.config.persona
        )
        return message

    def _render_from_file(self, template_name):
        '''Render the message component from a file'''
        template = self._environment.get_template(
            f"{self.config.persona.context_template}/{template_name}.tmpl")
        message = template.render(
            persona=self.config.persona,
            user_input=self.user_input,
            context=self._context
        )
        return message

    def _render(self, template_name):
        '''Renders the assistant message using twp passes through the template engine'''
        logger.error(f'User Input: {self.user_input}')
        # First pass - render the variables directly referenced in the template
        message = self._render_from_file(template_name)
        message = self._render_from_string(message)
        return message

    @property
    def assistant(self):
        '''Renders the current assistant message using template'''
        self._assistant = self._render('assistant')
        if self.config.debug:
            logger.info(f'Assistant Message: {self._assistant}')
        return self._assistant

    @property
    def system(self):
        '''Renders the current system message using template'''
        self._system = self._render('system')
        if self.config.debug:
            logger.info(f'System Message: {self._system}')
        return self._system

    @property
    def user(self):
        '''Renders the current user message using template'''
        self._user = self._render('user')
        if self.config.debug:
            logger.info(f'User Message: {self._user}')
        return self._user
