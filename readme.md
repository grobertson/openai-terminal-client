## READ FIRST!!!

This is a fork intended to explore extending "Genie" to be primarily a more robust and featureful command line chat tool, with a secondary goal of retaining Genie's one-shot question/answers feature for use as a script component. When and if this fork reaches the stated goals, this README will be updated. Motivation for this project is academic and experimental, rather than functional. One specific intent of experimentation will be in long conversation context management and summarization. 

### Planned features
- Extended support for adding your own prompts
- Easy adjustment of model params, specifically temperature and min-P, both when initializing and at any time during a session
- Extended support for defining available models
- Set a default model, saved in ~/.openai-terminal-client.conf
- Chat logging
- Context management for longer conversations (This is a broad ranging experiment)
- Enhanced logging or other abilities surrounding inspect/modify context
- CI/CD
- Excellent command help and well executed options and parameters

  
## ChatGPT in your terminal

OpenAI's ChatGPT integrated into your shell.

![](https://imgur.com/2WDy29Y.png)

### Description

Python implementation of OpenAI's ChatGPT intergrated into your shell - interaction can be either calling genie from shell for one off questions, or entering into an interactive chat with genie. There are some chat prompts to use for more honed responses - these can be added or amended in `prompts.py`

### Dependencies

* Install module dependencies using pip:
 ```pip install -r requirements.txt```

* OpenAI API key - you can get one [here](https://platform.openai.com/overview) - Dashboard - Settings - View API Keys - Generate


### Installing

* Clone the repo and copy the folder to a permanent location (including the /src/ folder).

* Open the script and amend `openai.api_key = "API_KEY"` with your aforementioned API key and save.

* Create an alias pointing at the script's location, either in your bash profile *~/.bash_profile* or *~/.bashrc* or *~/.zshrc* - i.e:
 ```alias genie='python3 /path/to/genie.py'```

### Usage

Using your chosen alias you can call it from shell and pass your question as an argument for one off questions:

```$ genie "Recommend a python module for LP and link documentation?"```

![genie](https://imgur.com/JYfwkd7.png)

Or by calling the alias without argument to enter an interactive chat with ChatGPT:

```$ genie ```

![genie-interactive](https://imgur.com/40kRhBe.png)


The default model used is `gpt-3.5-turbo` for a more fluent experience as its replies are much faster and API pricing is significantly cheaper.

You can switch API model using the `--model` argument (run without `--model` to use the default model) if you'd like to to use gpt-4:

```$ genie --model gpt-4```

`--model` will also accept *code-davinci-002* & *text-davinci-003* - other API models can be seen here [OpenAI ChatGPT API Models](https://platform.openai.com/docs/models) and added as required to the script.

The temperature used is `0.7` - which appears to be a good balance between creativity and focused responses. 

You can switch temperature using the `--temp` argument (run without `--temp` to use the default value).


To end the interactive chat, use either `bye`,`quit`,`q` or `ctrl+c`.

