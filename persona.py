#!/usr/bin/env python3
'''Loader for Persona console OpenAI API client'''
import sys

import click
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea
from prompt_toolkit import Application

from src.conf import Conf
from src.personachat import PersonaChat
from src.extras import LOGO
from src.console import center_multiline_string

HELP_TEXT = '''\
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
.help                               Show this help text.'''
LOGO_TEXT = ''.join(['\n\n\n\n\n\n\n', center_multiline_string(LOGO[5])])
#Prompt toolkit setup

# The key bindings.
kb = KeyBindings()
# The layout.
search_field = SearchToolbar()  # For reverse search.
output_field = TextArea(style="class:output-field", text=LOGO_TEXT)
input_field = TextArea(
    height=1,
    prompt=">>> ",
    style="class:input-field",
    multiline=False,
    wrap_lines=False,
    search_field=search_field,
)
# Attach accept handler to the input field. We do this by assigning the
# handler to the `TextArea` that we created earlier. it is also possible to
# pass it to the constructor of `TextArea`.
# NOTE: It's better to assign an `accept_handler`, rather then adding a
#       custom ENTER key binding. This will automatically reset the input
#       field and add the strings to the history.
def accept(buff):
    '''Evaluate user input'''
    try:
        output = f"\n\nIn:  {input_field.text}\nOut: {eval(input_field.text)}"
        # Don't do 'eval' in real code!
    except BaseException as e:
        output = f"\n\n{e}"
    new_text = output_field.text + output

    # Add text to output buffer.
    output_field.buffer.document = Document(
        text=new_text, cursor_position=len(new_text)
    )

input_field.accept_handler = accept

@kb.add("c-c")
@kb.add("c-q")
def _(event):
    "Pressing Ctrl-Q or Ctrl-C will exit the user interface."
    event.app.exit()

# Style.
style = Style(
    [
        ("output-field", "bg:#000044 #ffffff"),
        ("input-field", "bg:#000000 #ffffff"),
        ("line", "#004400"),
    ]
)
container = HSplit(
    [
        output_field,
        Window(height=1, char="-", style="class:line"),
        input_field,
        search_field,
    ]
)

layout = Layout(container, focused_element=input_field)


app = Application(layout=layout, full_screen=True, key_bindings=kb, style=style)
# app.run() # You won't be able to Exit this app
# sys.exit()
# Simple kickstart to glue objects together into application
# Keep app logic out of this file. 
def cmd(persona, user_input):
    ''' Persona - A flexible client for the OpenAI API '''
    app = PersonaChat()
    app.config.set_persona(persona)
    if app.config.debug:
        app.config.logger(app.persona)
    app.conversation.send(user_input=user_input)

@click.command()
@click.option('--persona', default='default')
def dev_cmd(persona):
    '''Persona - Development testing loader'''
    config = Conf()
    config.logger.info('Dev loader started from persona.py ')
    config.persona_default = persona
    p = PersonaChat(config=config)
    config.logger.info(f'Personas found: {p.config.personas}')
    config.logger.info('Dev loader exiting.')
    p._run()
    sys.exit()

if __name__ == '__main__':
    dev_cmd()
