#!/usr/bin/env python3
"""A class for reading configuration data from a yaml file and representing it as an object"""

import os
import glob
import sys
import yaml
from yaml.scanner import ScannerError
from yaml.parser import ParserError
from openai import OpenAI
from loguru import logger
import click

from .persona import Persona

class Settings:
    """Represent the configuration as an object"""

    # Config vars needed to load a config file
    home = os.environ.get("HOME")
    config_path = os.environ.get("OPENAI_TERMINAL_CONFIG_PATH", f"{home}")
    config_file = os.environ.get("OPENAI_TERMINAL_CONFIG_FILE", "persona.conf.yaml")
    # Required fields in the config file
    log_path = None
    log_level = None
    log_file = None
    debug = False
    logging = False
    default_server = "default"
    user = 'Persona User'
    servers = []
    _personas = []
    persona_path = None
    persona_name = None
    persona_extension = None
    persona = None
    persona_default = None
    host = None
    port = None
    api_key = None
    path = None
    proto = "https"
    insecure = False
    keyname = None
    model_name = None
    temperature = None
    max_tokens = None
    max_context = None
    top_p = None
    frequency_penalty = None
    presence_penalty = None
    stop = None
    n = None
    _instance = None

    def __new__(cls) -> object:
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Read and parse yaml config file, create object properties"""
        self.config_filename = f"{self.config_path}/etc/{self.config_file}"
        self.proto = "https"
        self.persona_name = None
        self.host = None
        self.port = None
        self.insecure = False
        self.keyname = None
        try:
            with open(self.config_filename, encoding="utf-8") as f:
                # use safe_load instead load
                config = yaml.safe_load(f)
                # Update the object with the config values
                self.__dict__.update(config)
        except FileNotFoundError:
            click.echo(
                "ERROR: Unable to read configuration file \
                        f'{self.config_filename}'. Exiting."
            )
            sys.exit(255)
        self.log_file = f"{self.config_path}/{self.log_path}/persona.log"
        logger.remove()  # Remove stderr sink. Must .add() to enable logging
        if self.logging:
            # This leaves us with one sink, the logfile
            # If logger.add is never called the log > /dev/null
            logger.add(f"{self.log_file}")
        logger.info(f"Configuration loaded from: {self.config_filename} bound to Conf.logger")
        self.persona_full_path = f"{self.config_path}/etc/{self.persona_path}"
        self.set_server(name=self.default_server)
        self.client = OpenAI(base_url=self.base_url,
                              api_key=self.api_key)
        self._personas = self.scan_personas(self.persona_full_path)
        self.persona = Persona(config=self, persona_name=self.persona_name)
        self.set_persona(name=self.persona_default)

    def __repr__(self) -> str:
        """Represent the Conf object with the full path to the loaded configuration file"""
        return f"{self.config_path}{self.config_file}"

    @property
    def base_url(self) -> str:
        """Return the base url using the config"""
        if self.insecure:
            logger.warning("Insecure mode enabled. API requests will be unencrypted.")
            self.proto = "http"
        if not self.port and self.insecure:
            self.port = 80
        if not self.port and not self.insecure:
            self.port = 443
        logger.warning(
            f"Using base_url: {self.proto}://{self.host}:{self.port}{self.path}"
        )
        return f"{self.proto}://{self.host}:{self.port}{self.path}"

    def get_server(self, name):
        """Return the server configuration based on the name provided"""
        for server in self.servers:
            if str(server['name']).lower() == str(name).lower():
                return server
            return None

    def set_server(self, name=None) -> bool:
        """Set the server to send requests to"""
        if not name:
            name = self.default_server
        for server in self.servers:
            if server["name"] == name:
                self.host = server["host"]
                self.port = server["port"]
                self.path = server["path"]
                self.proto = 'https'
                if server["insecure"]:
                    self.proto = 'http'
                self.api_key = os.environ.get(server["keyname"], None)
                self.client = OpenAI(base_url=self.base_url,
                                     api_key=self.api_key)
                logger.info(f"Server set to: {self.host}:{self.port}")
                return True
                
                self.host = server["host"]
                self.port = server["port"]
                self.path = server["path"]
                self.proto = 'https'
                if server["insecure"]:
                    self.proto = 'http'
                self.api_key = os.environ.get(server["keyname"], None)
                self.client = OpenAI(base_url=self.base_url,
                                api_key=self.api_key)
                logger.info(f"Server set to: {self.host}:{self.port}")
                return True
        logger.error(f"Failed to set server to: {self.host}")
        return False

    def set_persona(self, name="default") -> bool:
        """Load/reload a persona into the application"""
        if self.persona_name == name:
            logger.info(f"Ignoring attempt to load previously loaded Persona: \
                {self.persona_name}")
            return False
        else:
            for persona in self.get_personas():
                if persona['name'] == name:
                    self.persona_name = name
                    self.persona = Persona(
                        config=self
                    )  # Returns a Persona object using persona_name
                    self.persona.user = self.user
                    logger.info(f"Loaded Persona: {self.persona_name}.")
                    return True
        logger.info(f"Ignoring attempt to load non-existent Persona: \
            {self.persona_name}")
        return False

    def get_persona(self) -> dict:
        """Return the persona object as a dictionary"""
        return self.persona.__dict__

    def scan_personas(self, persona_path, **kwargs) -> list:
        """Find all persona files and attempt to load each of them."""
        logger.info(f"Scanning for persona files in: {persona_path}")
        if kwargs:
            pass
        personas = []
        for filename in glob.glob(
            os.path.join(persona_path, f"*.{self.persona_extension}")
        ):
            logger.info(f"Checking Persona file: {filename}")
            personas.append(self.load_persona(filename))
        return personas

    def get_personas(self) -> list:
        """Return the list of personas as a list of dictionaries"""
        return self._personas

    def load_persona(self, filename) -> dict:
        """Load a persona from a file"""
        try:
            # Attempt to open and parse each file. If it looks valid, add it to the list
            with open(filename, "r", encoding="utf-8") as f:
                persona = yaml.safe_load(f)
                if not persona:
                    if self.debug:
                        logger.error(f"Invalid persona file detected: {filename}")
                else:
                    val = persona["persona"]["name"]
                    logger.info(f'Found Persona "{val}" : {filename}')
                    return persona["persona"]
        except (FileNotFoundError, ScannerError, ParserError) as err:
            logger.error(f"Error while parsing persona : {filename}\n")
            logger.error(err)
            return None
