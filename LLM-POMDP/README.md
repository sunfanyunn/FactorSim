# FactorSim

This folder contains the code for generating simulations from language
descriptions using PyGame

### Setup
```
pip install -r requirements.txt
# to use OpenAI's language mdoels
export OPENAI_API_KEY=
# to use Replicate's APIs
export REPLICATE_API_TOKEN=
```

### Run
```
python main.py GAME_NAME LLM_MODEL
```

- `GAME_NAME` could be `pong`, `snake`, `pixelcopter`, `puckworld`, `waterworld`, `pong`, `flappy_bird`
- `LLM_MODEL` could be `gpt-4-1106-preview`, `gpt-3.5-turbo-1106` or `llama3`


