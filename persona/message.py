from time import time

from jinja2 import Environment, FileSystemLoader

class Message():
    '''Stores and renders the three message components used to request completion'''
    def __init__(self, config, user_input, **kwargs):
        '''Message() Init'''
        self.config = config           
        self.config.logger.info('New Message instance')
        # log the time the Message was created
        self.timestamp = str(time())
        self.user_input = user_input
        if kwargs:
            pass
        environment = Environment(loader=FileSystemLoader(f"{self.config.config_path}/etc/templates/"))
        self.template_user = environment.get_template(f"{self.config.persona_name}/user.tmpl")
        self.template_system = environment.get_template(f"{self.config.persona_name}/system.tmpl")
        self.template_assistant = environment.get_template(f"{self.config.persona_name}/assistant.tmpl")
        self._assistant = None
        self._user = None
        self._system = None
        self._completion = None

    @property
    def assistant(self):
        '''Renders the current assistant message using template'''
        self._assistant = self.template_assistant.render(
            persona=self.config.persona,
            user_input=self.user_input,
        )
        if self.config.debug:
            self.config.logger.info(f'Assistant Message: {self._assistant}')
        return self._assistant

    @property
    def system(self):
        '''Renders the current system message using template'''
        self._system = self.template_system.render(
            persona=self.config.persona,
            user_input=self.user_input,
        )
        if self.config.debug:
            self.config.logger.info(f'System Message: {self._system}')
        return self._system

    @property
    def user(self):
        '''Renders the current user message using template'''
        self._user = self.template_user.render(
            persona=self.config.persona,
            user_input=self.user_input,
        )
        if self.config.debug:
            self.config.logger.info(f'User Message: {self._user}')
        return self._user