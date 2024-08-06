# FactorSim

This folder contains the code for generating simulations from language descriptions using PyGame

### Setup
```
pip install -r requirements.txt
# to use OpenAI's language mdoels
export OPENAI_API_KEY=
```

### Run
1. place your openai api key at `~/api.key` and then run
```
export OPENAI_API_KEY=$(cat ~/api.key)
```

2. Run the following python commmand
```
python main.py GAME_NAME LLM_MODEL
```

A sample command can be found in `go.sh`

`LLM_MODEL` could be `gpt-4-1106-preview`, `gpt-3.5-turbo-1106` or `llama3`


