# Persona

Persona (originally forked from Genie) is targeted to be a flexible and highly configurable
client for OpenAI compatible API servers and providers.

The concept of the Persona system allows for non-trivial dynamic prompts to be created, such as
prompts that are conditional on variables, and prompts that are generated based on a template.

The Persona system gives you the ability to define prompts in a more modular way. Employing
[a 'persona' file to define variables](etc/personas/default.persona) (YAML Format) and then rendering System, Assistant,
and User prompts from [Jinja templates to determine format of prompts](etc/templates/default/assistant.tmpl), making it easier to
reuse prompts across different skills, create rich roleplaying characters, or make chat
based interactive games using any available LLM.

Prompts from Genie have been deprecated. Previous Genie prompts have been
converted to the Persona system.

I would like to thank @jameswylde, the author of Genie, for a good place 
from which to jump off. 

If you find Persona's flexibility is overwhelming, you might check out Genie for a more straight-forward client.

## Table of Contents

- [Persona](#persona)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [About](#about)
  - [License](#license)

## Installation

Instructions on how to install and set up the project.

Clone this repository into a local directory.

```
git clone https://github.com/grobertson/persona-openai-cli-chat/
```

Export API keys environment variables, creating one variable per API server, to match
the key_name varable for each server defined in [persona.conf.yaml](etc/persona.conf.yaml.example).

Install dependencies with poetry.

See the example configuration file in [etc/](etc/) for application settings.

See the initial Personas provided in [/etc/personas/](/etc/personas) for examples to use in
creating your own Personas. 

## Usage

Instructions on how to use the project and any relevant examples.

- *TO-DO: Fix command line arguments*

```
Persona - A flexible client for the OpenAI API

Options:
  --persona TEXT       Persona to load
  --debug BOOLEAN      Debug mode
  --no_splash BOOLEAN  Disable splash screen
  --question TEXT      User message to send to API
  --help               Show this message and exit.
```

An assortment of commands are available from within Persona's interactive REPL

Type *'?'* or *'.help'* at the prompt for help.

To exit the program, type '.exit' or '.quit' at the prompt, or press Ctrl-C.

## Additional Information

### Contributing

Guidelines for contributing to the project and how to submit pull requests.

If you've modified Persona in a way you think is interesting or cool, please submit a pull request.

- *TO-DO: Write contributor guidelines

### About

- Original Copyright (c) 2023 James Wylde @jameswylde

- Modifications Copyright (c) 2024 Grant Robertson @grobertson

### License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the conditions in [LICENCE.md](LICENSE.md)
