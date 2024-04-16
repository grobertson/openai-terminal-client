#!/usr/bin/env python3
import sys
import click

from colored import Fore, Style


help_text = f'''\
{Fore.green}COMMANDS{Fore.WHITE}:{Style.RESET}

{Fore.YELLOW}.quit                               {Fore.WHITE}Quit
{Fore.YELLOW}.new_conversation                   {Fore.WHITE}Start a new Conversation
{Fore.YELLOW}.save_conversation {Fore.BLUE}[{Fore.WHITE}FILENAME{Fore.BLUE}]       {Fore.WHITE}Save conversation to a file
{Fore.YELLOW}.list_conversations                 {Fore.WHITE}List saved conversations
{Fore.YELLOW}.load_conversation                  {Fore.WHITE}Load saved conversation from file
{Fore.YELLOW}.show_persona                       {Fore.WHITE}Display the current Persona's values
{Fore.YELLOW}.list_personas                      {Fore.WHITE}List available Personas
{Fore.YELLOW}.load_persona {Fore.BLUE}[{Fore.WHITE}PERSONA{Fore.BLUE}]             {Fore.WHITE}Load a Persona
{Fore.YELLOW}.show_context                       {Fore.WHITE}Display the most recent context values
{Fore.YELLOW}.help                               {Fore.WHITE}Show this help text.{Style.RESET}
'''

class Cmd():
    '''User commands for Persona'''

    config = None

    def __init__(self, config):
        self.config = config
        self.config.logger.info("REPL commands loaded. ")
        self._commands = self.gather_commands()

    def quit(self):
        '''Exit the app gracefully'''
        self.config.logger.info("REPL command: quit() ")
        click.echo(f'{Fore.YELLOW}Exiting...{Style.RESET}')
        sys.exit(0)

    def new_conversation(self):
        '''REPL Command: new_conversation'''
        self.config.logger.info("REPL command: new_conversation() ")
        return 'Command not yet implemented.'

    def save_conversation(self):
        '''REPL Command: save_conversation'''
        self.config.logger.info("REPL command: save_conversation() ")
        return 'Command not yet implemented.'

    def list_conversations(self):
        '''REPL Command: list_conversations'''
        self.config.logger.info("REPL command: list_conversations() ")
        return 'Command not yet implemented.'

    def load_conversation(self):
        '''REPL Command: load_conversation'''
        self.config.logger.info("REPL command: load_conversation() ")
        return 'Command not yet implemented.'

    def show_persona(self):
        '''REPL Command: show_persona'''
        self.config.logger.info("REPL command: show_persona() ")
        return 'Command not yet implemented.'

    def list_personas(self):
        '''REPL Command: list_personas'''
        self.config.logger.info("REPL command: list_personas() ")
        return 'Command not yet implemented.'

    def load_persona(self):
        '''REPL Command: load_persona'''
        self.config.logger.info("REPL command: load_persona() ")
        return 'Command not yet implemented.'

    def show_context(self):
        '''REPL Command: show_context'''
        self.config.logger.info("REPL command: show_context() ")
        return 'Command not yet implemented.'

    @property
    def help(self):
        '''REPL Command: help'''
        self.config.logger.info("REPL command: help() ")
        return help_text

    def gather_commands(self):
        '''Returns a list of command words'''
        self.config.logger.info('Gathering commands')
        commands = ['.quit',
                    '.exit',
                    '.new_conversation',
                    '.save_conversation',
                    '.list_conversations',
                    '.load_conversation',
                    '.show_persona',
                    '.list_personas',
                    '.load_persona',
                    '.show_context',
                    '.help',
                    '?',
                    ' ',
                    '']
        return commands

    def is_command(self, user_input):
        '''True if first word of user_input matches an element in self._commands[]'''
        user_input_parts = user_input.split(" ")
        if user_input_parts[0] in self._commands:
            return True
        else:
            return False
