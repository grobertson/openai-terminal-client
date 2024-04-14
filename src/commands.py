#!/usr/bin/env python3
import sys

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
        help = '''\
COMMANDS:
.quit                               Quit
.new_conversation                   Start a new Conversation
.save_conversation [FILENAME]       Save conversation to a file
.list_conversations                 List saved conversations
.load_conversation                  Load saved conversation from file
.show_persona                       Display the current Persona's values
.list_personas                      List available Personas
.load_persona [PERSONA]             Load a Persona
.show_context                       Display the most recent context values
.help                               Show this help text.
'''
        return help

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
