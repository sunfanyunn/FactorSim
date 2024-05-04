import os
import sys
from game_structure import GameRep
from utils import save_json_to_file, add_initial_states, add_initial_states_code_exp
from game_structure import GameRep
from prompts import high_level_decompose_prompt


def dynamical_import(game_path, context=False):
    # dynamically import the 'prompt' from prompt.py under game_path
    if context:
        prompt_path = os.path.join(game_path, "context_prompts.py")
    else:
        prompt_path = os.path.join(game_path, "prompts.py")

    spec = importlib.util.spec_from_file_location("prompt_module", prompt_path)
    prompt_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prompt_module)
    iterative_prompts = (
        prompt_module.iterative_prompts
    )  # dynamically import the 'prompt' variable
    context_prompt_code = (
        prompt_module.context_prompt_code
    )  # dynamically import the 'prompt' variable
    return iterative_prompts, context_prompt_code


if __name__ == "__main__":
    # Set these game constants
    game_name = sys.argv[1]
    llm_model = sys.argv[2]

    NUM_TRIALS = 20
    USE_DECOMPOSE_PROMPT = True
    WIDTH, HEIGHT, FPS = 1000, 1000, 30

    # make the directory if it does not exist
    game_path = f"./games/single_player_games/{game_name}"
    all_prompts, backbone_code = dynamical_import(game_path)
    save_dir = f"./results_pomdp-{llm_model}/{game_name}_eval"
    log_dir = f"{save_dir}/pomdp_{idx}"
    os.makedirs(log_dir, exist_ok=True)
    implementation_path = log_dir + "/final.py"

    game = GameRep(
        HEIGHT, WIDTH, FPS, MAX_RETRIES=10,
        log_dir=log_dir, debug_mode=1, model=llm_model
    )
    ## add default States to the game
    add_initial_states(game_name, game)
    if USE_DECOMPOSE_PROMPT:
        for _ in range(game.MAX_RETRIES):
            steps = game.ask_llm(high_level_decompose_prompt.format(game_specification=all_prompts))
            try:
                steps = game.ask_llm(high_level_decompose_prompt.format(game_specification=all_prompts))
                all_prompts = steps["steps"]
                break
            except:
                print("Failed to get steps from LLM")
                continue
    else:
        all_prompts = all_prompts.split("\n")

    code = game.export_code()
    for prompt in all_prompts:
        prompt = prompt.strip()
        if prompt == "":
            continue
        for response in game.process_user_query(prompt):
            print(response)
        code = game.export_code()
        with open(implementation_path, "w") as f:
            f.write(code)
