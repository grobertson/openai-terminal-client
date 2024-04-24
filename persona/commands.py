#!/usr/bin/env python3
'''REPL commands for the application'''
import sys

from colored import Fore, Style
from loguru import logger
import click

from persona.config import Settings
from persona.persona import Persona
from persona.conversation import Conversation

key_theme = f'{Fore.YELLOW}'
value_theme = f'{Style.RESET}{Fore.WHITE}'
sep_theme = f'{Fore.BLUE}{Style.BOLD}'
reset = f'{Style.RESET}'

class Cmd():
    '''User commands for Persona'''

    _instance = None

    def __init__(self):
        logger.info("REPL commands loaded. ")
        self.config = Settings()
        self.conversation = Conversation()
        self.commands = self.gather_commands()

    def __new__(cls):
        '''Singleton pattern for Cmd'''
        if cls._instance is None:
            cls._instance = super(Cmd, cls).__new__(cls)
        return cls._instance

    def quit(self, cmd=None, context=None):
        '''Exit the app gracefully'''
        logger.info("REPL command: quit() ")
        click.echo(f'{Fore.YELLOW}Exiting...{Style.RESET}')
        sys.exit(0)

    def new_conversation(self, cmd=None, context=None):
        '''REPL Command: new_conversation'''
        logger.info("REPL command: new_conversation() ")
        return 'Conversations not yet implemented.'

    def save_conversation(self, cmd=None, context=None):
        '''REPL Command: save_conversation'''
        logger.info(f"REPL command: save_conversation({cmd}) ")
        return 'Conversations not yet implemented.'

    def list_conversations(self, cmd=None, context=None):
        '''REPL Command: list_conversations'''
        logger.info("REPL command: list_conversations() ")
        return 'Conversations not yet implemented.'

    def load_conversation(self, cmd=None, context=None):
        '''REPL Command: load_conversation'''
        logger.info("REPL command: load_conversation({cmd}) ")
        cmd = cmd.split(' ')
        return 'Conversations not yet implemented.'

    def show_persona(self, cmd=None, context=None): # noqa: W0613
        '''REPL Command: show_persona'''
        persona = self.config.get_persona()
        output = []
        output.append('')
        for key in persona:
            value = persona[key]
            if isinstance(value, list):
                output.append(f"{key_theme}{key}{sep_theme}:")
                for item in value:
                    output.append(f"{key_theme} - {value_theme}{item}{reset}")
            elif key == 'character':
                output.append(f"{key_theme}{key}{sep_theme}:")
                for k in value.get:
                    v = value.get[k]
                    output.append(f"{key_theme} - {k}{sep_theme}: {value_theme}{v}{reset}")
            else:
                output.append(f"{key_theme}{key}{sep_theme}: {value_theme}{value}{reset}")
        logger.info("REPL command: show_persona() ")
        output.append('')
        return '\n'.join(output)

    def list_personas(self, cmd=None, context=None):
        '''REPL Command: list_personas'''
        output = '\n'
        self.config.personas = self.config.scan_personas(self.config.persona_full_path)
        for p in self.config.get_personas():
            output += f'{Fore.YELLOW}{Style.BOLD}{p["name"]}{Fore.WHITE} ("'
            output += f'{Fore.GREEN}{p["display_name"]}'
            output += f'{Fore.WHITE}"){Style.RESET}\n'
            output += f' {p["description"]}\n\n'
        logger.info("REPL command: list_personas() ")
        return output

    def load_persona(self, cmd=None, context=None):
        '''REPL Command: load_persona'''
        logger.info("REPL command: load_persona() ")
        cmd_args = cmd.split(' ')
        if len(cmd_args) == 1:
            return 'Please provide a Persona name.'
        p = Persona(self.config)
        p.switch_persona(cmd_args[1])
        return self.show_persona(cmd, context)

    def reset_context(self, cmd=None, context=None):
        '''REPL Command: reset_context'''
        logger.info("REPL command: reset_context() ")
        self.conversation.reset_context()
        return 'Context reset.'

    def set_temperature(self, cmd=None, context=None):
        '''REPL Command: set_temperature'''
        logger.info("REPL command: set_temperature() ")
        cmd_args = cmd.split(' ')
        if len(cmd_args) == 1:
            return 'Please provide a temperature.(0.00-1.00)'
        self.config.temperature = float(cmd_args[1])
        return f'API Parameter temperature set to {cmd_args[1]}'

    def set_max_tokens(self, cmd=None, context=None):
        '''REPL Command: set_max_tokens'''
        logger.info("REPL command: set_max_tokens() ")
        cmd_args = cmd.split(' ')
        if len(cmd_args) == 1:
            return 'Please provide a number of tokens.'
        self.config.max_tokens = int(cmd_args[1])
        return f'API Parameter max_tokens set to {cmd_args[1]}'

    def set_model(self, cmd=None, context=None):
        '''REPL Command: set_model'''
        logger.info("REPL command: set_model() ")
        cmd_args = cmd.split(' ')
        if len(cmd_args) == 1:
            return 'Please provide a model name.'
        self.config.model_name = cmd_args[1]
        return f'API model set to {cmd_args[1]}'

    def set_server(self, cmd=None, context=None):
        '''REPL Command: set_server'''
        logger.info("REPL command: set_server() ")
        cmd_args = cmd.split(' ')
        if len(cmd_args) == 1:
            return 'Please provide a named configuration.'
        self.config.set_server(cmd_args[1])
        return f'API server set to {cmd_args[1]}'

    def show_servers(self, cmd=None, context=None):
        '''REPL Command: show_servers'''
        logger.info("REPL command: show_servers() ")
        output = f'{Fore.YELLOW}Servers:{Style.RESET}\n'
        output += f'{Fore.YELLOW}--------{Style.RESET}\n'
        for server in self.config.servers:
            output += f'{Fore.YELLOW}{server}\t{Style.RESET}\n'
        return output

    def show_config(self, cmd=None, context=None):
        '''REPL Command: show_config'''
        def expand_persona(persona):
            '''Expand the persona dict'''
            n = persona['name']
            dn = persona['display_name']
            d = persona['description']
            return f'{Fore.YELLOW}{dn} ({n}){Style.RESET}: {d}\n'

        logger.info("REPL command: show_config() ")
        output = f'{Fore.YELLOW}Config:{Style.RESET}\n'
        output += f'{Fore.YELLOW}--------{Style.RESET}\n'
        for key, value in self.config.__dict__.items():
            if key == 'servers':
                output += '\nServers\n----\n'
                for server in self.config.servers:
                    n = server['name']
                    h = server['host']
                    output += f'\t{Fore.YELLOW}{n}{Style.RESET} : {h}\n'
                output += '\n'
            elif key == 'personas':
                output += '\nPersonas\n----\n'
                for persona in self.config.personas:
                    output += expand_persona(persona)
                output += '\n'
            else:
                output += f'{Fore.YELLOW}{key}{Style.RESET} : {value}\n'
        return output

    def set_top_p(self, cmd=None, context=None):
        '''REPL Command: set_topP'''
        logger.info("REPL command: set_top() ")
        cmd_args = cmd.split(' ')
        if len(cmd_args) == 1:
            return 'Please provide a value (0.00-1.00).'
        self.config.top_p = float(cmd_args[1])
        return f'API Parameter top_p set to {cmd_args[1]}'

    def show_context(self, cmd=None, context=None):
        '''REPL Command: show_context'''
        logger.info("REPL command: show_context() ")
        message = f'\n{Fore.YELLOW}Context:{Style.RESET}\n'
        message += f'{Fore.YELLOW}--------{Style.RESET}\n'
        message += f'{Fore.YELLOW}{context}{Style.RESET}\n'
        return message

    def show_user(self, cmd=None, context=None):
        '''REPL Command: show_context'''
        logger.info("REPL command: show_user() ")
        if self.conversation.current_message is not None:
            m = f'{Fore.YELLOW}\nUser:{Style.RESET}\n'
            m += f'{Fore.YELLOW}--------{Style.RESET}\n'
            m += f'{Fore.YELLOW}{self.conversation.current_message.user}{Style.RESET}\n'
            return m
        return 'No user message available.'

    def show_assistant(self, cmd=None, context=None):
        '''REPL Command: show_context'''
        logger.info("REPL command: show_assistant() ")
        if self.conversation.current_message is not None:
            m = f'{Fore.YELLOW}\nAssistant :{Style.RESET}\n'
            m += f'{Fore.YELLOW}--------{Style.RESET}\n'
            m += f'{Fore.YELLOW}{self.conversation.current_message.assistant}{Style.RESET}\n'
            return m
        return 'No assistant message available.'

    def show_system(self, cmd=None, context=None):
        '''REPL Command: show_context'''
        logger.info("REPL command: show_system() ")
        if self.conversation.current_message is not None:
            m = f'{Fore.YELLOW}\nSystem :{Style.RESET}\n'
            m += f'{Fore.YELLOW}--------{Style.RESET}\n'
            m += f'{Fore.YELLOW}{self.conversation.current_message.system}{Style.RESET}\n'
            return m
        return 'No system message available.'

    def toggle_debug(self, cmd=None, context=None):
        '''REPL Command: set_temperature'''
        logger.info("REPL command: toggle_debug() ")
        self.config.debug = not self.config.debug
        return f'Debug set to {self.config.debug}'

    @property
    def show_help(self, cmd=None, context=None):
        '''REPL Command: help'''
        logger.info("REPL command: help() ")
        formatted_text = '\n'.join(self.help_text)
        return formatted_text

    def gather_commands(self):
        '''Returns a list of command words'''
        # Wrapping this in a function to allow for eventual plugin commands
        logger.info('Gathering commands')
        commands = ['.quit',
                    '.exit',
                    '.new_conversation',
                    '.save_conversation',
                    '.list_conversations',
                    '.load_conversation',
                    '.show_persona',
                    '.list_personas',
                    '.load_persona',
                    '.reset_context',
                    '.show_context',
                    '.set_temperature',
                    '.set_max_tokens',
                    '.set_server',
                    '.show_servers',
                    '.show_config',
                    '.set_model',
                    '.set_top_p',
                    '.toggle_debug',
                    '.reset_context',
                    '.show_user',
                    '.show_assistant',
                    '.show_system',
                    '.help',
                    '?',
                    ' ',
                    '',
                    '.']
        return commands

    def dispatch_or_false(self, cmd):
        '''Dispatch calls to handle user commands'''
        if self.is_command(cmd):
            logger.info(f'Dispatching command: {cmd}')
            cmd_args = cmd.split(' ')
            verb = cmd_args[0][1:] # Remove the leading period
            if hasattr(self, verb):
                func = getattr(self, verb)
                # Call the method with the command and context
                # print the return value
                click.echo(func(cmd=cmd, context=self.conversation.get_context))
            else:   # Handle commands that are not methods
                if verb=='exit':
                    self.quit(cmd=cmd,context='')
                elif verb=='help' or verb=='?':
                    click.echo(self.help_text)
                else:
                    click.echo(f'Command not found: {cmd}')
            return True
        return False

    def is_command(self, user_input):
        '''True if first word of user_input matches an element in self[]'''
        return user_input.split(" ")[0] in self.commands

    @property
    def help_text(self) -> str:
        '''Assemble and return the help text for the application'''
        text = []
        text.append(f'{Fore.GREEN}COMMANDS{Fore.WHITE}:{Style.RESET}')
        text.append(f'{Fore.YELLOW}==============================={Style.RESET}')
        text.append(f'\n{Fore.GREEN}Completion Parameters{Fore.WHITE}:{Style.RESET}')
        text.append(f'{Fore.WHITE}----{Style.RESET}')
        text.append(f'{Fore.YELLOW}.set_temperature {Fore.BLUE}[{Fore.WHITE}TEMPERATURE{Fore.BLUE}]\t\t{Fore.WHITE}Set the temperature for the API')
        text.append(f'{Fore.YELLOW}.set_max_tokens {Fore.BLUE}[{Fore.WHITE}TOKENS{Fore.BLUE}]\t\t{Fore.WHITE}Set the max tokens for the API')
        text.append(f'{Fore.YELLOW}.set_model {Fore.BLUE}[{Fore.WHITE}MODEL{Fore.BLUE}]\t\t\t{Fore.WHITE}Set the model for the API')
        text.append(f'{Fore.YELLOW}.set_server {Fore.BLUE}[{Fore.WHITE}SERVER{Fore.BLUE}]\t\t\t{Fore.WHITE}Set the default server')
        text.append(f'{Fore.YELLOW}.set_top_p {Fore.BLUE}[{Fore.WHITE}TOP_P{Fore.BLUE}]\t\t\t{Fore.WHITE}Set the top_p value for the API')
        text.append(f'\n{Fore.GREEN}Inspect values{Fore.WHITE}:{Style.RESET}')
        text.append(f'{Fore.WHITE}----{Style.RESET}')
        text.append(f'{Fore.YELLOW}.show_servers\t\t\t\t{Fore.WHITE}List available servers')
        text.append(f'{Fore.YELLOW}.show_config\t\t\t\t{Fore.WHITE}Show the current configuration')
        text.append(f'{Fore.YELLOW}.show_context\t\t\t\t{Fore.WHITE}Display the most recent context values')
        text.append(f'{Fore.YELLOW}.show_assistant\t\t\t\t{Fore.WHITE}Display the most recent context values')
        text.append(f'{Fore.YELLOW}.show_user\t\t\t\t{Fore.WHITE}Display the most recent context values')
        text.append(f'{Fore.YELLOW}.show_system\t\t\t\t{Fore.WHITE}Display the most recent context values')
        text.append(f'\n{Fore.GREEN}Conversations{Fore.WHITE}:{Style.RESET}')
        text.append(f'{Fore.WHITE}----{Style.RESET}')
        text.append(f'{Fore.YELLOW}.new_conversation\t\t\t{Fore.WHITE}Start a new Conversation')
        text.append(f'{Fore.YELLOW}.save_conversation {Fore.BLUE}[{Fore.WHITE}FILENAME{Fore.BLUE}]\t\t{Fore.WHITE}Save conversation to a file')
        text.append(f'{Fore.YELLOW}.list_conversations\t\t\t{Fore.WHITE}List saved conversations')
        text.append(f'{Fore.YELLOW}.load_conversation\t\t\t{Fore.WHITE}Load saved conversation from file')
        text.append(f'\n{Fore.GREEN}Personas{Fore.WHITE}:{Style.RESET}')
        text.append(f'{Fore.WHITE}----{Style.RESET}')
        text.append(f'{Fore.YELLOW}.show_persona\t\t\t\t{Fore.WHITE}Display the current Persona\'s values')
        text.append(f'{Fore.YELLOW}.list_personas\t\t\t\t{Fore.WHITE}List available Personas')
        text.append(f'{Fore.YELLOW}.load_persona {Fore.BLUE}[{Fore.WHITE}PERSONA{Fore.BLUE}]\t\t\t{Fore.WHITE}Load a Persona')
        text.append(f'\n{Fore.GREEN}Application{Fore.WHITE}:{Style.RESET}')
        text.append(f'{Fore.WHITE}----{Style.RESET}')
        text.append(f'{Fore.YELLOW}.toggle_debug\t\t\t\t{Fore.WHITE}Toggle debug mode')
        text.append(f'{Fore.YELLOW}.reset_context\t\t\t\t{Fore.WHITE}Reset the context')
        text.append(f'{Fore.YELLOW}.help\t\t\t\t\t{Fore.WHITE}Show this help text.{Style.RESET}')
        text.append(f'{Fore.YELLOW}.quit\t\t\t\t\t{Fore.WHITE}Quit')
        return '\n' + '\n'.join(text) + '\n'
